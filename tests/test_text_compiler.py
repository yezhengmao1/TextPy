import unittest

from textpy.jit import text


@text(cache=None)
def output_the_same_text(*, text: str) -> str: ...


class TestTextCompiler(unittest.TestCase):
    def test_run_text_compiler(self):
        output = output_the_same_text(text="Test LLM")
        assert output == "Test LLM"


if __name__ == "__main__":
    unittest.main()
