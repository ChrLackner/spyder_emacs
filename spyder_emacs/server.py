
import os

from qtpy import QtCore
from epc.server import ThreadingEPCServer

import threading, logging

logger = logging.getLogger(__name__)

emacs_script = os.path.join(os.path.dirname(os.path.abspath(__file__)),"emacs-integration.el")

class EmacsProcess(QtCore.QProcess):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

    def start(self, winId, port):
        startstring = 'emacs --eval "(setq portnumber ' + str(port) + ')" --load ' + emacs_script + ' --maximized --parent-id ' + str(winId)
        super().start(startstring)


class SpyderEPCServer(ThreadingEPCServer):
    def __init__(self, plugin):
        super().__init__(('localhost',0), log_traceback=True)
        self.server_thread = threading.Thread(target=self.serve_forever)
        self.server_thread.allow_reuse_address = True
        self.server_thread.start()
        def run(buffer_filename):
            wdir, fname = os.path.split(os.path.abspath(buffer_filename))
            plugin.run_in_current_ipyclient.emit(fname, wdir, "",
                                                 False, False, True, True)
        self.register_function(run)
