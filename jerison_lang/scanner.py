from jerison_lang.error import error
from jerison_lang.token import Token, TokenType

T = TokenType


class Scanner:
    keywords = {
        "and": T.AND,
        "class": T.CLASS,
        "else": T.ELSE,
        "false": T.FALSE,
        "for": T.FOR,
        "fun": T.FUN,
        "if": T.IF,
        "nil": T.NIL,
        "or": T.OR,
        "print": T.PRINT,
        "return": T.RETURN,
        "super": T.SUPER,
        "this": T.THIS,
        "true": T.TRUE,
        "var": T.VAR,
        "while": T.WHILE,
    }

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
        return char

    def __add_token(self, token_type: T, literal: object = None) -> None:
        text = self.__source[self.__start:self.__current]
        self.__tokens.append(Token(token_type, text, literal, self.__line))

    def __match(self, expected: str) -> bool:
        if self.__is_at_end() or self.__source[self.__current] != expected:
            return False
        self.__current += 1
        return True

    def __peek(self) -> str | None:
        if self.__is_at_end():
            return None
        return self.__source[self.__current]

    def __is_digit(self, char: str | None) -> bool:
        if not char:
            return False
        return char in "0123456789"

    def __peek_next(self) -> str | None:
        if self.__current + 1 >= len(self.__source):
            return  None 
        return self.__source[self.__current + 1]

    def __string(self) -> None:
        while self.__peek() != "\"" and not self.__is_at_end():
            if self.__peek() == "\n":
                self.__line += 1
            self.__advance()

        if self.__is_at_end():
            error(self.__line, "Unterminated string.")
            return 

        self.__advance()

        value = self.__source[self.__start + 1:self.__current - 1]
        self.__add_token(T.STRING, value)  

    def __number(self) -> None:
        while self.__is_digit(self.__peek()):
            self.__advance()

        if self.__peek() == "." and self.__is_digit(self.__peek_next()):
            self.__advance()

        while self.__is_digit(self.__peek()):
            self.__advance()

        self.__add_token(T.NUMBER, float(self.__source[self.__start:self.__current]))

    def __is_alpha(self, char: str | None) -> bool:
        if not char:
            return False
        return char.isalpha() or char == "_"

    def __is_alnum(self, char: str | None) -> bool:
        return self.__is_alpha(char) or self.__is_digit(char)

    def __identifier(self) -> None:
        while self.__is_alnum(self.__peek()):
            self.__advance()
        text = self.__source[self.__start: self.__current]
        token_type = Scanner.keywords.get(text, T.IDENTIFIER)
        self.__add_token(token_type)
    
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
            case "/":
                if self.__match("/"):
                    while self.__peek() != "\n" and not self.__is_at_end():
                        self.__advance()
                else:
                    self.__add_token(T.SLASH)
            case " ":
                pass
            case "\r":
                pass
            case "\t":
                pass
            case "\n":
                self.__line += 1
            case "\"":
                self.__string()
            case _:
                if self.__is_digit(char):
                    self.__number()
                elif self.__is_alpha(char):
                    self.__identifier()
                error(self.__line, "Unexpected character.")

    def __is_at_end(self) -> bool:
        return self.__current >= len(self.__source)

    def scan_tokens(self) -> list[Token]:
        while not self.__is_at_end():
            self.__start = self.__current
            self.__scan_token()
        self.__tokens.append(Token(T.EOF, "", None, self.__line))
        return self.__tokens
