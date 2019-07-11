from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor, QFont, QImage, QPen, QBrush, QTextCursor
from PyQt5.QtCore import Qt, QPoint, QRect
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.console= QTextEdit(parent=self)
        self.foobar= QTextEdit(parent=self)
        self.console.resize(500,100)
        self.resize(500,500)
        self.foobar.resize(500, 100)
        self.foobar.move(0, 150)
        self.show()
        

app = QApplication(sys.argv)
interface = MainWindow()
sys.exit(app.exec_())
