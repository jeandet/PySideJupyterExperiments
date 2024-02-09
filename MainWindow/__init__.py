from PySide6.QtWidgets import QMainWindow, QPushButton
from ipykernel.kernelapp import IPKernelApp
from QtConsoleSpawner import new_qt_console


class MainWindow(QMainWindow):
    def __init__(self, kernel=None):
        super().__init__()
        self._kernel = kernel
        self._console = None
        self._button = QPushButton("Start QtConsole")
        self._button.clicked.connect(self.start_qt_console)
        self.setCentralWidget(self._button)
        if self._kernel is not None:
            self._kernel.shell.push({"main_window": self})

    def closeEvent(self, event):
        event.accept()
        if self._console is not None:
            self._console.terminate()
        self._kernel.shell.run_cell("quit()")
        self._kernel.cleanup_connection_file()
        self._kernel = None
        super().closeEvent(event)

    def start_qt_console(self):
        if self._kernel is None:
            self._kernel = IPKernelApp.instance(kernel_name="SciQLop")
            self._kernel.initialize(["python", "--gui=qt6", "--colors=linux"])
            self._kernel.shell.push({"main_window": self})
            self._console = new_qt_console(self._kernel)
            self._kernel.start()
        else:
            self._console = new_qt_console(self._kernel)
