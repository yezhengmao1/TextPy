import logging
from typing import List, Optional

from .func import BaseFunc

logger = logging.getLogger("CodeFunc")


class CodeFunc(BaseFunc):
    code_: Optional[str]
    pypi_package_: Optional[List[str]]

    def __init__(
        self,
        fn: callable,
        *,
        code: Optional[str] = None,
        pypi_package: Optional[List[str]] = None,
        **kwargs,
    ):
        super().__init__(fn, **kwargs)

        self.code_ = code
        self.pypi_package_ = pypi_package

    def code(self) -> str:
        return self.code_

    def __call__(self, **kwargs):
        # if there no code we need to compile it
        if self.code_ is None:
            from ..compiler import AICompiler

            logger.info(f"compile CodeFunc <{self.fn_name_}> .....")
            AICompiler.compile(self)
            logger.info(f"compile CodeFunc <{self.fn_name_}> done!")

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

                logger.info(f"optimize CodeFunc <{self.fn_name_}> .....")
                AICompiler.optimize(self, feedback=error_info)
                logger.info(f"optimize CodeFunc <{self.fn_name_}> done!")

            if execute_try_optimize >= 5:
                raise RuntimeError

        return response
