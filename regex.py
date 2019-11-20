import re

dot_regex = re.compile(r"[a-z]{2,3}\.|"
                       r"[A-Z][a-z]{0,3}\.|"
                       r"([A-Za-z]\.){2,}")

punctuation_regex = re.compile(r"\w+([\-,\[\]:;\"?!]+|\.\.\.)$")

contraction_regex = re.compile(r"\w+("
                               r"'ll|"
                               r"n't|"
                               r"'re|"
                               r"'ve|"
                               r"'s|"
                               r"'d)$")

en_dash_regex = re.compile(r"(\d+|"
                           r"(January|February|March|April|May|June|July|August|September|October|November|December))"
                           r"-"
                           r"((January|February|March|April|May|June|July|August|September|October|November|December)"
                           r"|\d+)")

sentence_end_regex = re.compile(r"^[\.!?]+$")

splitter_regex = re.compile(r".*?[?\.!]+\s|.*?$")