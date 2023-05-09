from enum import Enum
from datetime import datetime


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
    def normalize(value: str, formatted_as: str, date_type: DateType) -> str:

        if date_type == DateType.LOCAL_TIME:
            return str(datetime.strptime(value, formatted_as).time())

        return str(datetime.strptime(value, formatted_as))