import random
import urllib.request as ur
from typing import List

import pytest

import main

random.seed()


@pytest.fixture
def url():
    return 'https://www.mit.edu/~ecprice/wordlist.10000'


@pytest.fixture
def words(url, scope='session') -> List[bytes]:
    # https://docs/python.org/3/library/urllib.request.html
    with ur.urlopen(url) as req:
        txt_lines = req.readlines()
    return txt_lines


@pytest.fixture
def sample_string(words:List[str]) -> str:
    # https://docs/python.org/3/library/random.html
    min_words = 5
    max_words = 10
    assert len(words) >= min_words
    n = random.randint(min_words, min(max_words, len(words)))
    word_list = list(map(lambda w:w.decode().strip(), random.choices(words, k=n)))
    random.shuffle(word_list)
    return ' '.join(word_list)


def test_first_word_type(sample_string:str):
    assert isinstance(main.first_word(sample_string), str), f"Check return type: {type(main.first_word(sample_string))}"


def test_first_word_result_shorter_than_input(sample_string:str):
    assert len(main.first_word(sample_string)) < len(sample_string), f"Check len(result) = {len(main.first_word(sample_string))} vs len(sample_string) = {len(sample_string)}"


def test_first_word_white_space_in_result(sample_string:str):
    assert all(map(lambda x: x not in (' \t\n'), main.first_word(sample_string))), f"Result includes (a) whitespace(s) : {main.first_word(sample_string)!r}"


def test_first_word_result(sample_string:str):
    assert sample_string.startswith(main.first_word(sample_string)), f"Check result = {main.first_word(sample_string)!r}, input string = {sample_string}"


def test_last_word_type(sample_string:str):
    assert isinstance(main.last_word(sample_string), str), f"Check return type: {type(main.last_word(sample_string))}"


def test_last_word_result_shorter_than_input(sample_string:str):
    assert len(main.last_word(sample_string)) < len(sample_string), f"Check len(result) = {len(main.last_word(sample_string))} vs len(sample_string) = {len(sample_string)}"


def test_last_word_white_space_in_result(sample_string:str):
    assert all(map(lambda x: x not in (' \t\n'), main.last_word(sample_string))), f"Result includes (a) whitespace(s) : {main.last_word(sample_string)!r}"


def test_last_word_result(sample_string:str):
    assert sample_string.endswith(main.last_word(sample_string)), f"Check result = {main.first_word(sample_string)!r}, input string = {sample_string}"


if "__main__" == __name__:
    pytest.main()
