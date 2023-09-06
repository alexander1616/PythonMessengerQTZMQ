from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QPushButton,
    QWidget,
    QLabel,
    QTextEdit
)

class AlexQManager():
    def __init__(self):
        self.textbox = None
        self.msgCount = 0

    def appendMsg(self, msg):
        if self.msgCount >= 5:
            self.textbox.clear()
            self.msgCount = 0
        self.textbox.append(msg)
        self.msgCount += 1

    def createDisplay(self, wlayout, location):
        self.textbox = QTextEdit()
        wlayout.addWidget(self.textbox, location, 0, 1, 4)
