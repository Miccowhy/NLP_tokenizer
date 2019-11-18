from tokenizer import *

import argparse


def parse_cli():
    cli_parser = argparse.ArgumentParser(
        prog="Tokenizer",
        description="""Tokenizes provided data""",
    )
    cli_group = cli_parser.add_mutually_exclusive_group()

    cli_group.add_argument("-i", "--interactive", action="store_true",
                           help="use program in interactive mode")

    cli_group.add_argument("-f", "--file",
                           help="path to the input file")

    cli_parser.add_argument("-o", "--output",
                            help="path to the output file")

    return cli_parser.parse_args(), cli_parser


def functionify(data, passed_function):
    unnested_data = list()
    for word in data:
        checked_word = passed_function(word)
        if isinstance(checked_word, tuple):
            [unnested_data.append(subword) for subword in checked_word]
        else:
            unnested_data.append(checked_word)
    return unnested_data


def tokenize(data):
    processed_data = space_splitter(data)

    for function in (dot_remover, contraction_check, punctuation_remover, en_dash_remover):
        processed_data = functionify(processed_data, function)

    tokenized_data = geo_names(processed_data)

    return tokenized_data


if __name__ == "__main__":
    args, helper = parse_cli()
    data = None

    if args.interactive:
        data = input()
    elif args.file:
        with open(args.file, 'r') as input_file:
            data = input_file
    else:
        helper.print_help()

    if data is not None:
        tokenized_data = tokenize(data)

        if args.output:
            with open(args.output, 'w') as out_file:
                out_file.write(tokenized_data)
        else:
            print(tokenized_data)
