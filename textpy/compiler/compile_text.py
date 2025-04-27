import os
from typing import List

from ..func import TextFunc
from ..jit import text
from .compile_pass import (
    CompileContextInitPass,
    CompilePass,
    GetFuncContextPass,
    _textpy_prompt_cache_dir,
)


@text(cache=_textpy_prompt_cache_dir, constant=True)
def _gen_text_func(*, fn_name: str, context: str) -> str: ...


class LoadTextFuncFromCachePass(CompilePass):
    def __call__(self, func: TextFunc, **context):
        """
        Load the prompt from cache
        """
        if func.cache_ is None:
            return context

        cache_path = os.path.join(func.cache_, func.fn_name_ + ".text.tpy")
        if not os.path.isfile(cache_path):
            return context

        with open(cache_path, "r", encoding="utf-8") as file:
            func.prompt_ = file.read()
            context["is_done"] = True

        return context


class SaveTextFuncToCachePass(CompilePass):
    def __call__(self, func: TextFunc, **context):
        """
        save the prompt to cache
        """
        if func.cache_ is None:
            return context

        if not os.path.exists(func.cache_):
            os.makedirs(func.cache_)

        cache_path = os.path.join(func.cache_, func.fn_name_ + ".text.tpy")

        with open(cache_path, "w", encoding="utf-8") as file:
            file.write(func.prompt_)
        return context


class GenTextFuncPromptPass(CompilePass):
    def __call__(self, func: TextFunc, **context):
        """
        generate the prompt for textfunc
        """
        prompt = _gen_text_func(
            fn_name=func.fn_name_,
            context=context["func_context"],
        )
        func.prompt_ = prompt
        return context


class CompileTextFuncPass(CompilePass):
    def __call__(self, func: TextFunc, **context):

        compile_text_func_pass: List[CompilePass] = [
            CompileContextInitPass(),
            LoadTextFuncFromCachePass(),
            GetFuncContextPass(),
            GenTextFuncPromptPass(),
            SaveTextFuncToCachePass(),
        ]

        for compile_pass in compile_text_func_pass:
            context = compile_pass(func, **context)
            if context["is_done"]:
                return
