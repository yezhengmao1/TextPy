import os

from ..func.func import BaseFunc
from ..jit import text

_prompt_cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts")


# All prompts in the textpy/compiler/prompts
# This is a TextFunc, use this prompt to understand the functions
@text(cache=_prompt_cache_dir)
def _understand_func(*, fn_name: str, context: str) -> str: ...


class CompilePass:
    def __call__(self, func: BaseFunc, **context): ...


class CompileContextInitPass(CompilePass):
    def __call__(self, func: BaseFunc, **context):
        """
        init the context
        """
        context["is_done"] = False
        return context


class GetFuncContextPass(CompilePass):
    def __call__(self, func: BaseFunc, **context):
        """
        Collect the func's context, defult: read the function's entire file
        """
        with open(func.fn_file_, "r", encoding="utf-8") as file:
            context["func_context"] = file.read()
        return context


class UnderstandFuncPass(CompilePass):
    def __call__(self, func: BaseFunc, **context):
        """
        understand the function
        """
        understand_func = _understand_func(
            fn_name=func.fn_name_, context=context["func_context"]
        )
        func.fn_desc_ = understand_func
        return context
