from typing import Callable, Optional

from .func import BaseFunc


class TextFunc(BaseFunc):
    prompt_: str

    def __init__(
        self,
        fn: Callable,
        *,
        prompt: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(fn, **kwargs)

        self.prompt_ = prompt

    def prompt(self, *args, **kwargs):
        assert len(args) == 0
        if self.prompt_ is None:
            raise ValueError("Bug: not compiled this function!!!")

        return self.prompt_.format(**kwargs)

    def __call__(self, *args, **kwargs):
        # if there no prompt we need to compile it
        if self.prompt_ is None:
            from ..compiler import AICompiler

            AICompiler.compile(self)

        return super().__call__(*args, **kwargs)
