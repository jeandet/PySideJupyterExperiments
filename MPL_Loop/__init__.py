import jupyter_client

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication
from MainWindow import MainWindow

from ipykernel.kernelapp import IPKernelApp

from QtConsoleSpawner import new_qt_console


def main():
    app = QApplication([])
    kernel = IPKernelApp.instance(kernel_name="SciQLop")
    window = MainWindow(kernel)
    window.show()

    kernel.initialize(["python", "--matplotlib=qt"])
    print("IPython kernel initialized")
    kernel.start()


if __name__ == "__main__":
    main()
