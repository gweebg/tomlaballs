import pytest

import os

from src.parser.grammar import parser


BASE_PATH: str = "./invalid/"


def parse(content: str):

    parser.success = True
    result = parser.parse(content)

    if not parser.success:
        raise Exception("Failed to parse content.")

    return result


class TestInvalid:

    @staticmethod
    def get_value(filename: str, suite_name: str) -> (dict, dict):

        with open(os.path.join(BASE_PATH, suite_name + "/" + filename)) as file:
            file_content: str = file.read()

        output_dict: dict = parse(file_content)
        return output_dict

    @pytest.mark.parametrize("filename", filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "array"))))
    def test_array(self, filename: str):
        print(f"Current file: '{filename}'")
        with pytest.raises(Exception):
            self.get_value(filename, "array")

    @pytest.mark.parametrize("filename", filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "bool"))))
    def test_bool(self, filename: str):
        print(f"Current file: '{filename}'")
        with pytest.raises(Exception):
            self.get_value(filename, "bool")

    @pytest.mark.parametrize("filename", filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "control"))))
    def test_control(self, filename: str):
        print(f"Current file: '{filename}'")
        with pytest.raises(Exception):
            self.get_value(filename, "control")

    @pytest.mark.parametrize("filename",
                             filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "datetime"))))
    def test_datetime(self, filename: str):
        print(f"Current file: '{filename}'")
        with pytest.raises(Exception):
            self.get_value(filename, "datetime")

    @pytest.mark.parametrize("filename", filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "float"))))
    def test_float(self, filename: str):
        print(f"Current file: '{filename}'")
        with pytest.raises(Exception):
            self.get_value(filename, "float")

    @pytest.mark.parametrize("filename",
                             filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "inline-table"))))
    def test_inline_table(self, filename: str):
        print(f"Current file: '{filename}'")
        with pytest.raises(Exception):
            self.get_value(filename, "inline-table")

    @pytest.mark.parametrize("filename", filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "integer"))))
    def test_integer(self, filename: str):
        print(f"Current file: '{filename}'")
        with pytest.raises(Exception):
            self.get_value(filename, "integer")

    @pytest.mark.parametrize("filename", filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "key"))))
    def test_key(self, filename: str):
        print(f"Current file: '{filename}'")
        with pytest.raises(Exception):
            self.get_value(filename, "key")

    @pytest.mark.parametrize("filename", filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "spec"))))
    def test_spec(self, filename: str):
        print(f"Current file: '{filename}'")
        with pytest.raises(Exception):
            self.get_value(filename, "spec")

    @pytest.mark.parametrize("filename", filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "string"))))
    def test_string(self, filename: str):
        print(f"Current file: '{filename}'")
        with pytest.raises(Exception):
            self.get_value(filename, "string")

    @pytest.mark.parametrize("filename", filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "table"))))
    def test_table(self, filename: str):
        print(f"Current file: '{filename}'")
        with pytest.raises(Exception):
            self.get_value(filename, "table")

