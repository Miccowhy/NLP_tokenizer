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
    return cli_parser.parse_args(), cli_parser


def tokenize(data):
    split = space_splitter(data)
    print(f"Split: {split}")

    undotted = list()
    #for word in splitted:
    for word in split:
        checked = dot_remover(word)
        if isinstance(checked, tuple):
            [undotted.append(subword) for subword in checked]
        else:
            undotted.append(dot_remover(word))
    #print(f"Undotted: {undotted}")

    decontractioned = list()
    for word in undotted:
        checked = contraction_check(word)
        if isinstance(checked, tuple):
            [decontractioned.append(subword) for subword in checked]
        else:
            decontractioned.append(checked)
    #print(f"Deco: {decontractioned}")

    punctuation = list()
    for word in decontractioned:
        checked = punctuation_remover(word)
        if isinstance(checked, tuple):
            [punctuation.append(subword) for subword in checked]
        else:
            punctuation.append(checked)
    #print(f"Punc: {punctuation}")

    undashed = list()
    for word in punctuation:
        checked = en_dash_remover(word)
        if isinstance(checked, tuple):
            [undashed.append(subword) for subword in checked]
        else:
            undashed.append(checked)
    #print(f"Undashed: {undashed}")

    tokenized_data = geo_names(undashed)

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
        #helper.print_help()
        data = input()

    if data is not None:
        tokenized_data = tokenize(data)

        if args.output:
            with open(args.output, 'w') as out_file:
                out_file.write(tokenized_data)
        else:
            print(tokenized_data)