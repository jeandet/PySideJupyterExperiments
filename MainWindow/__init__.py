from PySide6.QtWidgets import QMainWindow, QPushButton

from QtConsoleSpawner import new_qt_console


class MainWindow(QMainWindow):
    def __init__(self, kernel):
        super().__init__()
        self._kernel = kernel
        self._console = None
        self._button = QPushButton("Start QtConsole")
        self._button.clicked.connect(self.start_qt_console)
        self.setCentralWidget(self._button)
        self._kernel.shell.push({"main_window": self})

    def closeEvent(self, event):
        event.accept()
        if self._console is not None:
            self._console.terminate()
        self._kernel.shell.run_cell("quit()")
        super().closeEvent(event)

    def start_qt_console(self):
        self._console = new_qt_console(self._kernel)
