import os
from dataclasses import dataclass

from ..func.func import BaseFunc
from ..jit import text

_prompt_cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts")


# All prompts in the textpy/compiler/prompts
# This is a TextFunc, use this prompt to understand the functions
@text(cache=_prompt_cache_dir)
def _understand_func(*, fn_name: str, context: str) -> str: ...


@dataclass
class CompileContext:
    is_done_: bool = False
    # the func's context in the source file
    func_context_: str = ""


class CompilePass:
    def __call__(self, func: BaseFunc, context: CompileContext): ...


class UnderstandFuncPass(CompilePass):
    def __call__(self, func: BaseFunc, context: CompileContext):
        """
        understand the function
        """
        understand_func = _understand_func(
            fn_name=func.fn_name_, context=context.func_context_
        )
        func.fn_desc_ = understand_func
        return context


class GetFuncContextPass(CompilePass):
    def __call__(self, func: BaseFunc, context: CompileContext):
        """
        Collect the func's context, defult: read the function's entire file
        """
        with open(func.fn_file_, "r", encoding="utf-8") as file:
            context.func_context_ = file.read()
        return context
