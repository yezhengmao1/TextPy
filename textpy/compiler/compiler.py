from typing import Callable, Dict, List, Optional

from ..func import CodeFunc, Func, TextFunc
from ..vm import VM
from .compile_code import CompileCodeFuncPass
from .compile_text import CompileTextFuncPass
from .optimize_code import OptimizeCodeFuncPass


class AICompiler:

    compile_funcs: Dict[Func, Callable] = {
        TextFunc: CompileTextFuncPass(),
        CodeFunc: CompileCodeFuncPass(),
    }

    optimize_funcs: Dict[Func, Callable] = {
        CodeFunc: OptimizeCodeFuncPass(),
    }

    @staticmethod
    def set_compiler(
        runtime: Optional[Dict] = None,
        cache: Optional[str] = None,
    ):
        """
        set the compiler used base model
        """
        from .compile_code import (
            _textpy_built_in_extract_function_source_from_text,
            _textpy_built_in_gen_code_func,
            _textpy_built_in_move_the_import_command_into_func,
        )
        from .compile_text import (
            _textpy_built_in_extract_function_return_value_from_text,
            _textpy_built_in_gen_text_func,
        )
        from .optimize_code import _textpy_built_in_code_optimize_by_feedback_func

        lm_funcs: List[TextFunc] = [
            _textpy_built_in_gen_code_func,
            _textpy_built_in_gen_text_func,
            _textpy_built_in_extract_function_return_value_from_text,
            _textpy_built_in_extract_function_source_from_text,
            _textpy_built_in_code_optimize_by_feedback_func,
            _textpy_built_in_move_the_import_command_into_func,
        ]

        if runtime is not None:
            for lm_func in lm_funcs:
                lm_func.set_runtime(VM["TextVM"](**runtime))

        if cache is not None:
            for lm_func in lm_funcs:
                lm_func.cache_ = cache

    @staticmethod
    def compile(func: Func, **context):
        if type(func) not in AICompiler.compile_funcs:
            raise NotImplementedError
        AICompiler.compile_funcs[type(func)](func, **context)

    @staticmethod
    def optimize(func: Func, **context):
        if type(func) not in AICompiler.optimize_funcs:
            raise NotImplementedError
        AICompiler.optimize_funcs[type(func)](func, **context)
