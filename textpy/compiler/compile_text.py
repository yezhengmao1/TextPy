import os
from dataclasses import dataclass
from typing import List

import yaml

from ..func import TextFunc
from ..jit import text
from .compile_pass import (
    CompileContext,
    CompilePass,
    GetFuncContextPass,
    UnderstandFuncPass,
)

_prompt_cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts")


@text(cache=_prompt_cache_dir)
def _gen_text_func(*, fn_source: str, fn_understand: str) -> str: ...


@dataclass
class TextFuncCompileContext(CompileContext): ...


class LoadTextFuncFromCachePass(CompilePass):
    def __call__(self, func: TextFunc, context: TextFuncCompileContext):
        """
        Load the prompt from cache
        """
        if func.cache_ is None:
            return context

        cache_path = os.path.join(func.cache_, func.fn_name_ + ".yaml")
        if not os.path.isfile(cache_path):
            return context

        with open(cache_path, "r", encoding="utf-8") as file:
            data = yaml.load(file, Loader=yaml.SafeLoader)
            if "prompt" not in data:
                return context
            func.prompt_ = data["prompt"]
            func.fn_desc_ = data["desc"]
            context.is_done_ = True

        return context


class SaveTextFuncToCachePass(CompilePass):
    def __call__(self, func: TextFunc, context: TextFuncCompileContext):
        """
        save the prompt to cache
        """
        if func.cache_ is None:
            return context

        if not os.path.exists(func.cache_):
            os.makedirs(func.cache_)

        cache_path = os.path.join(func.cache_, func.fn_name_ + ".yaml")

        with open(cache_path, "w", encoding="utf-8") as file:
            data = {
                "prompt": func.prompt_.replace("\\n", "\n"),
                "desc": func.fn_desc_,
            }

            yaml.dump(
                data,
                file,
                Dumper=yaml.SafeDumper,
                allow_unicode=True,
                default_style="|",
            )

        return context


class GenTextFuncPropmptPass(CompilePass):
    def __call__(self, func: TextFunc, context: TextFuncCompileContext):
        """
        generate the prompt for textfunc
        """
        prompt = _gen_text_func(
            fn_source=func.fn_source_,
            fn_understand=func.fn_desc_,
        )
        func.prompt_ = prompt
        return context


def compile_text_func(func: TextFunc):
    assert isinstance(func, TextFunc)

    context: TextFuncCompileContext = TextFuncCompileContext()
    compile_text_func_pass: List[CompilePass] = [
        LoadTextFuncFromCachePass(),
        GetFuncContextPass(),
        UnderstandFuncPass(),
        GenTextFuncPropmptPass(),
        SaveTextFuncToCachePass(),
    ]

    for compile_pass in compile_text_func_pass:
        context = compile_pass(func, context)
        if context.is_done_:
            return
