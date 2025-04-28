import logging
from typing import List

from ..func import CodeFunc
from ..jit import text
from .compile_code import (
    AdjustImportInFuncCodePass,
    ExtractFuncFromTextPass,
    SaveCodeFuncToCachePass,
)
from .compile_pass import CompileContextInitPass, CompilePass, _textpy_prompt_cache_dir

logger = logging.getLogger("OptimizeCode")


@text(
    cache=_textpy_prompt_cache_dir,
    constant=True,
)
# according the error information to modify the function
# ensure the function can be execute
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
        context["code"] = _textpy_built_in_code_optimize_by_feedback_func(
            fn_source=func.code_, fn_feedback=context["feedback"]
        )
        return context


class OptimizeCodeFuncPass(CompilePass):
    def __call__(self, func: CodeFunc, **context):

        compile_code_func_pass: List[CompilePass] = [
            CompileContextInitPass(),
            ContinueToOptimizeCodeFuncPass(),
            ReGenCodeFuncCodeByFeedbackPass(),
            AdjustImportInFuncCodePass(),
            ExtractFuncFromTextPass(),
            SaveCodeFuncToCachePass(),
        ]

        logging.info(f"optimize the function: {func.fn_name_}")

        for compile_pass in compile_code_func_pass:
            context = compile_pass(func, **context)
            if context["is_done"]:
                return
