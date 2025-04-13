import unittest

from textpy.jit import code


@code(cache=None)
# without code decorator
def output_the_same_text(*, text: str) -> str: ...


class TestCodeCompiler(unittest.TestCase):
    def test_run_code_compiler(self):
        output = output_the_same_text(text="Test LLM")
        assert output == "Test LLM"


if __name__ == "__main__":
    unittest.main()
