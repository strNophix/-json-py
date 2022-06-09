from __future__ import annotations
import typing
import json_py.lexer as lexer

ParserResult = typing.Tuple[typing.Any, lexer.TokenList]


def parse_array(tokens: lexer.TokenList) -> ParserResult:
    json_array: typing.List[typing.Any] = []

    if tokens[0] == "]":
        return json_array, tokens[1:]

    expect_comma = False
    for i in range(len(tokens)):
        t = tokens[i]
        if t == "]":
            if not expect_comma:
                raise ValueError("Expected one more item")

            return json_array, tokens[i + 1 :]
        elif t == ",":
            if not expect_comma:
                raise ValueError("Unexpected comma")

            expect_comma = False
        else:
            if expect_comma:
                raise ValueError("Expected comma but got item")

            json_array.append(t)
            expect_comma = True

    raise ValueError("List not closed")


def parse_object(tokens: lexer.TokenList) -> ParserResult:
    json_object: typing.Any = {}

    if tokens[0] == "}":
        return json_object, tokens[1:]

    is_syntax: typing.Callable[[str], bool] = lambda x: str(x) in ":"
    while True:
        json_key = tokens[0]

        if is_syntax(json_key):
            raise Exception(f"Expected value before '{json_key}'")

        colon = tokens[1]
        if colon != ":":
            raise Exception(f"Expected ':' but got '{colon}'")

        json_value, tokens = parse(tokens[2:])
        json_object[json_key] = json_value

        next_token = tokens[0]
        if next_token == ",":
            tokens = tokens[1:]
        elif next_token == "}":
            return json_object, tokens[1:]
        else:
            raise Exception(f"Expected ',' or '{'}'}' but got '{next_token}'")


def parse(tokens: lexer.TokenList) -> typing.Any:
    t = tokens[0]
    if t == "[":
        return parse_array(tokens[1:])
    elif t == "{":
        return parse_object(tokens[1:])
    else:
        return t, tokens[1:]
