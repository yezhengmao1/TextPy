from typing import Callable, Dict, List

from ..func import CodeFunc, Func, TextFunc
from ..vm import VM
from .compile_code import CompileCodeFuncPass
from .compile_text import CompileTextFuncPass


class AICompiler:

    compile_funcs: Dict[Func, Callable] = {
        TextFunc: CompileTextFuncPass(),
        CodeFunc: CompileCodeFuncPass(),
    }

    @staticmethod
    def set_compiler(**kwargs):
        """
        set the compiler used base model
        """
        from .compile_code import _extract_function_code_from_text, _gen_code_func
        from .compile_text import _gen_text_func

        lm_funcs: List[TextFunc] = [
            _extract_function_code_from_text,
            _gen_code_func,
            _gen_text_func,
        ]

        for lm_func in lm_funcs:
            lm_func.set_runtime(VM["TextVM"](**kwargs))

    @staticmethod
    def compile(func: Func, **context):
        if type(func) not in AICompiler.compile_funcs:
            raise NotImplementedError
        AICompiler.compile_funcs[type(func)](func, **context)
