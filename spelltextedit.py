"""
References:
    https://github.com/AshwiniRangnekar/GrammaticalErrorDetection-Correction
    https://github.com/troublemeeter/spelling-correction
    https://github.com/NethumL/pyqt-spellcheck
"""

from typing import List

from PyQt5.QtCore import QEvent, Qt, pyqtSlot
from PyQt5.QtGui import QContextMenuEvent, QMouseEvent, QTextCursor
from PyQt5.QtWidgets import QMenu, QTextEdit

from correction_action import SpecialAction
from highlighter import SpellCheckHighlighter
from spellcheckwrapper import SpellCheckWrapper


class SpellTextEdit(QTextEdit):
    def __init__(self, *args):
        if args and type(args[0]) == SpellCheckWrapper:
            super().__init__(*args[1:])
            self.speller = args[0]
        else:
            super().__init__(*args)

        self.highlighter = SpellCheckHighlighter(self.document())
        if hasattr(self, 'speller'):
            self.highlighter.setSpeller(self.speller)

    def setSpeller(self, speller):
        self.speller = speller
        self.highlighter.setSpeller(self.speller)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.RightButton:
            event = QMouseEvent(
                QEvent.MouseButtonPress,
                event.pos(),
                Qt.LeftButton,
                Qt.LeftButton,
                Qt.NoModifier,
            )
        super().mousePressEvent(event)

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        self.contextMenu = self.createStandardContextMenu(event.pos())

        textCursor = self.textCursor()
        textCursor.select(QTextCursor.WordUnderCursor)
        self.setTextCursor(textCursor)

        wordToCheck = textCursor.selectedText()
        if wordToCheck != '':
            suggestions = self.speller.suggestions(wordToCheck)

            space_count = 0
            space_index = []
            plainText = self.toPlainText()
            cursor_index = textCursor.position() - 1
            while cursor_index > 0:
                if plainText[cursor_index].isspace():
                    space_count += 1
                    space_index.append(cursor_index)
                if space_count == 2:
                    break
                cursor_index -= 1

            if not self.speller.check(wordToCheck):
                self.contextMenu.addSeparator()
                self.contextMenu.addMenu(self.createSuggestionsMenu(suggestions))

            elif len(space_index) > 0:
                if len(space_index) == 1:
                    # word_1 = plainText[: space_index[0]]
                    # word_2 = plainText[space_index[0] + 1: textCursor.position()]
                    word = plainText[: textCursor.position()]
                if len(space_index) == 2:
                    # word_1 = plainText[space_index[1] + 1: space_index[0]]
                    # word_2 = plainText[space_index[0] + 1: textCursor.position()]
                    word = plainText[space_index[1] + 1: textCursor.position()]

                suggestions_context = self.speller.suggestions_context(word)
                if not self.speller.check_context(word):
                    self.contextMenu.addSeparator()
                    self.contextMenu.addMenu(self.createSuggestionsMenu(suggestions_context))

        self.contextMenu.exec_(event.globalPos())

    def createSuggestionsMenu(self, suggestions: List[str]):
        suggestionsMenu = QMenu('Change to', self)
        for word in suggestions:
            action = SpecialAction(word, self.contextMenu)
            action.actionTriggered.connect(self.correctWord)
            suggestionsMenu.addAction(action)

        return suggestionsMenu

    @pyqtSlot(str)
    def correctWord(self, word: str):
        textCursor = self.textCursor()
        textCursor.beginEditBlock()
        textCursor.removeSelectedText()
        textCursor.insertText(word)
        textCursor.endEditBlock()
