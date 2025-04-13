import unittest

from textpy.jit import text
from textpy.vm import TextVM


@text(runtime=TextVM(engine="LMEngine", model="deepseek/deepseek-chat"))
def output_the_text(*, text: str) -> str: ...


class TestTextCompiler(unittest.TestCase):
    def test_run_text_compiler(self):
        output = output_the_text(text="Test LLM")
        assert output == "Test LLM"


if __name__ == "__main__":
    unittest.main()
