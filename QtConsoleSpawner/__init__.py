from PySide6.QtCore import QObject, Signal, Slot, QProcess
import jupyter_client
import subprocess
import os, sys


def get_python_executable() -> str:
    if "APPIMAGE" in os.environ:
        return os.path.join(os.environ["APPDIR"], "usr/bin/python3")
    python_exe = 'python.exe' if os.name == 'nt' else 'python'
    if python_exe not in os.path.basename(sys.executable):
        def _find_python() -> str:
            return next(filter(lambda p: os.path.exists(p),
                               map(lambda p: os.path.join(p, python_exe),
                                   [sys.prefix, os.path.join(sys.prefix, 'bin'), sys.base_prefix, sys.base_exec_prefix,
                                    os.path.join(sys.base_prefix, 'bin')])))

        if (python_path := _find_python()) in (None, "") or not os.path.exists(python_path):
            raise RuntimeError("Could not find python executable")
        else:
            return python_path
    return sys.executable


def new_qt_console(kernel):
    connection_file = jupyter_client.find_connection_file(kernel.abs_connection_file)
    args = ["-S", "-c", "from qtconsole import qtconsoleapp;qtconsoleapp.main()", "--existing", connection_file]
    python_executable = get_python_executable()
    print(f"Starting QtConsole with {python_executable} {' '.join(args)}")
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(sys.path)
    process = subprocess.Popen([python_executable] + args, env=env)
    print(f"Started QtConsole with PID {process.pid}, connection file {connection_file}")
    return process
