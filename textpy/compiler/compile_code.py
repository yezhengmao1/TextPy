import os
from typing import List

import yaml

from ..func import CodeFunc
from ..jit import text
from .compile_pass import (
    CompileContextInitPass,
    CompilePass,
    GetFuncContextPass,
    _textpy_prompt_cache_dir,
)


@text(cache=_textpy_prompt_cache_dir)
def _gen_code_func(*, fn_name: str, context: str) -> str: ...


@text
# without any markdown label, and only text
def _extract_function_code_from_text(*, text: str, func_name: str) -> str: ...


class LoadCodeFuncFromCachePass(CompilePass):
    def __call__(self, func: CodeFunc, **context):
        """
        Load the code from cache
        """
        if func.cache_ is None:
            return context

        cache_path = os.path.join(func.cache_, func.fn_name_ + ".yaml")
        if not os.path.isfile(cache_path):
            return context

        with open(cache_path, "r", encoding="utf-8") as file:
            data = yaml.load(file, Loader=yaml.SafeLoader)
            if "code" not in data:
                return context
            func.code_ = data["code"]
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

        cache_path = os.path.join(func.cache_, func.fn_name_ + ".yaml")

        with open(cache_path, "w", encoding="utf-8") as file:
            data = {"code": func.code_}

            yaml.dump(
                data,
                file,
                Dumper=yaml.SafeDumper,
                allow_unicode=True,
                default_style="|",
            )

        return context


class GenCodeFuncCodePass(CompilePass):
    def __call__(self, func: CodeFunc, **context):
        """
        generate the code for codefunc
        """
        code = _gen_code_func(
            fn_name=func.fn_name_,
            context=context["func_context"],
        )
        code = _extract_function_code_from_text(text=code, func_name=func.fn_name_)
        func.code_ = code
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
