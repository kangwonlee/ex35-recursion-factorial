import ast
import collections
import math
import random
import sys

import pytest

import main

random.seed()


@pytest.fixture
def int_n() -> int:
    return random.randint(5, 20)


@pytest.fixture(scope="session")
def filename() -> str:
    return 'main.py'


def test_factorial_type(int_n:int):
    assert isinstance(main.factorial(int_n), (int, float)), f"Check the type of the return value : {type(main.factorial(int_n))}"


def test_factorial_result(int_n:int):
    assert main.factorial(int_n) == math.factorial(int_n), f"Check the return value : {main.factorial(int_n)}"


def test_is_numpy_installed():
    assert 'numpy' not in sys.modules


def get_imports(filename):
    # https://stackoverflow.com/a/9049549

    Import = collections.namedtuple("Import", ["module", "name", "alias"])

    with open(filename, 'rt') as f:
        root = ast.parse(f.read(), filename)
    
    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.Import):
            module = []
        elif isinstance(node, ast.ImportFrom):
            module = node.module.split('.')
        else:
            continue

        for n in node.names:
            yield Import(module, n.name.split('.'), n.asname)


@pytest.fixture(scope="session")
def imports(filename):
    return list(get_imports(filename))


def test_main_imports_math(imports):
    for import_tuple in imports:
        assert 'math' not in import_tuple.module, "Check if main.py imports math module"


def test_main_imports_numpy(imports):
    for import_tuple in imports:
        assert 'numpy' not in import_tuple.module, "Check if main.py imports numpy module"


if "__main__" == __name__:
    pytest.main()
