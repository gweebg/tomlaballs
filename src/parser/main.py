import json

from src.parser.grammar import parser
from src.parser.utils import JsonNormalizer


def parse(content: str) -> tuple[str, bool, str]:

    parser.success = True

    result_as_dict: dict = parser.parse(content)
    normalized_result: dict = JsonNormalizer(result_as_dict).normalize()

    print(normalized_result)

    result_as_str: str = json.dumps(normalized_result)

    print("result:", result_as_str)

    if parser.success:
        return result_as_str, True, ""

    else:
        return "", False, "Failed to parse TOML content."

