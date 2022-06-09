import pytest
import json_py
import json_py.lexer as lexer
import json_py.parser as parser


def test_parser():
    expected = {"hello": ["world", "!", 69], 3: 9.1}
    assert json_py.from_json('{"hello": ["world", "!", 69], 3: 9.1}') == expected
    assert json_py.from_json('{"friends": null}') == {"friends": None}


def test_lex_string():
    assert lexer.lex_string('"hello"') == ("hello", "")


def test_lex_number():
    assert lexer.lex_number("1349") == (1349, "")
    assert lexer.lex_number("6.9") == (6.9, "")
    with pytest.raises(ValueError):
        lexer.lex_number("6..9")


def test_lex_bool():
    assert lexer.lex_bool("True") == (True, "")
    assert lexer.lex_bool("False") == (False, "")
    assert lexer.lex_bool("Sample") == (None, "Sample")


def test_lex_null():
    assert lexer.lex_null("null") == (True, "")


def test_lex_object():
    assert lexer.lex("{12: 2, 3: 4}") == ["{", 12, ":", 2, ",", 3, ":", 4, "}"]


def test_parse_array():
    # Skip first token 'cos parser consumes it.
    assert parser.parse_array([12, ",", 2, "]"]) == ([12, 2], [])
    assert parser.parse_array(["]"]) == ([], [])
    with pytest.raises(ValueError):
        parser.parse_array([12, "," "]"])
    with pytest.raises(ValueError):
        parser.parse_array([12, 3, "]"])
    with pytest.raises(ValueError):
        parser.parse_array([12, ",", 3])


def test_parse_object():
    # Skip first token 'cos parser consumes it.
    assert parser.parse_object(["}"]) == ({}, [])
    assert parser.parse_object(["age", ":", 21, "}"]) == ({"age": 21}, [])
    assert parser.parse_object(["12", ":", "[", 1, "]", "}"]) == ({"12": [1]}, [])
