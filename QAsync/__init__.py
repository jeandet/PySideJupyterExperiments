from qasync import QEventLoop, QApplication, asyncSlot
from PySide6.QtCore import QTimer
from typing import Optional
import asyncio

from MainWindow import MainWindow
import sys

from ipykernel.kernelapp import IPKernelApp

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


class MyKernelApp(IPKernelApp):
    def start(self):
        """Start the application."""
        if self.subapp is not None:
            return self.subapp.start()
        if self.poller is not None:
            self.poller.start()
        self.kernel.start()
        app = get_app()
        app_close_event = asyncio.Event()
        app.aboutToQuit.connect(app_close_event.set)
        self.timer = QTimer()
        self.timer.timeout.connect(self.do_one_iteration)
        self.timer.start(int(1000 * self.kernel._poll_interval))
        event_loop = get_event_loop()
        with event_loop:
            event_loop.run_until_complete(app_close_event.wait())

    @asyncSlot()
    async def do_one_iteration(self):
        await self.kernel.do_one_iteration()


def main():
    event_loop = get_event_loop()
    app = get_app()
    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set)
    kernel_app = MyKernelApp.instance(kernel_name="MyKernel")
    kernel_app.initialize()
    main_window = MainWindow(kernel=kernel_app)
    main_window.show()
    kernel_app.start()


if __name__ == "__main__":
    main()
