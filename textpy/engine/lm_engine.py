from typing import Optional

from litellm import completion

from .engine import BaseEngine


class LMEngine(BaseEngine):
    model_: str
    api_key_: Optional[str]

    token_cnt_: int = 0

    def __init__(
        self,
        model: str,
        api_key: Optional[None],
    ):
        super().__init__()

        self.model_ = model
        self.api_key_ = api_key

    def run(self, prompt: str):
        resp = completion(
            model=self.model_,
            api_key=self.api_key_,
            messages=[{"content": prompt, "role": "user"}],
        )
        self.token_cnt_ += int(resp.usage.total_tokens)
        return resp.choices[0].message.content
