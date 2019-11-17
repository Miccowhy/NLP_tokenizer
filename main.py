from tokenizer import *

import argparse


def parse_cli():
    cli_parser = argparse.ArgumentParser(
        prog="Tokenizer",
        description="""Tokenizes provided data""",
    )
    cli_group = cli_parser.add_mutually_exclusive_group()
    cli_parser.add_argument("-o", "--output",
                            help="path to the output file")

    cli_group.add_argument("-i", "--interactive", action="store_true",
                           help="use program in interactive mode")

    cli_group.add_argument("-f", "--file",
                           help="path to the input file")
    return cli_parser.parse_args()


def tokenize(data):
    splitted = space_splitter(data)
    print(splitted)
    #geo_data = geo_names(splitted)

    undotted = list()
    for word in splitted:
        if isinstance(word, tuple):
            [undotted.append(sub) for sub in dot_remover(word)]
        else:
            undotted.append(dot_remover(word))
    print(undotted)

    tokenized_data = list()
    for word in undotted:
        if isinstance(word, tuple):
            [tokenized_data.append(sub) for sub in contraction_check(word)]
        else:
            tokenized_data.append(contraction_check(word))
    print(tokenized_data)

    return tokenized_data


if __name__ == "__main__":
    args = parse_cli()
    data = None

    if args.interactive:
        data = input()
    elif args.file:
        with open(args.file, 'r') as input_file:
            data = input_file
    else:
        data = input()

    if data is not None:
        tokenized_data = tokenize(data)

        if args.output:
            with open(args.output, 'w') as out_file:
                out_file.write(tokenized_data)
        else:
            print(tokenized_data)