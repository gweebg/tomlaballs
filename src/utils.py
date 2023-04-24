from enum import Enum
from datetime import datetime


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

            DateType.OFFSET_DATETIME: ['%Y-%m-%dT%H:%M:%SZ',
                                       '%Y-%m-%dT%H:%M:%S%z',
                                       '%Y-%m-%dT%H:%M:%S.%f%z',
                                       '%Y-%m-%d %H:%M:%SZ'],

            DateType.LOCAL_DATETIME: ['%Y-%m-%dT%H:%M:%S.%f%z',
                                      '%Y-%m-%dT%H:%M:%S.%f',
                                      '%Y-%m-%dT%H:%M:%SZ',
                                      '%Y-%m-%dT%H:%M:%S'],

            DateType.LOCAL_DATE: ['%Y-%m-%d'],
            DateType.LOCAL_TIME: ['%H:%M:%S.%f', '%H:%M:%S']

        }

    def validate(self) -> bool:

        formats: list[str] = self.formats.get(self.type)

        valid: bool = False
        for fmt in formats:

            try:
                datetime.strptime(self.token, fmt)
                valid = True
                break

            except ValueError:
                pass

        return valid

"""
if __name__ == '__main__':

    dates = [
        ("1979-05-27T07:32:00Z", DateType.OFFSET_DATETIME),
        ("1979-05-27T00:32:00-07:00", DateType.OFFSET_DATETIME),
        ("1979-05-27T00:32:00.999999-07:00", DateType.OFFSET_DATETIME),
        ("1979-05-27 07:32:00Z", DateType.OFFSET_DATETIME),
        ("1979-05-27T07:32:00", DateType.LOCAL_DATETIME),  #
        ("1979-05-27T00:32:00.999999", DateType.LOCAL_DATETIME),
        ("1979-05-27", DateType.LOCAL_DATE),
        ("07:32:00", DateType.LOCAL_TIME),
        ("00:32:00.999999", DateType.LOCAL_TIME)
    ]

    for date in dates:
        print(DateValidator(date[0], date[1]).validate())
"""
