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
    assert 'numpy' not in sys.modules, f"Check if the numpy is installed"


@pytest.fixture(scope='session')
def ast_root(filename):
    # https://stackoverflow.com/a/9049549

    with open(filename, 'rt') as f:
        root = ast.parse(f.read(), filename)

    return root


def get_imports(root:ast.AST):
    # https://stackoverflow.com/a/9049549
    Import = collections.namedtuple("Import", ["module", "name", "alias"])

    result = []

    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.Import):
            module = []
        elif isinstance(node, ast.ImportFrom):
            module = node.module.split('.')
        elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            function_result = get_imports(node)
            if function_result:
                result += function_result
            continue
        else:
            continue

        for n in node.names:
            result.append(Import(module, n.name.split('.'), n.asname))

    return result


@pytest.fixture(scope="session")
def imports(ast_root):
    return get_imports(ast_root)


def test_main_imports_math(imports):
    for import_tuple in imports:
        assert 'math' not in import_tuple.name, "Check if main.py imports math module"


def test_main_imports_numpy(imports):
    for import_tuple in imports:
        assert 'numpy' not in import_tuple.name, "Check if main.py imports numpy module"


def get_functions(ast_root:ast.AST):
    function_def_list = []

    for node in ast.iter_child_nodes(ast_root):
        if isinstance(node, ast.FunctionDef):
            function_def_list.append((node.name, node))
            function_def_list += get_functions(node)

    return function_def_list            


@pytest.fixture(scope='session')
def ast_function(ast_root):
    return get_functions(ast_root)


def test_get_functions():
    src = (
        'def f(x):\n'
        '   def g(y):\n'
        '       return y * x\n'
        '   return g(x)'
    )

    root = ast.parse(src)

    result = get_functions(root)

    names = [n[0] for n in result]

    assert 'f' in names
    assert 'g' in names


@pytest.fixture
def function_factorial(ast_function):
    result = []
    for name, func in ast_function:
        if 'factorial' == name:
            result.append((name, func))
    return result


def test_is_for_in_factorial(function_factorial):
    for func_factorial in function_factorial:
        ast_factorial = func_factorial[1]

        for node in ast.iter_child_nodes(ast_factorial):
            assert not isinstance(node, ast.For), "Check if factorial() is using for"


def test_is_while_in_factorial(function_factorial):
    for func_factorial in function_factorial:
        ast_factorial = func_factorial[1]

        for node in ast.iter_child_nodes(ast_factorial):
            assert not isinstance(node, ast.While), "Check if factorial() is using While"


if "__main__" == __name__:
    pytest.main()
