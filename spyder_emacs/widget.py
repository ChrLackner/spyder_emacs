
from qtpy import QtWidgets, QtGui

from .server import EmacsProcess, SpyderEPCServer

import time
from threading import Thread
import logging
logger = logging.getLogger(__name__)

class EmacsWidget(QtWidgets.QWidget):
    def __init__(self, plugin, *args, **kwargs):
        super(EmacsWidget, self).__init__(*args, **kwargs)
        self.plugin = plugin
        self._started = False

    def _resize_emacs(self):
        while not self._server.clients:
            time.sleep(0.1)
        self._server.clients[0].call("set-width", [int(self.geometry().width()*0.95)])
        self._server.clients[0].call("set-height", [int(self.geometry().height()*0.97)])

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
        thread = Thread(target=self._resize_emacs)
        thread.daemon = True
        thread.start()
