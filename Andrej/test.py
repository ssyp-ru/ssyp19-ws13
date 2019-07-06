from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor, QFont, QImage, QPen
from PyQt5.QtCore import Qt, QPoint
from random import *
import sys

class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.brushes = []
        self.brushtype = "point"
        self.brushundertype = "point"
        self.draw = False
        self.lastPoint = QPoint
        self.brushColor = Qt.black
        self.brushSize = 1
        self.backgorundColor = Qt.white
        
        self.painter = QPainter()

        self.canvas = QImage(self.size(), QImage.Format_RGB32)
        self.canvas.fill(Qt.black)

        self.initUI()
        self.grabKeyboard()

    def newBrush(self, brush):
    	self.brushes.append(brush)

    def messageSend(self, message):
    	self.statusBar().showMessage(message)

    def brushMessage(self):
    	self.messageSend("Brush Type is \"" + self.brushtype + "\"")

    def paintEvent(self, event):
    	self.painter.begin(self)
    	self.painter.setBackground(self.backgorundColor)
    	self.painter.fillRect(0, 24, 700, 600, self.backgorundColor)

    def createObject(self, objectType):
    	pass

    def setBrushType(self, typeOfBrush, brushObject):
    	self.brushtype = typeOfBrush
    	self.brushMessage()
    	for brush in self.brushes:
    		brush.setChecked(False)
    	brushObject.setChecked(True)


    def back(self):
    	pass

    def forwards(self):
    	pass

    def mouseMoveEvent(self, event):
    	if event.buttons():
    		print("Moving with Button-1")

    def mousePressEvent(self, event):
    	if event.button() == 1:
    		print("Button-1 was pressed")
    		pos = [event.x(), event.y()]
    	elif event.button() == 2 or event.button() == 3:
    		print("Button-2 was pressed")

    def mouseReleaseEvent(self, event):
    	if event.button() == 1:
    		print("Button-1 was unpressed")


    def centering(self):
    	qr = self.frameGeometry()
    	cp = QDesktopWidget().availableGeometry().center()
    	qr.moveCenter(cp)
    	self.move(qr.topLeft())

    def clear(self):
        self.painter.setBackground(self.backgorundColor)
        self.painter.fillRect(0, 24, 700, 600, self.backgorundColor)
        #self.showMessage("Clear succesfully")

    def initUI(self):
        self.setGeometry(400, 400, 700, 600)
        self.setWindowTitle("Prototype")
        self.show()
        self.centering()
        self.resize(700, 600)

        self.setToolTip("<b>Drawing Place</b>")
        
        self.newFileAct = QAction("&New", self)
        self.newFileAct.setShortcut("Ctrl+N")
        self.newFileAct.setStatusTip("Creating New File")
        self.newFileAct.setToolTip("Creating <b>New</b> File")
        #self.newFileAct.triggered.connect(self.clear)

        self.quitAct = QAction("&Quit", self)
        self.quitAct.setShortcut("Ctrl+Q")
        self.quitAct.setStatusTip("Quit program")
        self.quitAct.setToolTip("<b>Quit</b> program")
        self.quitAct.triggered.connect(qApp.quit)

        self.typeBrushes = QMenu("&Brush Types", self)

        self.pointBrush = QAction("&Point", self, checkable=True)
        self.pointBrush.setShortcut("Ctrl+1")
        self.pointBrush.setStatusTip("Take Point Brush")
        self.pointBrush.setToolTip("Take <b>Point</b> Brush")
        self.pointBrush.triggered.connect(lambda event: self.setBrushType("point", self.pointBrush))
        self.pointBrush.setChecked(True)
        self.newBrush(self.pointBrush)

        self.sectionBrush = QAction("&Section", self, checkable=True)
        self.sectionBrush.setShortcut("Ctrl+2")
        self.sectionBrush.setStatusTip("Take Section Brush")
        self.sectionBrush.setToolTip("Take <b>Section</b> Brush")
        self.sectionBrush.triggered.connect(lambda event: self.setBrushType("section", self.sectionBrush))
        self.sectionBrush.setChecked(False)
        self.newBrush(self.sectionBrush)

        self.circleBrush = QAction("&Circle", self, checkable=True)
        self.circleBrush.setShortcut("Ctrl+3")
        self.circleBrush.setStatusTip("Take Circle Brush")
        self.circleBrush.setToolTip("Take <b>Circle</b> Brush")
        self.circleBrush.triggered.connect(lambda event: self.setBrushType("circle", self.circleBrush))
        self.circleBrush.setChecked(False)
        self.newBrush(self.circleBrush)


        self.backCommand = QAction("&Back", self)
        self.backCommand.setShortcut("Ctrl+Left")
        self.backCommand.setStatusTip("Return back")
        self.backCommand.setToolTip("Return <b>back</b>")
        self.backCommand.triggered.connect(self.back)

        self.forwardCommand = QAction("&Forwards", self)
        self.forwardCommand.setShortcut("Ctrl+Right")
        self.forwardCommand.setStatusTip("Return forwards")
        self.forwardCommand.setToolTip("Return <b>forwards</b>")
        self.forwardCommand.triggered.connect(self.forwards)


        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu("&File")
        self.fileMenu.addAction(self.newFileAct)

        self.brushesMenu = self.menubar.addMenu("&Brushes")
        self.brushesMenu.addMenu(self.typeBrushes)

        self.typeBrushes.addAction(self.pointBrush)
        self.typeBrushes.addAction(self.sectionBrush)
        self.typeBrushes.addAction(self.circleBrush)

        self.editMenu = self.menubar.addMenu("&Edit")

        self.editMenu.addAction(self.backCommand)
        self.editMenu.addAction(self.forwardCommand)

        self.toolbar = self.addToolBar("Toolbar")
        self.toolbar.setMovable(False)
        self.toolbar.setToolTip("<b>Toolbar</b>")
        self.toolbar.setStatusTip("Toolbar")
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.pointBrush)
        self.toolbar.addAction(self.sectionBrush)
        self.toolbar.addAction(self.circleBrush)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.backCommand)
        self.toolbar.addAction(self.forwardCommand)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.newFileAct)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.quitAct)
        self.toolbar.addSeparator()

        self.statusBar().showMessage("Paint")

app = QApplication(sys.argv)
interface = MainWidget()
sys.exit(app.exec_())
