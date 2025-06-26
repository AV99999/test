# gui/gui_main_window.py

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QTextEdit, QLineEdit
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from tcl_interpreter import TclInterpreter
import sys

class TclGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenDB Tcl GUI")
        self.setGeometry(100, 100, 800, 600)

        self.interp = TclInterpreter()
        self.history = []
        self.history_index = -1
        self.font_size = 12

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(QFont("Courier", self.font_size))

        self.input = QLineEdit()
        self.input.setFont(QFont("Courier", self.font_size))
        self.input.returnPressed.connect(self.execute_command)

        central = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.output)
        layout.addWidget(self.input)
        central.setLayout(layout)

        self.setCentralWidget(central)
        self.input.setFocus()

    def execute_command(self):
        cmd = self.input.text().strip()
        if not cmd:
            return

        self.history.append(cmd)
        self.history_index = len(self.history)

        result = self.interp.eval(cmd)
        self.output.append(f"> {cmd}")
        self.output.append(result)
        self.input.clear()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up and self.history:
            self.history_index = max(0, self.history_index - 1)
            self.input.setText(self.history[self.history_index])
        elif event.key() == Qt.Key_Down and self.history:
            self.history_index = min(len(self.history), self.history_index + 1)
            if self.history_index < len(self.history):
                self.input.setText(self.history[self.history_index])
            else:
                self.input.clear()
        elif event.modifiers() & Qt.ControlModifier:
            if event.key() == Qt.Key_Plus:
                self.font_size += 1
                self._update_font()
            elif event.key() == Qt.Key_Minus:
                self.font_size -= 1
                self._update_font()

    def _update_font(self):
        font = QFont("Courier", self.font_size)
        self.output.setFont(font)
        self.input.setFont(font)

def launch_gui():
    app = QApplication(sys.argv)
    win = TclGui()
    win.show()
    sys.exit(app.exec_())

