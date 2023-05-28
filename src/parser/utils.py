import argparse
from enum import Enum
from datetime import datetime, time, date


def to_bool(token: str) -> bool:
    if token == 'true':
        return True

    if token == 'false':
        return False


class DateType(Enum):
    OFFSET_DATETIME = 1
    LOCAL_DATETIME = 2
    LOCAL_DATE = 3
    LOCAL_TIME = 4


class DateValidator:

    def __init__(self, token: str, date_type: DateType) -> None:

        self.token: str = token
        self.type: DateType = date_type

        self.formats: dict[DateType, list[str]] = {

            DateType.OFFSET_DATETIME: [
                '%Y-%m-%dT%H:%M:%S%z',
                '%Y-%m-%dT%H:%M:%S.%f%z',
                '%Y-%m-%dT%H:%M%z',
                '%Y-%m-%d %H:%M:%S.%f%z',
                '%Y-%m-%d %H:%M:%S%z',
                '%Y-%m-%d %H:%M%z'
            ],

            DateType.LOCAL_DATETIME: [
                '%Y-%m-%dT%H:%M',
                '%Y-%m-%dT%H:%M:%S.%f',
                '%Y-%m-%dT%H:%M:%S',
                '%Y-%m-%d %H:%M:%S%z',
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d %H:%M'
            ],

            DateType.LOCAL_DATE: ['%Y-%m-%d'],

            DateType.LOCAL_TIME: [
                '%H:%M:%S.%f',
                '%H:%M:%S',
                '%H:%M'
            ]

        }

    def validate(self) -> tuple[bool, str]:

        formats: list[str] = self.formats.get(self.type)

        valid: bool = False
        for fmt in formats:

            try:
                datetime.strptime(self.token, fmt)
                valid = True
                return valid, fmt

            except ValueError:
                pass

        return valid, ""

    @staticmethod
    def normalize(value: str, formatted_as: str, date_type: DateType) -> time | datetime | date:

        if date_type == DateType.LOCAL_TIME:
            return datetime.strptime(value, formatted_as).time()

        if date_type == DateType.LOCAL_DATE:
            return datetime.strptime(value, formatted_as).date()

        return datetime.strptime(value, formatted_as)


class TableArray(list):
    def __init__(self) -> None:
        super().__init__()

    def get_last(self):
        return self[len(self) - 1]


class Table(dict):
    is_locked = False

    def __init__(self):
        super().__init__()


class JsonNormalizer:

    def __init__(self, toml_dict: dict):
        self.dict: dict = toml_dict
        self.__normalized: dict = {}
        self.json: str = ""

    def normalize(self) -> dict:

        if not self.dict:
            return {}

        self.__normalized = self.dict
        stack: list[dict] = [self.__normalized]

        while stack:

            current_dict: dict = stack.pop()

            for (key, value) in current_dict.items():

                if isinstance(value, dict):
                    stack.append(value)

                elif isinstance(value, datetime | time | date):
                    current_dict[key] = str(value)

                else:
                    current_dict[key] = value

        return self.__normalized

    def to_json(self, dictionary: dict) -> str:

        json_string: str = "{"

        for key, value in dictionary.items():

            json_string += f'"{key}": '

            if isinstance(value, dict):
                json_string += self.to_json(value)  # Run recursively if encounters another dict.

            elif isinstance(value, str):
                json_string += f'"{value}"'  # Append value if it is a string.

            elif isinstance(value, bool):
                json_string += f'{str(value).lower()}'  # Convert boolean to lowecase string.

            else:
                json_string += str(value).replace("'", '"')  # Convert to string and replace quotation marks.

            json_string += ","

        if len(dictionary) > 0:
            json_string = json_string[:-1]  # Remove the trailing comma.

        return json_string + "}"


def toml_file(astring: str) -> str:

    if not astring.endswith('.toml'):
        raise argparse.ArgumentTypeError

    return astring
