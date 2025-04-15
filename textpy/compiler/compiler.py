from typing import Callable, Dict

from ..func import CodeFunc, Func, TextFunc
from .compile_text import CompileTextFuncPass


class AICompiler:

    compile_funcs: Dict[Func, Callable] = {
        TextFunc: CompileTextFuncPass(),
    }

    @staticmethod
    def set_model():
        pass

    @staticmethod
    def compile(func: Func, **context):
        if type(func) not in AICompiler.compile_funcs:
            raise NotImplementedError
        AICompiler.compile_funcs[type(func)](func, **context)
