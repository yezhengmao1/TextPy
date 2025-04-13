import os

from ..func import BaseFunc
from ..jit import text

_textpy_prompt_cache_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "prompts"
)


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
