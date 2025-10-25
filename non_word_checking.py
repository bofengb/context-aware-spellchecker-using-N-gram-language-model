"""
References:
    https://github.com/AshwiniRangnekar/GrammaticalErrorDetection-Correction
    https://github.com/troublemeeter/spelling-correction
    https://github.com/NethumL/pyqt-spellcheck
"""

import re
import sys
import math
import glob
import string

from typing import List, Dict, Tuple
from collections import OrderedDict
from operator import itemgetter

import numpy as np


"""
Part 1: Tokenization
"""
def remove_punctuations(text: str):
    """
    Remove the punctuation marks, special symbols from the tokens.
    """
    punct = ["[", "]", "'s", "(", ")", "!", "\"", "%", "$", "*", "&", "^", "=", "+", "`", "'", ","]
    for x in punct:
        text = text.replace(x, '')

    for x in text:
        if x.isdigit():
            text = text.replace(x, '')

    text = text.replace("\n\n", ". ")
    text = text.replace(".\n\n", ". ")
    text = text.replace("..", ".")

    p = [":--", "-", "\n", "  ", "_", ",", ";", ":", "?", "/", "{", "}"]
    for pp in p:
        text = text.replace(pp, ' ')
    return text


def tokenize(text: str, sent: List, tok: List):
    """
    Tokenize the corpus into words and sentences
    """
    text = text.lower()
    text = remove_punctuations(text)

    sentences = []
    s = '<SOS> '
    for word in text:
        if word.endswith('.'):
            word = word[:-1]
            s = s + word + ' <EOS>'

            if s != '<SOS>  <EOS>':
                s = s.replace('  ', ' ')
                sentences.append(s.strip())
            s = '<SOS> '

        else:
            s = s + word

    for sent1 in sentences:
        if sent1 == ' ':
            remove_punctuations(sent1)

    sent.extend(sentences)
    tokens = text.split()
    lower_tokens = []
    for x in tokens:
        lower_tokens.append(x.lower())
    punct = string.punctuation
    table = str.maketrans('', '', punct)
    stripped = [w.translate(table) for w in tokens]
    tok.extend(stripped)
    return tok, sent


def get_tokens(file_dir: str):
    sentences = []
    tokens = []

    files = glob.glob(file_dir)

    for name in files:
        file = open(name, 'rt', encoding="ISO-8859-1")
        text = file.read()
        tokens, sentences = tokenize(text, sentences, tokens)

    return tokens, sentences


"""
Part 2: Define Unigram Language Model
"""
def unigramLangModel(words: str, start_sentence: str, end_sentence: str, freq_dict_unigram: Dict) -> Dict:
    for word in words:
        if word != start_sentence and word != end_sentence:
            freq_dict_unigram[word] = freq_dict_unigram.get(word, 0) + 1

    return freq_dict_unigram


"""
Part 3: Minimum Edit Distance
"""
def edit_distance(word, alphabet):
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
    replaces = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts = [a + c + b for a, b in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)


def edit_distance2(word, alphabet):
    return set(e2 for e1 in edit_distance(word, alphabet) for e2 in edit_distance(e1, alphabet))


def cal_med(s: str, t: str):
    if s == '':
        return len(t)
    if t == '':
        return len(s)
    if s[-1] == t[-1]:
        cost = 0
    else:
        cost = 1

    res = min([cal_med(s[:-1], t) + 1,
               cal_med(s, t[:-1]) + 1,
               cal_med(s[:-1], t[:-1]) + cost])

    return res


"""
Part 4: Spelling Correction
"""
def spell_checker(word, alphabet, n_grams, need_2_med=True) -> Tuple:
    """
    Take a word as input and check whether the word is in vocabulary dictionary.
    """
    word = word.lower()

    if word in n_grams.keys():
        return True, 'correct'
    else:

        suggestion_set = set(edit_distance(word, alphabet)) & set(n_grams.keys())

        if need_2_med and len(suggestion_set) == 0:
            suggestion_set = set(edit_distance2(word, alphabet)) & set(n_grams.keys())

        suggestion_dict = OrderedDict()
        for i in suggestion_set:
            temp_med = cal_med(word, i)
            temp = i + ' (Non-word Error with MED: ' + str(temp_med) + ')'
            suggestion_dict[temp] = temp_med

        return False, suggestion_dict


"""
Part 5: Build Language Model
"""
def language_model(tokens, start_sentence: str, end_sentence: str, freq_dict_unigram: Dict):
    freq_dict_unigram = unigramLangModel(tokens, start_sentence, end_sentence, freq_dict_unigram)
    return freq_dict_unigram
