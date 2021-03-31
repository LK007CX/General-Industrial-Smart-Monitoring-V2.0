import sys

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication


class MonitorWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(MonitorWidget, self).__init__(*args, **kwargs)

        self.label1 = QLabel("allow close: ")
        self.label2 = QLabel("result list: ")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MonitorWidget()
    win.show()
    sys.exit(app.exec_())
