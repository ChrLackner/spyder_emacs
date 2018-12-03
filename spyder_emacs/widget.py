
from qtpy import QtWidgets, QtGui

from .server import EmacsProcess, SpyderEPCServer

import time
from threading import Thread
import logging, queue
logger = logging.getLogger(__name__)

class EmacsWidget(QtWidgets.QWidget):
    def __init__(self, plugin, *args, **kwargs):
        super(EmacsWidget, self).__init__(*args, **kwargs)
        self.plugin = plugin
        self._started = False
        self._resizeQueue = queue.Queue()
        def run():
            while True:
                _exit_sig = self._resizeQueue.get()
                if _exit_sig:
                    break
                while True:
                    try:
                        _exit_sig = self._resizeQueue.get(False)
                        if _exit_sig:
                            return
                    except:
                        break
                while not self._server.clients:
                    time.sleep(0.1)
                self._server.clients[0].call("set-width", [int(self.geometry().width())-40])
                self._server.clients[0].call("set-height", [int(self.geometry().height())-20])
                time.sleep(0.1)
                self._resizeQueue.task_done()
        self._resizeThread = Thread(target=run)
        self._resizeThread.start()

    def _resize_emacs(self):
        self._resizeQueue.put(False)

    def start(self):
        self._started = True
        self._server = SpyderEPCServer(self.plugin)
        self._emacs_window = QtGui.QWindow()
        self._emacs_widget = QtWidgets.QWidget.createWindowContainer(self._emacs_window)
        self.proc = EmacsProcess(self._emacs_window)
        self.proc.start(int(self._emacs_window.winId()), self._server.server_address[1])
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._emacs_widget)
        self.setLayout(layout)

    def close(self):
        self._server.shutdown()
        self.proc.kill()
        self.proc.waitForFinished()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self._started:
            self.start()
        self._resize_emacs()
