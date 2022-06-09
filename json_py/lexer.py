from __future__ import annotations
import typing


TypeLexer = typing.Tuple[typing.Optional[typing.Any], str]


def lex_string(string: str) -> TypeLexer:
    if not string.startswith('"'):
        return None, string

    string = string[1:]
    for i in range(len(string)):
        if string[i] == '"':
            return string[:i], string[i + 1 :]

    return None, string


def lex_number(string: str) -> TypeLexer:
    if not string[0].isdigit():
        return None, string

    has_decimal = False

    for i in range(len(string)):
        if string[i] == ".":
            if has_decimal:
                raise ValueError("Invalid number")

            has_decimal = True
            continue

        if not string[i].isdigit():
            if has_decimal:
                return float(string[:i]), string[i:]
            return int(string[:i]), string[i:]

    if has_decimal:
        return float(string), ""
    return int(string), ""


def lex_bool(string: str) -> TypeLexer:
    if string[0].lower() not in "tf":
        return None, string

    if string[:4].lower() == "true":
        return True, string[4:]
    elif string[:5].lower() == "false":
        return False, string[5:]

    return None, string


def lex_null(string: str) -> TypeLexer:
    if string[:4].lower() == "null":
        return True, string[4:]

    return None, string


TokenList = typing.List[typing.Any]


def lex(string: str) -> TokenList:
    tokens: TokenList = []
    while len(string) > 0:
        json_string, string = lex_string(string)
        if json_string is not None:
            tokens.append(json_string)
            continue

        json_number, string = lex_number(string)
        if json_number is not None:
            tokens.append(json_number)
            continue

        json_bool, string = lex_bool(string)
        if json_bool is not None:
            tokens.append(json_bool)
            continue

        json_null, string = lex_null(string)
        if json_null is not None:
            tokens.append(None)
            continue

        if string[0] in " ":
            string = string[1:]
        elif string[0] in ":{},[]":
            tokens.append(string[0])
            string = string[1:]
        else:
            raise Exception("Unexpected character: {}".format(string[0]))

    return tokens
