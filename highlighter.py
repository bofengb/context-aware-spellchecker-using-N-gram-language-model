"""
References:
    https://github.com/AshwiniRangnekar/GrammaticalErrorDetection-Correction
    https://github.com/troublemeeter/spelling-correction
    https://github.com/NethumL/pyqt-spellcheck
"""

import re

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat

from spellcheckwrapper import SpellCheckWrapper


class SpellCheckHighlighter(QSyntaxHighlighter):
    wordRegEx = re.compile(r"\b([A-Za-z]{1,})\b")

    def highlightBlock(self, text: str) -> None:
        if not hasattr(self, "speller"):
            return

        self.misspelledFormat = QTextCharFormat()
        self.misspelledFormat.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)
        self.misspelledFormat.setUnderlineColor(Qt.red)

        self.missContextFormat = QTextCharFormat()
        self.missContextFormat.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)
        self.missContextFormat.setUnderlineColor(Qt.blue)

        temp = []
        for word_object in self.wordRegEx.finditer(text):
            temp.append(word_object.group())

        count = 0
        for word_object in self.wordRegEx.finditer(text):
            if not self.speller.check(word_object.group()):
                self.setFormat(
                    word_object.start(),
                    word_object.end() - word_object.start(),
                    self.misspelledFormat,
                )

            elif count != 0:
                if not self.speller.check_context(temp[count - 1] + ' ' + temp[count]):
                    self.setFormat(
                        word_object.start(),
                        word_object.end() - word_object.start(),
                        self.missContextFormat,
                    )

            count += 1

    def setSpeller(self, speller: SpellCheckWrapper):
        self.speller = speller
