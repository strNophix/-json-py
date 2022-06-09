from __future__ import annotations
import typing
import json_py.lexer as lexer
import json_py.parser as parser


def to_json(obj: typing.Any) -> str:
    raise NotImplementedError("Not implemented yet")


def from_json(string: str) -> typing.Any:
    tokens = lexer.lex(string)
    return parser.parse(tokens)[0]


__all__ = (
    "to_json",
    "from_json",
)
