import hashlib
import os
from typing import List

from ..func import CodeFunc
from ..jit import text
from .compile_pass import (
    CompileContextInitPass,
    CompilePass,
    GetFuncContextPass,
    _textpy_prompt_cache_dir,
)


@text(
    cache=_textpy_prompt_cache_dir,
    response_format="json_object",
    constant=True,
)
# return json_object, like {"return":""} without any markdown label
def _textpy_built_in_extract_function_source_from_text(
    *, text: str, func_name: str
) -> str: ...


@text(
    cache=_textpy_prompt_cache_dir,
    constant=True,
)
def _textpy_built_in_gen_code_func(*, fn_name: str, context: str, pypi: str) -> str: ...


@text(
    cache=_textpy_prompt_cache_dir,
    constant=True,
)
# move all import command into the function
def _textpy_built_in_move_the_import_command_into_func(*, fn_source: str) -> str: ...


class LoadCodeFuncFromCachePass(CompilePass):
    def __call__(self, func: CodeFunc, **context):
        """
        Load the code from cache
        """
        if func.cache_ is None:
            return context

        file_name = func.fn_name_
        if not file_name.startswith("_textpy_built_in"):
            file_name += "." + hashlib.md5(func.fn_source_.encode()).hexdigest()[:8]

        cache_path = os.path.join(func.cache_, file_name + ".code.tpy")
        if not os.path.isfile(cache_path):
            return context

        with open(cache_path, "r", encoding="utf-8") as file:
            func.code_ = file.read()
            context["is_done"] = True

        return context


class SaveCodeFuncToCachePass(CompilePass):
    def __call__(self, func: CodeFunc, **context):
        """
        save the code to cache
        """
        if func.cache_ is None:
            return context

        if not os.path.exists(func.cache_):
            os.makedirs(func.cache_)

        file_name = func.fn_name_
        if not file_name.startswith("_textpy_built_in"):
            file_name += "." + hashlib.md5(func.fn_source_.encode()).hexdigest()[:8]

        cache_path = os.path.join(func.cache_, file_name + ".code.tpy")

        with open(cache_path, "w", encoding="utf-8") as file:
            file.write(func.code_)

        return context


class GetPypiPackageContextPass(CompilePass):
    def __call__(self, func: CodeFunc, **context):
        """
        Collect the tool's information for the func
        """
        if func.pypi_package_ is None or len(func.pypi_package_) == 0:
            context["pypi"] = ""
            return context

        # get the pypi info from the url
        context["pypi"] = ""
        for package in func.pypi_package_:
            context["pypi"] += "\n" + package + "\n"

        return context


class GenCodeFuncCodePass(CompilePass):
    def __call__(self, func: CodeFunc, **context):
        """
        generate the code for codefunc
        """
        context["code"] = _textpy_built_in_gen_code_func(
            fn_name=func.fn_name_,
            context=context["func_context"],
            pypi=context["pypi"],
        )

        return context


class AdjustImportInFuncCodePass(CompilePass):
    def __call__(self, func: CodeFunc, **context):
        """
        relocates module import statements from the module-level scope into function bodies
        """
        context["code"] = _textpy_built_in_move_the_import_command_into_func(
            fn_source=context["code"]
        )
        return context


class ExtractFuncFromTextPass(CompilePass):
    def __call__(self, func: CodeFunc, **context):
        """
        extract the function from the text
        """
        import json

        func.code_ = json.loads(
            _textpy_built_in_extract_function_source_from_text(
                text=context["code"], func_name=func.fn_name_
            )
        )["return"]

        return context


class CompileCodeFuncPass(CompilePass):
    def __call__(self, func: CodeFunc, **context):

        compile_code_func_pass: List[CompilePass] = [
            CompileContextInitPass(),
            LoadCodeFuncFromCachePass(),
            GetFuncContextPass(),
            GetPypiPackageContextPass(),
            GenCodeFuncCodePass(),
            AdjustImportInFuncCodePass(),
            ExtractFuncFromTextPass(),
            SaveCodeFuncToCachePass(),
        ]

        for compile_pass in compile_code_func_pass:
            context = compile_pass(func, **context)
            if context["is_done"]:
                return
