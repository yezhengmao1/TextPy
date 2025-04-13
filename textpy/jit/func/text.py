from typing import Callable, Optional

from textpy.tvm import TVM

from .func import Func


class TextFunc(Func):
    def __init__(
        self,
        fn: Callable,
        *,
        runtime: Optional[TVM] = None,
        cache: Optional[str] = None,
        description: Optional[str] = None,
        prompt: Optional[str] = None,
        override_ret: Optional[Callable] = None,
        override_arg: Optional[Callable] = None,
        **kwargs,
    ):
        super().__init__(fn, **kwargs)

    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)
