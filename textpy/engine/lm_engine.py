from typing import Optional

from litellm import completion

from .engine import BaseEngine


class LMEngine(BaseEngine):
    model_: str
    api_key_: Optional[str]
    base_url_: Optional[str]

    response_format_: str

    token_cnt_: int = 0

    def __init__(
        self,
        model: str = "deepseek/deepseek-chat",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        response_format: str = "text",
        **kwargs,
    ):
        super().__init__()

        self.model_ = model
        self.api_key_ = api_key
        self.base_url_ = base_url

        self.response_format_ = response_format

        del kwargs

    def run(self, prompt: str):
        resp = completion(
            model=self.model_,
            api_key=self.api_key_,
            base_url=self.base_url_,
            response_format={"type": self.response_format_},
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": prompt},
            ],
        )
        self.token_cnt_ += int(resp.usage.total_tokens)
        return resp.choices[0].message.content

    def copy(self, engine: "LMEngine"):
        self.model_ = engine.model_
        self.api_key_ = engine.api_key_
        self.base_url_ = engine.base_url_
