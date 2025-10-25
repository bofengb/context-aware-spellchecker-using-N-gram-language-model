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
        file = open(name, 'rt')
        text = file.read()
        tokens, sentences = tokenize(text, sentences, tokens)

    return tokens, sentences


"""
Part 2: Define Unigram Language Model and Bigram Language Model
"""
def unigramLangModel(words: str, start_sentence: str, end_sentence: str, freq_dict_unigram: Dict) -> Dict:
    for word in words:
        if word != start_sentence and word != end_sentence:
            freq_dict_unigram[word] = freq_dict_unigram.get(word, 0) + 1

    return freq_dict_unigram


def bigramLangModel(sentences: str, start_sentence: str, end_sentence: str, freq_dict_bigram: Dict) -> Dict:
    for sentence in sentences:
        sentence = sentence.split()

        previous_word = None
        for word in sentence:
            if previous_word is not None:
                freq_dict_bigram[(previous_word, word)] = freq_dict_bigram.get((previous_word, word), 0) + 1

            previous_word = word

    return freq_dict_bigram


"""
Part 3: Laplace Smoothing Techniques
"""
def laplace_smoothing(num: int, deno: int, freq_dict_unigram: Dict):
    num += 1
    deno += len(freq_dict_unigram) + 1
    return num, deno


"""
Part 4: Compute Sentence Score
"""
def bigram_sentence_probability(sent, freq_dict_unigram: Dict, freq_dict_bigram: Dict):
    """
    Calculate the score for a sentence using Bigram Language model.
    If the score of the input sentence is high, this sentence is tend to be correct.
    If the score of the input sentence is low, this sentence may contain a real-word error.
    """
    sum = 0.0
    previous_word = None
    sent = sent.split()
    for word in sent:
        if previous_word != None:
            bigram_prob = cal_bigram_probability(previous_word, word, freq_dict_unigram, freq_dict_bigram)
            if bigram_prob != 0:
                sum += bigram_prob
        previous_word = word
    return sum


def cal_bigram_probability(prev_word, word, freq_dict_unigram: Dict, freq_dict_bigram: Dict):
    num = freq_dict_bigram.get((prev_word, word), 0)
    denum = freq_dict_unigram.get(prev_word, 0)

    # Laplace Smoothing
    num, denum = laplace_smoothing(num, denum, freq_dict_unigram)
    if num == 0 or denum == 0:
        return 0.0
    else:
        return float(num) / float(denum)


"""
Part 5: Build Language Model
"""
def language_model(tokens, sentences, start_sentence: str, end_sentence: str, freq_dict_unigram: Dict, freq_dict_bigram: Dict):
    freq_dict_unigram = unigramLangModel(tokens, start_sentence, end_sentence, freq_dict_unigram)
    freq_dict_bigram = bigramLangModel(sentences, start_sentence, end_sentence, freq_dict_bigram)
    return freq_dict_unigram, freq_dict_bigram
