from tokenizer import *
from regex import sentence_end_regex, splitter_regex

import argparse
import sys

def parse_cli():
    cli_parser = argparse.ArgumentParser(
        prog="Tokenizer",
        description="""Tokenizes provided data""",
    )
    cli_group = cli_parser.add_mutually_exclusive_group()

    cli_parser.add_argument("-t", "--tokenize", action="store_true",
                            help="tokenize data, default action")

    cli_parser.add_argument("-s", "--split", action="store_true",
                            help="split data into sentences")

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


def splitter(data, tokenized_data):
    raw_split = splitter_regex.findall(data)
    if raw_split:
        #print(raw_split)
        current_sentence = raw_split.pop(0)
    else:
        return data
    sentence_end = list()
    split_sentences = list()

    for i, token in enumerate(tokenized_data):
        if sentence_end_regex.search(token) is not None:
            sentence_end.append(f"{tokenized_data[i-1]}{token} ")

    while raw_split:
        if sentence_end and current_sentence[-len(sentence_end[0]):] == sentence_end[0]:
            split_sentences.append(current_sentence.rstrip())
            current_sentence = raw_split.pop(0)
            sentence_end.pop(0)
        else:
            current_sentence += raw_split.pop(0)
    if current_sentence != split_sentences[-1]:
        split_sentences.append(current_sentence)
    return split_sentences


if __name__ == "__main__":
    args, helper = parse_cli()
    data = str()

    if args.interactive:
        for line in sys.stdin:
            data += line
    elif args.file:
        with open(args.file, 'r') as input_file:
            data = input_file
    else:
        helper.print_help()

    if data and (args.tokenize or args.split):
        tokenized_data = tokenize(data)

        output = str()
        if args.tokenize:
            output += ("Tokenized data:\n"
                       f"{tokenized_data}\n")
        if args.split:
            split_data = splitter(data, tokenized_data)
            output += ("Split data:\n"
                       f"{split_data}\n")

        if args.output:
            with open(args.output, 'w') as out_file:
                    out_file.write(output)
        else:
            print(output)
    else:
        helper.print_help()