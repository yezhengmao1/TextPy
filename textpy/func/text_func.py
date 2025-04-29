import json
import logging
from typing import Callable, Optional

from .func import BaseFunc

logger = logging.getLogger("TextFunc")


class TextFunc(BaseFunc):
    prompt_: Optional[str]
    built_in_extract_return_func_: Optional[Callable]

    def __init__(
        self,
        fn: Callable,
        *,
        prompt: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(fn, **kwargs)

        self.prompt_ = prompt
        self.built_in_extract_return_func_ = None

    def prompt(self, **kwargs):
        if self.prompt_ is None:
            raise ValueError("Bug: not compiled this function!!!")

        # safe replace
        prompt = self.prompt_
        for key, value in kwargs.items():
            replace_key = "{" + key + "}"
            if replace_key not in prompt:
                continue
            prompt = prompt.replace(replace_key, value)

        return prompt

    def __call__(self, **kwargs):
        # if there no prompt we need to compile it
        if self.prompt_ is None:
            from ..compiler import AICompiler

            logger.info(f"compile TextFunc <{self.fn_name_}> .....")
            AICompiler.compile(self)
            logger.info(f"compile TextFunc <{self.fn_name_}> done!")

        assert self.runtime_ is not None

        response = self.runtime_(self, **kwargs)

        if self.constant_ and self.override_ret_ is None:
            return response

        if self.constant_ and self.override_arg_ is not None:
            return self.override_ret_(response)

        # constant is False need to optimize
        # TODO: optimize loop
        #     check the response, the response must same with the func's return value
        #     maybe we need to recompile it

        if self.built_in_extract_return_func_:
            response = self.built_in_extract_return_func_(response=response)

        return response
