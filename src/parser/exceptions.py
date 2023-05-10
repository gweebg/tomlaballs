from ply.lex import LexToken


class InvalidDatetimeFormat(Exception):

    def __init__(self, token: LexToken):
        error_message: str = f"Invalid {token.type} format:{token.lexer.lineno}:{token.lexpos}::{token.value}"
        super().__init__(error_message)


class IllegalCharacterException(Exception):

    def __init__(self, char: str):
        error_message: str = f"Invalid character '{char}'"
        super().__init__(error_message)


class UnexcapedBackslashException(Exception):

    def __init__(self, error_message: str):
        super().__init__(error_message)
