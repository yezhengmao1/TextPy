import os

import yaml

from ..func import TextFunc
from ..jit import text

_prompt_cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts")


# All prompts in the textpy/compiler/prompts
# This is a TextFunc, use this prompt to understand the functions
@text(cache=_prompt_cache_dir)
def _understand_func(*, fn_name: str, context: str) -> str: ...


def load_from_cache(func: TextFunc):
    """
    Load the prompt from cache
    :param func: the func
    """
    cache_path = os.path.join(func.cache_, func.fn_name_ + ".yaml")
    if not os.path.isfile(cache_path):
        return

    with open(cache_path, "r", encoding="utf-8") as file:
        data = yaml.load(file, Loader=yaml.SafeLoader)
        if "prompt" not in data:
            return
        func.prompt_ = data["prompt"]
        func.fn_desc_ = data["desc"]


def func_context(func: TextFunc):
    """
    get the func's context
    :param func: the func
    """
    pass


def compile_text_func(func: TextFunc):
    assert isinstance(func, TextFunc)

    # load from cache
    if func.cache_:
        load_from_cache(func)
    if func.prompt_:
        return

    # need call compiler to compile it
    understand_func = _understand_func(
        fn_name=func.fn_name_, context=func_context(func)
    )

    func.fn_desc_ = understand_func
