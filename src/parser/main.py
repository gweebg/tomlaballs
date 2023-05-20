from src.parser.grammar import parser
from src.parser.utils import JsonNormalizer


def parse(content: str) -> tuple[str, bool, str]:

    parser.success = True

    result_as_dict: dict = parser.parse(content)
    json: JsonNormalizer = JsonNormalizer(result_as_dict)

    normalized_result: dict = json.normalize()
    result_as_str: str = json.to_json(normalized_result)

    print(result_as_dict)

    if parser.success:
        return result_as_str, True, ""

    else:
        return "", False, "Failed to parse TOML content."


if __name__ == '__main__':

    content: str = """..."""
    parse(content)