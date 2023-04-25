import sys

sys.path.insert(1, '../src')

from sint import parser

import pytest

import os
import json

from datetime import date, datetime


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


BASE_PATH: str = "./invalid/"


def parse(content: str):
    parser.success = True

    #try:
    result = parser.parse(content)
    #except:
    #    return "Failed to parse content."


    if parser.success:
        return json.dumps(result, default=json_serial)

    else:
        return "Failed to parse content."


class TestValid:

    @staticmethod
    def get_value_and_expected(filename: str, suite_name: str) -> (str):
        with open(os.path.join(BASE_PATH, suite_name + "/" + filename)) as file:
            file_content: str = file.read()

        output: str = parse(file_content)

        return output
    
    # TODO: fix illegal characters, datetime e o resto já agora :)

    @pytest.mark.parametrize("filename", filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "array"))))
    def test_array(self, filename: str):
        print(f"Current file: '{filename}'")
        output = self.get_value_and_expected(filename, "array")
        assert output == "Failed to parse content."
    
    @pytest.mark.parametrize("filename", filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "bool"))))
    def test_bool(self, filename: str):
        print(f"Current file: '{filename}'")
        output = self.get_value_and_expected(filename, "bool")
        assert output == "Failed to parse content."

    @pytest.mark.parametrize("filename", filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "control"))))
    def test_control(self, filename: str):
        print(f"Current file: '{filename}'")
        output = self.get_value_and_expected(filename, "control")
        assert output == "Failed to parse content."

        
    @pytest.mark.parametrize("filename", filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "datetime"))))
    def test_datetime(self, filename: str):
        print(f"Current file: '{filename}'")
        output = self.get_value_and_expected(filename, "datetime")
        assert output == "Failed to parse content."

    @pytest.mark.parametrize("filename", filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "encoding"))))
    def test_encoding(self, filename: str):
        print(f"Current file: '{filename}'")
        output = self.get_value_and_expected(filename, "encoding")
        assert output == "Failed to parse content."

    @pytest.mark.parametrize("filename", filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "float"))))
    def test_float(self, filename: str):
        print(f"Current file: '{filename}'")
        output = self.get_value_and_expected(filename, "float")
        assert output == "Failed to parse content."

    @pytest.mark.parametrize("filename", filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "inline-table"))))
    def test_inline_table(self, filename: str):
        print(f"Current file: '{filename}'")
        output = self.get_value_and_expected(filename, "inline-table")
        assert output == "Failed to parse content."
 
    @pytest.mark.parametrize("filename", filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "integer"))))
    def test_integer(self, filename: str):
        print(f"Current file: '{filename}'")
        output = self.get_value_and_expected(filename, "integer")
        assert output == "Failed to parse content."

    @pytest.mark.parametrize("filename", filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "key"))))
    def test_key(self, filename: str):
        print(f"Current file: '{filename}'")
        output = self.get_value_and_expected(filename, "key")
        assert output == "Failed to parse content."
    
    @pytest.mark.parametrize("filename", filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "spec"))))
    def test_spec(self, filename: str):
        print(f"Current file: '{filename}'")
        output = self.get_value_and_expected(filename, "spec")
        assert output == "Failed to parse content."

    @pytest.mark.parametrize("filename", filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "string"))))
    def test_string(self, filename: str):
        print(f"Current file: '{filename}'")
        output = self.get_value_and_expected(filename, "string")
        assert output == "Failed to parse content."

    @pytest.mark.parametrize("filename", filter(lambda f: f.endswith(".toml"), list(os.listdir(BASE_PATH + "table"))))
    def test_table(self, filename: str):
        print(f"Current file: '{filename}'")
        output = self.get_value_and_expected(filename, "table")
        assert output == "Failed to parse content."


