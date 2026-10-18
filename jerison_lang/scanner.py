from jerison_lang.token import Token, TokenType
from jerison_lang.error import error

T = TokenType


class Scanner:
    def __init__(self, source: str) -> None:
        self.__source = source
        self.__tokens: list[Token] = []
        self.__start = 0
        self.__current = 0
        self.__line = 1

    @property
    def tokens(self) -> list[Token]:
        return self.__tokens

    def __advance(self) -> str:
        char = self.__source[self.__current]
        self.__current += 1
        if char == "\n":
            self.__line += 1
        return char

    def __add_token(self, token_type: T, literal: object = None) -> None:
        text = self.__source[self.__start:self.__current]
        self.__tokens.append(Token(token_type, text, literal, self.__line))

    def __match(self, expected: str) -> bool:
        if self.__is_at_end():
            return False
        elif self.__source[self.__current] != expected:
            return False
        self.__current += 1
        return True

    def __scan_token(self) -> None:
        char = self.__advance()
        match char:
            case "(":
                self.__add_token(T.LEFT_PAREN)
            case ")":
                self.__add_token(T.RIGHT_PAREN)
            case "{":
                self.__add_token(T.LEFT_BRACE)
            case "}":
                self.__add_token(T.RIGHT_BRACE)
            case ",":
                self.__add_token(T.COMMA)
            case ".":
                self.__add_token(T.DOT)
            case "-":
                self.__add_token(T.MINUS)
            case "+":
                self.__add_token(T.PLUS)
            case ";":
                self.__add_token(T.SEMICOLON)
            case "*":
                self.__add_token(T.STAR)
            case "!":
                self.__add_token(T.BANG_EQUAL if self.__match("=") else T.BANG)
            case "=":
                self.__add_token(T.EQUAL_EQUAL if self.__match("=") else T.EQUAL)
            case "<":
                self.__add_token(T.LESS_EQUAL if self.__match("=") else T.LESS)
            case ">":
                self.__add_token(T.GREATER_EQUAL if self.__match("=") else T.GREATER)
            case _:
                error(self.__line, "Unexpected character.")

    def __is_at_end(self) -> bool:
        return self.__current >= len(self.__source)

    def scan_tokens(self) -> list[Token]:
        while not self.__is_at_end():
            self.__start = self.__current
            self.__scan_token()
        self.__tokens.append(Token(T.EOF, "", None, self.__line))
        return self.__tokens
