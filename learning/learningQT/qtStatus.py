import time, os, sys
import zmq
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QPushButton,
    QWidget,
    QLabel,
    QTextEdit
)
from PyQt6 import (
    QtCore
)

class AlexQStatus():
    def __init__(self, port, adr = None, func = None):
        self.port = port
        if adr is None:
            self.adr = "tcp://localhost"
        else:
            self.adr = adr
        self.totalMsgs = 0
        self.curTime = 0
        self.lastTime = 0
        self.msgRcv = 0
        self.msgRate = 0
        self.maxRate = 0
        self.maxTime = 0
        self.lastTotalMsgs = 0
        
        if func is None:
            raise Exception("Need a callback func for read")
        
        self.readCbFunc = func
        self.socket = None
        self.socketNotifier = None
        ### display object should be here
        ### 
        self.labelPort = None
        self.labelTotal = None
        self.labelMaxPer = None
        self.labelRecvPer = None
        self.labelCurrentTime = None

    #################
    # zmq helper functions
    def _createWorker(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.PULL)
        self.socket.connect("%s:%d"%(self.adr, self.port))
        self.socketNotifier = QtCore.QSocketNotifier(self._getFd(), QtCore.QSocketNotifier.Type.Read)
        self.socketNotifier.activated.connect(self.zmqPollAvail)

    def _getFd(self):
        return self.socket.getsockopt(zmq.FD)

    def _getEvents(self):
        return self.socket.getsockopt(zmq.EVENTS)
    
   # @QtCore.pyqtSlot()
    def zmqPollAvail(self):
        self.socketNotifier.setEnabled(False)
        if self._getEvents() & zmq.POLLIN:
            while self._getEvents() & zmq.POLLIN:
                buff = self.socket.recv()
                self.updateTotal()
                if self.readCbFunc is not None:
                    self.readCbFunc(str(buff))
        self.socketNotifier.setEnabled(True)

    #######################
    # display related functions
    #######################
    def createDisplayObj(self, wlayout, startat):
        self.labelPort = QLabel('Port')
        self.labelTotal = QLabel('Total')
        self.labelMaxPer = QLabel('Max')
        self.labelRecvPer = QLabel('Recv')
        self.labelCurrentTime = QLabel('Time')
        wlayout.addWidget(self.labelPort, startat, 0)
        wlayout.addWidget(self.labelCurrentTime, startat, 1)
        wlayout.addWidget(self.labelTotal, startat, 2)
        wlayout.addWidget(self.labelRecvPer, startat, 3)
        wlayout.addWidget(self.labelMaxPer, startat, 4)

        ########################
        # Create pulling socket
        self._createWorker()
        return

    #######################
    # display Total only for fast update
    #######################
    def displayTotal(self):
        self.labelTotal.setText("%14d"%(self.totalMsgs))
        
    def displayStatus(self):
        local_time = time.ctime(self.curTime)
        displayMsg = f"{local_time}"
        self.labelPort.setText(f"{self.port}")
        self.labelCurrentTime.setText(displayMsg)
        self.labelTotal.setText("%14d"%(self.totalMsgs))
        self.labelMaxPer.setText("%6.0f"%(self.maxRate))
        self.labelRecvPer.setText("%6.0f"%(self.msgRate))

    #######################
    # function will deal with internal data
    #######################
    def updateTotal(self):
        self.totalMsgs += 1
        self.displayTotal()

    def timerStatus(self):
        t_cur_time = time.time()
        if t_cur_time < self.curTime:
            print("Duplicated Call: TimerStatus")
            return
        self.lastTime = self.curTime
        self.curTime = time.time()
        self.msgRcv = self.totalMsgs - self.lastTotalMsgs
        time_diff = self.curTime - self.lastTime
        self.msgRate = self.msgRcv / time_diff
        if self.msgRate > self.maxRate:
            self.maxRate = self.msgRcv
            self.maxTime = self.curTime
        self.lastTotalMsgs = self.totalMsgs
        self.displayStatus()
