from src.parser.grammar import parser
from src.parser.utils import JsonNormalizer, toml_file

import argparse


def parse(content: str) -> tuple[str, bool, str]:

    parser.success = True

    result_as_dict: dict = parser.parse(content)
    json: JsonNormalizer = JsonNormalizer(result_as_dict)

    normalized_result: dict = json.normalize()
    result_as_str: str = json.to_json(normalized_result)

    print(result_as_str)

    if parser.success:
        return result_as_str, True, ""

    else:
        return "", False, "Failed to parse TOML content."


def main():

    args: argparse.ArgumentParser = argparse.ArgumentParser(prog="tomalaballs cli",
                                                            description="yet another toml parser",
                                                            epilog="project made by tomlaballs team")

    args.add_argument('-f',
                      '--filename',
                      required=False,
                      type=toml_file,
                      help='parse the content from a toml file')

    args.add_argument('-o',
                      '--output',
                      required=False,
                      help='create a file with the output from parsing, only works if a file is provided')

    args: argparse.Namespace = args.parse_args()

    if args.filename and args.output:

        with open(args.output, 'w') as out:

            with open(args.filename) as inp:
                content: str = inp.read()

            parse_result: tuple[str, bool, str] = parse(content)

            if parse_result[1]:
                out.write(parse_result[0])

            else:
                out.write(parse_result[2])

    elif args.filename:

        with open(args.filename) as inp:
            content: str = inp.read()

        parse_result: tuple[str, bool, str] = parse(content)

        if parse_result[1]:
            print(parse_result[0])

        else:
            print(parse_result[2])


if __name__ == "__main__":
    SystemExit(main())