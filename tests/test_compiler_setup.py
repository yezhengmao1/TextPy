import unittest

from textpy.compiler import AICompiler
from textpy.engine.engine import BaseEngine

is_called = False


class TestEngine(BaseEngine):
    def __init__(self):
        super().__init__()
        global is_called
        is_called = True


class TestCompilerSetup(unittest.TestCase):
    def test_compiler_setup(self):
        AICompiler.set_compiler(runtime={"engine": "TestEngine"})
        assert is_called == True
        AICompiler.set_compiler(runtime={"engine": "LMEngine"})


if __name__ == "__main__":
    unittest.main()
