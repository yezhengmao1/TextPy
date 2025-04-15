from typing import Optional

from .func import BaseFunc


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

        return super().__call__(**kwargs)
