from typing import List

from ..func import CodeFunc
from ..jit import text
from .compile_code import (
    SaveCodeFuncToCachePass,
    _textpy_built_in_extract_function_source_from_text,
)
from .compile_pass import CompileContextInitPass, CompilePass, _textpy_prompt_cache_dir


@text(
    cache=_textpy_prompt_cache_dir,
    constant=True,
)
def _textpy_built_in_code_optimize_by_feedback_func(
    *, fn_source: str, fn_feedback: str
) -> str: ...


class ContinueToOptimizeCodeFuncPass(CompilePass):
    def __call__(self, func: CodeFunc, **context):

        assert func.code_ is not None
        assert "feedback" in context

        return context


class ReGenCodeFuncCodeByFeedbackPass(CompilePass):
    def __call__(self, func: CodeFunc, **context):
        text = _textpy_built_in_code_optimize_by_feedback_func(
            fn_source=func.code_, fn_feedback=context["feedback"]
        )
        import json

        func.code_ = json.loads(
            _textpy_built_in_extract_function_source_from_text(
                text=text, func_name=func.fn_name_
            )
        )["return"]

        return context


class OptimizeCodeFuncPass(CompilePass):
    def __call__(self, func: CodeFunc, **context):

        compile_code_func_pass: List[CompilePass] = [
            CompileContextInitPass(),
            ContinueToOptimizeCodeFuncPass(),
            ReGenCodeFuncCodeByFeedbackPass(),
            SaveCodeFuncToCachePass(),
        ]

        for compile_pass in compile_code_func_pass:
            context = compile_pass(func, **context)
            if context["is_done"]:
                return
