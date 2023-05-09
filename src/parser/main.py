import json

from src.parser.grammar import parser


def parse(content: str) -> tuple[str, bool, str]:

    parser.success = True
    result = parser.parse(content)

    if parser.success:
        return json.dumps(result, default=str), True, ""

    else:
        return "", False, "Failed to parse TOML content."

