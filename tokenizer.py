from regex import dot_regex, punctuation_regex, contraction_regex, en_dash_regex
import pandas

world_cities = "https://raw.githubusercontent.com/datasets/world-cities/master/data/world-cities.csv"
geo_list = pandas.read_csv(world_cities)['name'].values.tolist()


def space_splitter(data):
    splitted_data = data.split()
    return splitted_data


def dot_remover(word):
    if dot_regex.match(word) is not None:
        return word
    elif word[-1] == ".":
        return word[:-1], "."
    else:
        return word


def punctuation_remover(word):
    punctuation = punctuation_regex.findall(word)
    if punctuation:
        return word.replace(punctuation[0], ""), punctuation[0]
    else:
        return word


def en_dash_remover(word):
    dash = en_dash_regex.match(word)
    if dash is not None:
        split = word.split("-")
        return split[0], "-", split[1]
    else:
        return word


def geo_names(data):
    for word in range(len(data)):
        try:
            if f"{data[word]} {data[word + 1]} {data[word + 2]}" in geo_list:
                data[word] = f"{data[word]} {data[word + 1]} {data[word + 2]}"
                data.pop(word + 2)
                data.pop(word + 1)
            elif f"{data[word]} {data[word+1]}" in geo_list:
                data[word] = f"{data[word]} {data[word+1]}"
                data.pop(word + 1)
        except IndexError:
            pass
    return data


def contraction_check(word):
    contraction = contraction_regex.findall(word)
    if contraction:
        word = word.replace(contraction[0], '')
        return word, contraction[0]
    else:
        return word
