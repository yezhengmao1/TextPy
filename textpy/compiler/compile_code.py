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
def _textpy_built_in_gen_code_func(*, fn_name: str, context: str) -> str: ...


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


class GenCodeFuncCodePass(CompilePass):
    def __call__(self, func: CodeFunc, **context):
        """
        generate the code for codefunc
        """
        text = _textpy_built_in_gen_code_func(
            fn_name=func.fn_name_,
            context=context["func_context"],
        )
        import json

        func.code_ = json.loads(
            _textpy_built_in_extract_function_source_from_text(
                text=text, func_name=func.fn_name_
            )
        )["return"]

        return context


class CompileCodeFuncPass(CompilePass):
    def __call__(self, func: CodeFunc, **context):

        compile_code_func_pass: List[CompilePass] = [
            CompileContextInitPass(),
            LoadCodeFuncFromCachePass(),
            GetFuncContextPass(),
            GenCodeFuncCodePass(),
            SaveCodeFuncToCachePass(),
        ]

        for compile_pass in compile_code_func_pass:
            context = compile_pass(func, **context)
            if context["is_done"]:
                return
