import re
import pandas

dot_regex = re.compile("[a-z]{2,4}\.|"
                       "[A-Z][a-z]{0,3}\.|"
                       "([A-Za-z]\.){2,}")

contraction_regex = re.compile("\w+("
                               "'ll|"
                               "n't|"
                               "'re|"
                               "'ve|"
                               "'s|"
                               "'d)$")

en_dash_regex = re.compile("(\d+|"
                           "(January|February|March|April|May|June|July|August|September|October|November|December))"
                           "-"
                            "((January|February|March|April|May|June|July|August|September|October|November|December)"
                           "|\d+)")

geo_list = pandas.read_csv("world-cities.csv", usecols=['name'])


def space_splitter(data):
    splitted_data = data.split()
    return splitted_data


def dot_remover(word):
    if dot_regex.match(word) is not None:
        return word
    else:
        return word[:-1], "."


def geo_names(data):
    for word in range(len(data)):
        try:
            if f"{data[word]} {data[word+1]}" in geo_list:
                data[word] = f"{data[word]} {data[word+1]}"
                data[word + 1].pop()
            elif f"{data[word]} {data[word+1]} {data[word+2]}" in geo_list:
                data[word] = f"{data[word]} {data[word + 1]}"
                data[word + 1].pop()
                data[word + 2].pop()
        except IndexError:
            pass


def contraction_check(word):
    contraction = contraction_regex.findall(word)
    if contraction:
        word = word.replace(contraction, '')
        return word, contraction
    else:
        return word


#if __name__ == "__main__":
