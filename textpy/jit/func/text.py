from typing import Callable, Optional

from textpy.tvm import TVM

from .func import Func


class TextFunc(Func):
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

    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)
