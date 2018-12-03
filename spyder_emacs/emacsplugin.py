
from spyder.config.base import _
from spyder.utils import icon_manager as ima

try:
    # Spyder 4
    from spyder.api.plugins import SpyderPluginWidget
except ImportError:
    # Spyder 3
    from spyder.plugins import SpyderPluginWidget

# qt imports
from qtpy import PYQT4, PYSIDE, QtCore, QtWidgets
from .server import SpyderEPCServer, EmacsProcess
from .widget import EmacsWidget

import logging

logger = logging.getLogger(__name__)

class EmacsPlugin(SpyderPluginWidget):
    CONF_SECTION = 'emacs'

    # Signals
    run_in_current_ipyclient = QtCore.Signal(str, str, str, bool, bool, bool, bool)
    run_cell_in_ipyclient = QtCore.Signal(str, str, str, bool)
    exec_in_extconsole = QtCore.Signal(str, bool)
    redirect_stdio = QtCore.Signal(bool)
    open_dir = QtCore.Signal(str)
    breakpoints_saved = QtCore.Signal()
    run_in_current_extconsole = QtCore.Signal(str, str, str, bool, bool)
    open_file_update = QtCore.Signal(str)
    sig_lsp_notification = QtCore.Signal(dict, str)

    def __init__(self, parent, testing=False):
        super(EmacsPlugin, self).__init__(parent)
        self.initialize_plugin()
        self.emacs_widget = EmacsWidget(self)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.emacs_widget)
        self.setLayout(layout)

    # ------ SpyderPluginMixin API --------------------------------------------
    def get_plugin_title(self):
        """Return widget title."""
        title = _('Emacs')
        return title

    def get_plugin_icon(self):
        """Return widget icon."""
        return ima.icon('ipython_console')

    def get_focus_widget(self):
        """Return the widget to give focus to."""
        return self.emacs_widget

    def get_plugin_actions(self):
        """Return a list of actions related to plugin."""
        return []

    def on_first_registration(self):
        pass

    def update_font(self):
        """Update font from Preferences."""
        pass

    def register_plugin(self):
        self.main.add_dockwidget(self)
        self.run_in_current_ipyclient.connect(self.main.editor.run_in_current_ipyclient.emit)

    def refresh_plugin(self):
        """Refresh tabwidget."""

    def closing_plugin(self, cancelable=False):
        """Perform actions before parent main window is closed."""
        return True

    def check_compatibility(self):
        """Check compatibility for PyQt and sWebEngine."""
        value = True
        message = ''
        if PYQT4 or PYSIDE:
            message = _("You are working with Qt4 and in order to use this "
                        "plugin you need to have Qt5.<br><br>"
                        "Please update your Qt and/or PyQt packages to "
                        "meet this requirement.")
            value = False
        return value, message
