"""
References:
    https://github.com/AshwiniRangnekar/GrammaticalErrorDetection-Correction
    https://github.com/troublemeeter/spelling-correction
    https://github.com/NethumL/pyqt-spellcheck
"""

from typing import Callable, List, Set

from PyQt5.QtCore import QTemporaryFile

import non_word_checking
import real_word_checking


class SpellCheckWrapper:
    def __init__(self):
        self.file = QTemporaryFile()
        self.file.open()

        # Sentence start identifier
        start_sentence = '<SOS>'
        # Sentence end identifier
        end_sentence = '<EOS>'
        # Unigram dictionary
        freq_dict_unigram = {}
        # Bigram dictionary
        freq_dict_bigram = {}

        self.alphabet = set('abcdefghijklmnopqrstuvwxyz')

        # Corpus preprocessing
        a, b = non_word_checking.get_tokens('./data/*.txt')

        # Build language models
        self.freq_dict_unigram = non_word_checking.language_model(a, start_sentence, end_sentence, freq_dict_unigram)
        self.freq_dict_unigram_context, self.freq_dict_bigram_context, = real_word_checking.language_model(a, b, start_sentence, end_sentence, freq_dict_unigram, freq_dict_bigram)

    def suggestions(self, word: str) -> List[str]:
        corr_flag, suggestions = non_word_checking.spell_checker(word, self.alphabet, self.freq_dict_unigram, need_2_med=True)
        return suggestions

    def suggestions_context(self, word: str) -> List[str]:
        if len(word.split()) > 1:
            pre_word = word.split()[0]
            last_word = word.split()[1]
        else:
            return []

        # word = '<SOS> ' + word + ' <EOS>'
        prob = real_word_checking.bigram_sentence_probability(word, self.freq_dict_unigram_context, self.freq_dict_bigram_context)

        suggestion_set = set(non_word_checking.edit_distance(last_word, self.alphabet)) & set(self.freq_dict_unigram.keys())
        # suggestion_set_1 = set(non_word_checking.edit_distance(last_word, self.alphabet)) & set(self.freq_dict_unigram.keys())
        # suggestion_set_2 = {}
        # if len(suggestion_set_1) == 0:
        #     suggestion_set_2 = set(non_word_checking.edit_distance2(last_word, self.alphabet)) & set(
        #     self.freq_dict_unigram.keys())
        # suggestion_set = suggestion_set_1 or suggestion_set_2
        suggestion_list = list(suggestion_set)

        real_suggestion_list = []
        for i in suggestion_list:
            # prob_temp = real_word_checking.bigram_sentence_probability('<SOS> ' + pre_word + ' ' + i + ' <EOS>', self.freq_dict_unigram_context, self.freq_dict_bigram_context)
            prob_temp = real_word_checking.bigram_sentence_probability(pre_word + ' ' + i, self.freq_dict_unigram_context, self.freq_dict_bigram_context)
            if prob < prob_temp:
                real_suggestion_list.append(i + ' (Real-word Error)')

        return real_suggestion_list

    def check(self, word: str) -> bool:
        corr_flag, suggestions = non_word_checking.spell_checker(word, self.alphabet, self.freq_dict_unigram)
        return corr_flag

    def check_context(self, word: str) -> bool:
        if len(word.split()) > 1:
            pre_word = word.split()[0]
            last_word = word.split()[1]
        else:
            return True

        # word = '<SOS> ' + word + ' <EOS>'
        prob = real_word_checking.bigram_sentence_probability(word, self.freq_dict_unigram_context, self.freq_dict_bigram_context)

        suggestion_set = set(non_word_checking.edit_distance(last_word, self.alphabet)) & set(self.freq_dict_unigram.keys())
        # suggestion_set_1 = set(non_word_checking.edit_distance(last_word, self.alphabet)) & set(
        #     self.freq_dict_unigram.keys())
        # suggestion_set_2 = {}
        # if len(suggestion_set_1) == 0:
        #     suggestion_set_2 = set(non_word_checking.edit_distance2(last_word, self.alphabet)) & set(
        #         self.freq_dict_unigram.keys())
        # suggestion_set = suggestion_set_1 or suggestion_set_2
        suggestion_list = list(suggestion_set)

        for i in suggestion_list:
            # prob_temp = real_word_checking.bigram_sentence_probability('<SOS> ' + pre_word + ' ' + i + ' <EOS>', self.freq_dict_unigram_context, self.freq_dict_bigram_context)
            prob_temp = real_word_checking.bigram_sentence_probability(pre_word + ' ' + i, self.freq_dict_unigram_context, self.freq_dict_bigram_context)
            if prob < prob_temp:
                return False

        return True
