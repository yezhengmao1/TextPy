import json
import logging
from typing import Callable, Optional

from .func import BaseFunc

logger = logging.getLogger("TextFunc")


class TextFunc(BaseFunc):
    prompt_: Optional[str]

    def __init__(
        self,
        fn: Callable,
        *,
        prompt: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(fn, **kwargs)

        self.prompt_ = prompt

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

    def _extract_function_return_value(self, response: str):
        # extract the return value from the text
        from ..jit import text

        @text(
            cache=self.cache_,
            response_format="json_object",
            constant=True,
        )
        # return json_object, like {"return":""}
        # without any markdown label
        def _textpy_built_in_extract_function_return_value_from_text(
            *, text: str, func_source: str
        ) -> str: ...

        _textpy_built_in_extract_function_return_value_from_text.copy_runtime(self)

        # recurse call the extract function
        response = _textpy_built_in_extract_function_return_value_from_text(
            text=response, func_source=self.fn_source_
        )

        response_obj = json.loads(response)

        return response_obj["return"]

    def __call__(self, **kwargs):
        # if there no prompt we need to compile it
        if self.prompt_ is None:
            from ..compiler import AICompiler

            AICompiler.compile(self)

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

        response = self._extract_function_return_value(response=response)

        return response
