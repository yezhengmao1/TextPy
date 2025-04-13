import os
from dataclasses import dataclass
from typing import Callable, List

import yaml

from ..func import TextFunc
from ..jit import text

_prompt_cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts")


@dataclass
class TextFuncCompileContext:
    is_done_: bool = False


# All prompts in the textpy/compiler/prompts
# This is a TextFunc, use this prompt to understand the functions
@text(cache=_prompt_cache_dir)
def _understand_func(*, fn_name: str, context: str) -> str: ...


@text(cache=_prompt_cache_dir)
def _gen_text_func(*, fn_source: str, fn_understand: str) -> str: ...


def func_context(func: TextFunc) -> str:
    """
    Collect the func's context, defult: read the function's entire file
    """
    with open(func.fn_file_, "r", encoding="utf-8") as file:
        return file.read()


def load_from_cache(func: TextFunc, context: TextFuncCompileContext):
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


def save_to_cache(func: TextFunc, context: TextFuncCompileContext):
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


def understand_func(func: TextFunc, context: TextFuncCompileContext):
    """
    understand the function
    """
    understand_func = _understand_func(
        fn_name=func.fn_name_, context=func_context(func)
    )
    func.fn_desc_ = understand_func
    return context


def gen_text_func_prompt(func: TextFunc, context: TextFuncCompileContext):
    prompt = _gen_text_func(
        fn_source=func.fn_source_,
        fn_understand=func.fn_desc_,
    )
    func.prompt_ = prompt
    return context


def compile_text_func(func: TextFunc):
    assert isinstance(func, TextFunc)

    context: TextFuncCompileContext = TextFuncCompileContext()
    compile_text_func_pass: List[Callable] = [
        load_from_cache,
        understand_func,
        gen_text_func_prompt,
        save_to_cache,
    ]

    for compile_pass in compile_text_func_pass:
        context = compile_pass(func, context)
        if context.is_done_:
            return
