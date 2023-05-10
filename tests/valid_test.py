import pytest
import tomllib

import os

from src.parser.grammar import parser,TableArray


BASE_PATH: str = "./valid/"


def json_encode(val):
    if isinstance(val, TableArray):
        return val.l


def parse(content: str) :
    parser.success = True

    result = parser.parse(content)

    if parser.success:
        return result

    else:
        return "Failed to parse content."


class TestValid:

    @staticmethod
    def get_value_and_expected(filename: str, suite_name: str) -> (dict, dict):
        with open(os.path.join(BASE_PATH, suite_name + "/" + filename)) as file:
            file_content: str = file.read()

        output_dict = parse(file_content)
        expected_dict = tomllib.loads(file_content)

        return output_dict, expected_dict

    @pytest.mark.parametrize("filename", filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "array"))))
    def test_array(self, filename: str):
        print(f"Current file: '{filename}'")
        output, expected_content = self.get_value_and_expected(filename, "array")
        assert output == expected_content

    @pytest.mark.parametrize("filename", filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "bool"))))
    def test_bool(self, filename: str):
        print(f"Current file: '{filename}'")
        output, expected_content = self.get_value_and_expected(filename, "bool")
        assert output == expected_content

    @pytest.mark.parametrize("filename", filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "comment"))))
    def test_comment(self, filename: str):
        print(f"Current file: '{filename}'")
        output, expected_content = self.get_value_and_expected(filename, "comment")
        assert output == expected_content

    @pytest.mark.parametrize("filename",
                             filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "datetime"))))
    def test_datetime(self, filename: str):
        print(f"Current file: '{filename}'")
        output, expected_content = self.get_value_and_expected(filename, "datetime")
        assert output == expected_content

    @pytest.mark.parametrize("filename", filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "float"))))
    def test_float(self, filename: str):
        print(f"Current file: '{filename}'")
        output, expected_content = self.get_value_and_expected(filename, "float")
        assert output == expected_content

    @pytest.mark.parametrize("filename",
                             filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "inline-table"))))
    def test_inline_table(self, filename: str):
        print(f"Current file: '{filename}'")
        output, expected_content = self.get_value_and_expected(filename, "inline-table")
        assert output == expected_content

    @pytest.mark.parametrize("filename", filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "integer"))))
    def test_integer(self, filename: str):
        print(f"Current file: '{filename}'")
        output, expected_content = self.get_value_and_expected(filename, "integer")
        assert output == expected_content

    @pytest.mark.parametrize("filename", filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "key"))))
    def test_key(self, filename: str):
        print(f"Current file: '{filename}'")
        output, expected_content = self.get_value_and_expected(filename, "key")
        assert output == expected_content

    @pytest.mark.parametrize("filename", filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "spec"))))
    def test_spec(self, filename: str):
        print(f"Current file: '{filename}'")
        output, expected_content = self.get_value_and_expected(filename, "spec")
        assert output == expected_content

    @pytest.mark.parametrize("filename", filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "string"))))
    def test_string(self, filename: str):
        print(f"Current file: '{filename}'")
        output, expected_content = self.get_value_and_expected(filename, "string")
        assert output == expected_content

    @pytest.mark.parametrize("filename", filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "table"))))
    def test_table(self, filename: str):
        print(f"Current file: '{filename}'")
        output, expected_content = self.get_value_and_expected(filename, "table")
        assert output == expected_content
