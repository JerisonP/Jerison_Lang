from jerison_lang.token import Token, TokenType

T = TokenType


class Scanner:
    def __init__(self, source: str) -> None:
        self.__source = source
        self.__tokens: list[Token] = []

    @property
    def tokens(self) -> list[Token]:
        return self.__tokens

    def __add_token(self, token_type: T, text: str, line: int) -> None:
        lexeme = text
        literal = literal_value(token_type, text)
        self.__tokens.append(Token(token_type, lexeme, literal, line))

    def __scan_token(self, text: str, line: int) -> None:
        token_type = classify_token(text)
        self.__add_token(token_type, text, line)

    def scan_tokens(self) -> list[Token]:
        line = 1
        text = ""
        for char in self.__source:
            if not char.isspace():
                text += char
            if char == "\n":
                line += 1
                text = ""
            try:
                self.__scan_token(text, line)
                text = ""
            except ValueError:
                pass
        self.__tokens.append(Token(T.EOF, "", None, line))
        return self.tokens


def literal_value(token_type: T, text: str) -> object:
    match token_type:
        case T.STRING:
            return text
        case T.NUMBER:
            return float(text)
        case _:
            return None


def classify_token(text: str) -> T:
    match text:
        case "(":
            return T.LEFT_PAREN
        case ")":
            return T.RIGHT_PAREN
        case "{":
            return T.LEFT_BRACE
        case "}":
            return T.RIGHT_BRACE
        case ",":
            return T.COMMA
        case ".":
            return T.DOT
        case "-":
            return T.MINUS
        case "+":
            return T.PLUS
        case ";":
            return T.SEMICOLON
        case "*":
            return T.STAR
        case _:
            raise ValueError("must be a valid token")
