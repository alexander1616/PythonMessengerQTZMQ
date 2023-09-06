import time
from PyQt6.QtCore import (
    QTimer,
    QDateTime
)

class AlexQTimer():
    def __init__(self):
        self.timestamp = time.time()
        self.timeObj = None
        self.callback = []

    def updateTime(self):
        self.timestamp = time.time()
        ###
        # callbacks
        for f in self.callback:
            f()

    def addCallback(self, f):
        self.callback.append(f)

    def createQTimer(self):
        self.timeObj = QTimer()
        self.timeObj.timeout.connect(self.updateTime)

    def start(self):
        self.timeObj.start(1000)
