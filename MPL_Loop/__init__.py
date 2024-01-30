from PySide6.QtWidgets import QApplication
from MainWindow import MainWindow

from ipykernel.kernelapp import IPKernelApp


def main():
    app = QApplication([])
    kernel = IPKernelApp.instance(kernel_name="SciQLop")
    kernel.initialize(["python", "--matplotlib=qt"])
    window = MainWindow(kernel)
    window.show()

    print("IPython kernel initialized")
    kernel.start()


if __name__ == "__main__":
    main()
