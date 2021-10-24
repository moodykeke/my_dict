#!/bin/python3
import fcntl
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from src.main_window import MainWindow
from src.setting import setting, setting_folder
from src.util import version

flock = None


def is_running():
    global flock
    if not os.path.exists(setting_folder):
        os.makedirs(setting_folder)
    flock = open(os.path.join(setting_folder, "lock"), 'w+')
    try:
        fcntl.flock(flock, fcntl.LOCK_NB | fcntl.LOCK_EX)
        return False
    except:
        return True


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '-v':
        print(version["curr"])
        return
    if is_running():
        print("The application is running...")
        return
    # os.environ['QT_DEBUG_PLUGINS'] = '1'
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    if setting.use_dark_skin:
        import qdarkstyle
        dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
        app.setStyleSheet(dark_stylesheet)
    app.setApplicationName("MyDict")
    app.setQuitOnLastWindowClosed(False)
    main_window = MainWindow(app)
    if setting.show_main_window_when_startup:
        main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
