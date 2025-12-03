#################chapter 8

text = "The oneperfectly divine thing, the oneglimpse of God's paradisegiven on earth, is to fight a losingbattle - and notlose it."

word_list = ['The', 'one', 'perfectly', 'divine']

word_list_copy = [word for word in word_list]

has_n = [word for word in word_list if 'n' in word]

import re

locs = list(set([(m.start(), m.end()) for word in word_list for m in re.finditer(word, text)]))

spacestarts = [m.start() for m in re.finditer(' ', text)]
spacestarts.append(-1)
spacestarts.append(len(text))
spacestarts.sort()

spacestarts_affine = [ss + 1 for ss in spacestarts]
spacestarts_affine.sort()

between_spaces = [(spacestarts[k] + 1, spacestarts[k + 1]) for k in range(0, len(spacestarts) - 1)]

between_spaces_notvalid = [loc for loc in between_spaces if \
                           text[loc[0]:loc[1]] not in word_list]

import nltk

nltk.download('brown')

from nltk.corpus import brown

wordlist = set(brown.words())
word_list = list(wordlist)

word_list = [word.replace('*', '') for word in word_list]
word_list = [word.replace('[', '') for word in word_list]
word_list = [word.replace(']', '') for word in word_list]
word_list = [word.replace('?', '') for word in word_list]
word_list = [word.replace('.', '') for word in word_list]
word_list = [word.replace('+', '') for word in word_list]
word_list = [word.replace('/', '') for word in word_list]
word_list = [word.replace(';', '') for word in word_list]
word_list = [word.replace(':', '') for word in word_list]
word_list = [word.replace(',', '') for word in word_list]
word_list = [word.replace(')', '') for word in word_list]
word_list = [word.replace('(', '') for word in word_list]
word_list.remove('')

between_spaces_notvalid = [loc for loc in between_spaces if \
                           text[loc[0]:loc[1]] not in word_list]

partial_words = [loc for loc in locs if loc[0] in spacestarts_affine and \
                 loc[1] not in spacestarts]

partial_words_end = [loc for loc in locs if loc[0] not in spacestarts_affine \
                     and loc[1] in spacestarts]

loc = between_spaces_notvalid[0]

endsofbeginnings = [loc2[1] for loc2 in partial_words if loc2[0] == loc[0] \
                    and (loc2[1] - loc[0]) > 1]

beginningsofends = [loc2[0] for loc2 in partial_words_end if loc2[1] == loc[1] and \
                    (loc2[1] - loc[0]) > 1]

pivot = list(set(endsofbeginnings).intersection(beginningsofends))

import numpy as np

pivot = np.min(pivot)

textnew = text
textnew = textnew.replace(text[loc[0]:loc[1]], text[loc[0]:pivot] + ' ' + text[pivot:loc[1]])


def insertspaces(text, word_list):
    locs = list(set([(m.start(), m.end()) for word in word_list for m in re.finditer(word, \
                                                                                     text)]))
    spacestarts = [m.start() for m in re.finditer(' ', text)]
    spacestarts.append(-1)
    spacestarts.append(len(text))
    spacestarts.sort()
    spacestarts_affine = [ss + 1 for ss in spacestarts]
    spacestarts_affine.sort()
    partial_words = [loc for loc in locs if loc[0] in spacestarts_affine and loc[1] not in \
                     spacestarts]
    partial_words_end = [loc for loc in locs if loc[0] not in spacestarts_affine and loc[1] \
                         in spacestarts]
    between_spaces = [(spacestarts[k] + 1, spacestarts[k + 1]) for k in \
                      range(0, len(spacestarts) - 1)]
    between_spaces_notvalid = [loc for loc in between_spaces if text[loc[0]:loc[1]] not in \
                               word_list]
    textnew = text
    for loc in between_spaces_notvalid:
        endsofbeginnings = [loc2[1] for loc2 in partial_words if loc2[0] == loc[0] and \
                            (loc2[1] - loc[0]) > 1]
        beginningsofends = [loc2[0] for loc2 in partial_words_end if loc2[1] == loc[1] and \
                            (loc2[1] - loc[0]) > 1]
        pivot = list(set(endsofbeginnings).intersection(beginningsofends))
        if (len(pivot) > 0):
            pivot = np.min(pivot)
            textnew = textnew.replace(text[loc[0]:loc[1]], text[loc[0]:pivot] + ' ' + text[pivot:loc[1]])
    textnew = textnew.replace(' ', ' ')
    return (textnew)


text = "The oneperfectly divine thing, the oneglimpse of God's paradisegiven on earth, is to fight a losingbattle - and notlose it."
print(insertspaces(text, word_list))

nltk.download('punkt')

from nltk.tokenize import sent_tokenize, word_tokenize

text = "Time forks perpetually toward innumerable futures"
print(word_tokenize(text))

import nltk
from nltk.util import ngrams

token = nltk.word_tokenize(text)
bigrams = ngrams(token, 2)
trigrams = ngrams(token, 3)
fourgrams = ngrams(token, 4)
fivegrams = ngrams(token, 5)

grams = [ngrams(token, 2), ngrams(token, 3), ngrams(token, 4), ngrams(token, 5)]

import requests

file = requests.get('http://www.bradfordtuckfield.com/shakespeare.txt')
file = file.text
text = file.replace('\n', '')

token = nltk.word_tokenize(text)
bigrams = ngrams(token, 2)
trigrams = ngrams(token, 3)
fourgrams = ngrams(token, 4)
fivegrams = ngrams(token, 5)
grams = [ngrams(token, 2), ngrams(token, 3), ngrams(token, 4), ngrams(token, 5)]

search_term = 'life is a'
split_term = tuple(search_term.split(' '))
search_term_length = len(search_term.split(' '))

from collections import Counter

counted_grams = Counter(grams[search_term_length - 1])

print(list(counted_grams.items())[0])

matching_terms = [element for element in list(counted_grams.items()) if \
                  element[0][:-1] == tuple(split_term)]

if (len(matching_terms) > 0):
    frequencies = [item[1] for item in matching_terms]
    maximum_frequency = np.max(frequencies)
    highest_frequency_term = [item[0] for item in matching_terms if item[1] == \
                              maximum_frequency][0]
    combined_term = ' '.join(highest_frequency_term)


def search_suggestion(search_term, text):
    token = nltk.word_tokenize(text)
    bigrams = ngrams(token, 2)
    trigrams = ngrams(token, 3)
    fourgrams = ngrams(token, 4)
    fivegrams = ngrams(token, 5)
    grams = [ngrams(token, 2), ngrams(token, 3), ngrams(token, 4), ngrams(token, 5)]
    split_term = tuple(search_term.split(' '))
    search_term_length = len(search_term.split(' '))
    counted_grams = Counter(grams[search_term_length - 1])
    combined_term = 'No suggested searches'
    matching_terms = [element for element in list(counted_grams.items()) if \
                      element[0][:-1] == tuple(split_term)]
    if (len(matching_terms) > 0):
        frequencies = [item[1] for item in matching_terms]
        maximum_frequency = np.max(frequencies)
        highest_frequency_term = [item[0] for item in matching_terms if item[1] == \
                                  maximum_frequency][0]
        combined_term = ' '.join(highest_frequency_term)
    return (combined_term)


file = requests.get('http://www.bradfordtuckfield.com/shakespeare.txt')
file = file = file.text
text = file.replace('\n', '')
print(search_suggestion('life is a', text))

file = requests.get('http://www.bradfordtuckfield.com/marktwain.txt')
file = file = file.text
text = file.replace('\n', '')

print(search_suggestion('life is a', text))
