import sys, os
import traceback
import threading
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QWidget
)

import learningQT.qtStatus as qtStatus
import learningQT.qtTimer as aqTimer
import learningQT.qtMsgManager as aqManager

#####################################
#
# Alex Reader Main Class
#
#####################################

class AlexQReader():
    def __init__(self, title):
        self.title = title
        self.window = None
        self.layout = None
        self.textbox = None
        self.status1 = None
        self.status2 = None
        self.timer = None
    
    def _readCb(self, buff):
        self.textbox.appendMsg(buff)
        
    def createDisplay(self):
        # window = widget
        self.window = QWidget()
        self.window.setWindowTitle(self.title)
        # make buttons/widgets first
        self.textbox = aqManager.AlexQManager()
        #self.status1 = qtStatus.AlexQStatus(port=5100, adr="tcp://localhost", func=self._readCb)
        #self.status2 = qtStatus.AlexQStatus(port=5101, adr="tcp://localhost", func=self._readCb)
        self.status1 = qtStatus.AlexQStatus(port=5100, adr="tcp://localhost", func=self.textbox.appendMsg)
        self.status2 = qtStatus.AlexQStatus(port=5101, adr="tcp://localhost", func=self.textbox.appendMsg)
        self.timer = aqTimer.AlexQTimer()
        # add functionality to buttons
        # layout
        self.layout = QGridLayout()
        self.textbox.createDisplay(self.layout, 4)
        self.status1.createDisplayObj(self.layout, 7)
        self.status2.createDisplayObj(self.layout, 8)
        self.window.setLayout(self.layout)
        # timer create after displayable
        self.timer.addCallback(self.status1.timerStatus)
        self.timer.addCallback(self.status2.timerStatus)
        self.timer.createQTimer()

    def start(self):
        self.timer.start()

# first thing to do
app = QApplication([])
alexReader = AlexQReader("Packet Reader")
alexReader.createDisplay()
alexReader.start()

# run program
try:
    alexReader.window.show()
    app.exec()
    sys.exit(0)
except:
    traceback.print_exc(file=sys.stdout)
