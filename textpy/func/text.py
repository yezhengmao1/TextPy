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
        del args
        return self.prompt_.format(**kwargs)

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
