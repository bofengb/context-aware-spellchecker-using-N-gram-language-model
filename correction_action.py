"""
References:
    https://github.com/AshwiniRangnekar/GrammaticalErrorDetection-Correction
    https://github.com/troublemeeter/spelling-correction
    https://github.com/NethumL/pyqt-spellcheck
"""

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QAction


class SpecialAction(QAction):
    actionTriggered = pyqtSignal(str)

    def __init__(self, *args):
        super().__init__(*args)

        self.triggered.connect(self.emitTriggered)

    def emitTriggered(self):
        self.actionTriggered.emit(self.text().split()[0])
