from typing import Callable, Dict

from ..func import Func, TextFunc
from .compile_text import compile_text_func


class Compiler:

    compile_funcs: Dict[Func, Callable] = {
        TextFunc: compile_text_func,
    }

    @staticmethod
    def compile(func: Func):
        if type(func) not in Compiler.compile_funcs:
            raise NotImplementedError
        Compiler.compile_funcs[type(func)](func)
