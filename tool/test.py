import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


def fun():
    print("ff")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    QTimer().singleShot(1000, fun)
    sys.exit(app.exec_())
