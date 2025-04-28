import logging
from typing import Optional

from .func import BaseFunc

logger = logging.getLogger("CodeFunc")


class CodeFunc(BaseFunc):
    code_: Optional[str]

    def __init__(
        self,
        fn: callable,
        *,
        code: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(fn, **kwargs)

        self.code_ = code

    def code(self) -> str:
        return self.code_

    def __call__(self, **kwargs):
        # if there no code we need to compile it
        if self.code_ is None:
            from ..compiler import AICompiler

            AICompiler.compile(self)

        assert self.runtime_ is not None

        execute_try_optimize = 0

        while True:
            try:
                response = self.runtime_(self, **kwargs)
                break
            except Exception as e:
                error_info = f"execute function error, error type {type(e)}: {str(e)}"

                logger.info(
                    "code func execute error\n"
                    + f"the code is:\n{self.code_}\n"
                    + f"the error information:\n{error_info}\n"
                )

                # use the error_info to optimize the code
                execute_try_optimize += 1
                AICompiler.optimize(self, feedback=error_info)

            if execute_try_optimize >= 5:
                raise RuntimeError

        return response
