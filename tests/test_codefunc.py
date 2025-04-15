import unittest

from textpy.jit import code


@code(
    code="""
def output_the_same_as_text(text: str) -> str:
      return text
"""
)
def output_the_same_as_text(*, text: str) -> str: ...


class TestTextFuncAndTVM(unittest.TestCase):
    def test_run_text_func_in_tvm(self):
        output = output_the_same_as_text(text="Test LLM")
        assert output == "Test LLM"


if __name__ == "__main__":
    unittest.main()
