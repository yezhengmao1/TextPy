import os
from dataclasses import dataclass
from typing import Callable, List

import yaml

from ..func import CodeFunc
from ..jit import text
from .compile_pass import CompileContext, CompilePass

_prompt_cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts")


@dataclass
class CodeFuncCompileContext(CompileContext): ...


class LoadCodeFuncFromCachePass(CompilePass):
    def __call__(self, func: CodeFunc, context: CodeFuncCompileContext):
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
            if "prompt" not in data:
                return context
            func.code_ = data["code"]
            func.fn_desc_ = data["desc"]
            context.is_done_ = True

        return context


def save_to_cache(func: CodeFunc, context: CodeFuncCompileContext):
    if func.cache_ is None:
        return context

    if not os.path.exists(func.cache_):
        os.makedirs(func.cache_)

    cache_path = os.path.join(func.cache_, func.fn_name_ + ".yaml")

    with open(cache_path, "w", encoding="utf-8") as file:
        data = {
            "code": func.code_.replace("\\n", "\n"),
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


def compile_text_func(func: CodeFunc):
    assert isinstance(func, CodeFunc)

    context: CodeFuncCompileContext = CodeFuncCompileContext()
    compile_text_func_pass: List[Callable] = [
        load_from_cache,
    ]

    for compile_pass in compile_text_func_pass:
        context = compile_pass(func, context)
        if context.is_done_:
            return
