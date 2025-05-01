import threading
import time
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

    compile_lock = threading.Lock()
    compiling_funcs = set()

    optimize_lock = threading.Lock()
    optimizing_funcs = set()

    @staticmethod
    def compile(func: Func, **context):
        if type(func) not in AICompiler.compile_funcs:
            raise NotImplementedError

        # only compile one function if the funcion need to be cached
        if func.cache_ is None:
            return AICompiler.compile_funcs[type(func)](func, **context)

        AICompiler.compile_lock.acquire_lock()

        check_compiling = func.fn_name_ in AICompiler.compiling_funcs

        if check_compiling:
            AICompiler.compile_lock.release()
            while check_compiling:
                check_compiling = func.fn_name_ in AICompiler.compiling_funcs
                # it's ok do not acquire the lock
                time.sleep(0.1)
        else:
            AICompiler.compiling_funcs.add(func.fn_name_)
            AICompiler.compile_lock.release()

            AICompiler.compile_funcs[type(func)](func, **context)
            AICompiler.compiling_funcs.remove(func.fn_name_)

    @staticmethod
    def optimize(func: Func, **context):
        if type(func) not in AICompiler.optimize_funcs:
            raise NotImplementedError

        if func.cache_ is None:
            AICompiler.optimize_funcs[type(func)](func, **context)

        AICompiler.optimize_lock.acquire_lock()

        check_optimizing = func.fn_name_ in AICompiler.optimizing_funcs

        if check_optimizing:
            AICompiler.optimize_lock.release()
            while check_optimizing:
                check_optimizing = func.fn_name_ in AICompiler.optimizing_funcs
                # it's ok do not acquire the lock
                time.sleep(0.1)
        else:
            AICompiler.optimizing_funcs.add(func.fn_name_)
            AICompiler.optimize_lock.release()

            AICompiler.optimize_funcs[type(func)](func, **context)
            AICompiler.optimizing_funcs.remove(func.fn_name_)
