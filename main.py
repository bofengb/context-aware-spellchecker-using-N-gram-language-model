"""
References:
    https://github.com/AshwiniRangnekar/GrammaticalErrorDetection-Correction
    https://github.com/troublemeeter/spelling-correction
    https://github.com/NethumL/pyqt-spellcheck
"""

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from spellcheckwrapper import SpellCheckWrapper
from spelltextedit import SpellTextEdit


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.speller = SpellCheckWrapper()
        self.setupUi()

    def setupUi(self):
        self.resize(500, 500)
        self.setWindowTitle('Spelling Correction')

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout(self.centralWidget)
        self.centralWidget.setLayout(self.layout)

        self.textEdit = SpellTextEdit(self.speller, self.centralWidget)
        self.layout.addWidget(self.textEdit)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())
