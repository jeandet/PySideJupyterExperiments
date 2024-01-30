from qasync import QEventLoop, QApplication
import asyncio

from MainWindow import MainWindow
import sys

from ipykernel.kernelapp import IPKernelApp


def main():
    app = QApplication(sys.argv)

    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)

    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set)
    kernel = IPKernelApp.instance(kernel_name="SciQLop")

    kernel.initialize()
    main_window = MainWindow(kernel)
    main_window.show()
    # this start function is blocking :/ but it still works
    kernel.start()
    print("IPython kernel started")
    with event_loop:
        print("Starting event loop")
        event_loop.run_until_complete(app_close_event.wait())


if __name__ == "__main__":
    main()
