import math
import random

import pytest

import main

random.seed()


@pytest.fixture
def int_n():
    return random.randint(5, 20)


def test_factorial_type(int_n):
    assert isinstance(main.factorial(int_n), (int, float)), f"Check the type of the return value : {type(main.factorial(int_n))}"


def test_factorial_result(int_n):
    assert main.factorial(int_n) == math.factorial(int_n), f"Check the return value : {main.factorial(int_n)}"
