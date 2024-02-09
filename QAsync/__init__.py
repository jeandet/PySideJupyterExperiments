from qasync import QEventLoop, QApplication
from PySide6.QtCore import QTimer
from typing import Optional
import asyncio

from MainWindow import MainWindow
import sys

from ipykernel.kernelapp import IPKernelApp
from ipykernel.ipkernel import IPythonKernel
from ipykernel.eventloops import register_integration, enable_gui

event_loop: Optional[QEventLoop] = None
app: Optional[QApplication] = None


def get_app() -> QApplication:
    global app
    if app is None:
        app = QApplication(sys.argv)
    return app


def get_event_loop() -> QEventLoop:
    global event_loop
    if event_loop is None:
        event_loop = QEventLoop(get_app())
        asyncio.set_event_loop(event_loop)
    return event_loop


@register_integration('my_loop')
def loop_sciqlop(kernel: IPythonKernel):
    """Start the SciQLop event loop."""
    timer = QTimer()
    timer.timeout.connect(kernel.do_one_iteration)
    timer.start(int(kernel._poll_interval))
    get_event_loop().exec()


def main():
    event_loop = get_event_loop()
    app = get_app()
    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set)
    kernel_app = IPKernelApp.instance(kernel_name="MyKernel")
    kernel_app.eventloop = None
    enable_gui('my_loop', kernel=kernel_app)
    kernel_app.initialize()
    main_window = MainWindow(kernel=kernel_app)
    main_window.show()
    kernel_app.start()


if __name__ == "__main__":
    main()
