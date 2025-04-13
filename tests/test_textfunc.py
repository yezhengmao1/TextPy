import unittest

from textpy.jit import text
from textpy.vm import TVM


@text(runtime=TVM(), prompt="请输出hello world字符串")
def test_fn() -> str: ...


class TestTextFuncAndTVM(unittest.TestCase):
    def test_run_text_func_in_tvm(self):
        test_fn()


if __name__ == "__main__":
    unittest.main()
