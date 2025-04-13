import unittest

from textpy.jit import text


@text(prompt="请输出 {text} 字符串，注意只输出文本，不要有额外内容。")
def test_fn(*, text: str) -> str: ...


class TestTextFuncAndTextVM(unittest.TestCase):
    def test_run_text_func_in_textvm(self):
        output = test_fn(text="Test LLM")
        assert output == "Test LLM"


if __name__ == "__main__":
    unittest.main()
