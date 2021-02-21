import math
import random
import sys

import pytest

import main

random.seed()


@pytest.fixture
def int_n() -> int:
    return random.randint(5, 20)


@pytest.fixture
def filename() -> str:
    return 'main.py'


def test_factorial_type(int_n:int):
    assert isinstance(main.factorial(int_n), (int, float)), f"Check the type of the return value : {type(main.factorial(int_n))}"


def test_factorial_result(int_n:int):
    assert main.factorial(int_n) == math.factorial(int_n), f"Check the return value : {main.factorial(int_n)}"


if "__main__" == __name__:
    pytest.main()
