from typing import Callable, Dict

from ..func import Func, TextFunc
from .compile_text import compile_text_func


class AICompiler:

    compile_funcs: Dict[Func, Callable] = {
        TextFunc: compile_text_func,
    }

    @staticmethod
    def compile(func: Func):
        if type(func) not in AICompiler.compile_funcs:
            raise NotImplementedError
        AICompiler.compile_funcs[type(func)](func)
