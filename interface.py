from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor, QFont, QImage, QPen
from PyQt5.QtCore import Qt, QPoint
from random import *
import sys
import geom as geometry
import math

class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.brushes = []
        self.brushtype = "point"
        self.flag = False
        self.brushColor = Qt.black
        self.backgorundColor = Qt.white
        self.points = []
        self.pointsValue = 0
        self.segments = []
        self.segmentsValue = 0
        self.circles = []
        self.circlesValue = 0
        self.lastname = -1
        self.pointCoords = []
        self.fieldWidth = 400
        self.fieldHeight = 400

        self.table = False

        self.initUI()
        self.grabKeyboard()



    def generatePointName(self):
        dictionary = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
                      "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
                      "W", "X", "Y", "Z"]
        return dictionary[self.lastname-1]

    def newPoint(self, point):
        self.points.append(point)
        self.pointsValue += 1

    def newSegment(self, segment):
        self.segments.append(segment)
        self.segmentsValue += 1

    def newCircle(self, circle):
        self.circles.append(circle)
        self.circlesValue += 1


    def newBrush(self, brush):
        self.brushes.append(brush)

    def messageSend(self, message):
        self.statusBar().showMessage(message)

    def brushMessage(self):
        self.messageSend("Brush Type is \"" + self.brushtype + "\"")

    def paintEvent(self, event):
        paint = QPainter(self)
        paint.drawImage(0,0, self.image)

    def drawingObjects(self, event):
        self.paint.setBrush(QColor("black"))
        self.paint.setPen(QPen(Qt.black, 3))
        self.paint.setFont(QFont("Decorative", 10))
        if self.brushtype == "point":
            self.newPoint(geometry.Point(event.x(), event.y()))
            self.paint.drawEllipse(event.pos(), 2, 2)
            self.update()
            self.messageSend("Point succesfully placed")
        if self.brushtype == "segment":
            if self.pointCoords == []:
                self.pointCoords = [event.x(), event.y()]
            else:
                if self.pointCoords == [event.x(), event.y()]:
                    self.messageSend("Error")
                else:
                    pointCoords = self.pointCoords
                    self.pointCoords = [event.x(), event.y()]
                    self.paint.drawLine(pointCoords[0], pointCoords[1], self.pointCoords[0], self.pointCoords[1])
                    
                    point1 = geometry.Point(pointCoords[0], pointCoords[1])
                    point2 = geometry.Point(self.pointCoords[0], self.pointCoords[1])
                    newSegment = geometry.Segment(point1, point2)
                    self.newSegment(newSegment)
                    
                    self.update()
                    self.messageSend("Segment succesfully placed")
                    self.pointCoords = []
        if self.brushtype == "circle":
            if self.pointCoords == []:
                self.pointCoords = [event.x(), event.y()]
            else:
                pointCoords = self.pointCoords
                self.pointCoords = [event.x(), event.y()]

                #print(pointCoords)
                #print(self.pointCoords)

                coords1 = pointCoords
                coords2 = self.pointCoords
                x = pointCoords[0] - self.pointCoords[0]
                y = pointCoords[1] - self.pointCoords[1]
                distance = math.sqrt((x**2)+(y**2))

                alphaColor = QColor.fromRgbF(0, 0, 0, 0)
                self.paint.setBrush(alphaColor)
                self.paint.drawEllipse(pointCoords[0]-distance, pointCoords[1]-distance, distance*2, distance*2)
                
                self.paint.setBrush(QColor("black"))

                self.newCircle(str(pointCoords[0]-distance) + "-" + str(pointCoords[1]-distance) + "-" + str(distance))

                self.update()
                self.messageSend("Circle succesfully placed")
                self.pointCoords = []

    def createText(self, event, text):
        self.paint.setPen(QColor(53, 8, 65))
        self.paint.setFont(QFont("Decorative", 10))
        self.paint.drawText(event.rect(), Qt.AlignCenter, text)

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

    def reset(self):
        self.pointCoords = []


    def mouseMoveEvent(self, event):
        pass
        

    def mousePressEvent(self, event):
        if event.button() == 1:
            self.flag = True
            self.paint = QPainter(self.image)
            self.drawingObjects(event)
        elif event.button() == 2 or event.button() == 3:
            print("Button-2 was pressed")

    def mouseReleaseEvent(self, event):
        pass


    def centering(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def clear(self):
        #self.painter.setBackground(self.backgorundColor)
        #self.painter.fillRect(0, 24, 700, 600, self.backgorundColor)
        #self.showMessage("Clear succesfully")
        pass

    def reference(self):
        pass

    def authors(self):
        pass


    def backgroundColorSelect(self):
        pass

    def foregroundColorSelect(self):
        pass

    def initUI(self):
        self.setGeometry(400, 400, 700, 600)
        self.setWindowTitle("Prototype")
        self.show()
        self.centering()
        self.resize(700, 600)

        self.image = QImage(self.width(), self.height(), QImage.Format_ARGB32)
        self.image.fill(QColor(255, 255, 255))

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

        self.segmentBrush = QAction("&Segment", self, checkable=True)
        self.segmentBrush.setShortcut("Ctrl+2")
        self.segmentBrush.setStatusTip("Take Segment Brush")
        self.segmentBrush.setToolTip("Take <b>Segment</b> Brush")
        self.segmentBrush.triggered.connect(lambda event: self.setBrushType("segment", self.segmentBrush))
        self.segmentBrush.setChecked(False)
        self.newBrush(self.segmentBrush)

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

        self.resetCommand = QAction("&Reset", self)
        self.resetCommand.setShortcut("Ctrl+R")
        self.resetCommand.setStatusTip("Reset point")
        self.resetCommand.setToolTip("<b>Reset</b> point")
        self.resetCommand.triggered.connect(self.reset)


        self.backgroundColorCommand = QAction("&Background", self)
        self.backgroundColorCommand.setShortcut("Alt+B")
        self.backgroundColorCommand.setStatusTip("Change your background color")
        self.backgroundColorCommand.setToolTip("Change your <b>background color</b>")
        self.backgroundColorCommand.triggered.connect(self.backgroundColorSelect)

        self.foregroundColorCommand = QAction("&Foreground", self)
        self.foregroundColorCommand.setShortcut("Alt+F")
        self.foregroundColorCommand.setStatusTip("Change your foreground color")
        self.foregroundColorCommand.setToolTip("Change your <b>foreground color</b>")
        self.foregroundColorCommand.triggered.connect(self.foregroundColorSelect)


        self.referenceCommand = QAction("&Reference", self)
        self.referenceCommand.setShortcut("F1")
        self.referenceCommand.setStatusTip("Reference show")
        self.referenceCommand.setToolTip("<b>Reference</b> show")
        self.referenceCommand.triggered.connect(self.reference)

        self.authorsCommand = QAction("&Authors", self)
        self.authorsCommand.setStatusTip("Authors show")
        self.authorsCommand.setToolTip("<b>Authors</b> show")
        self.authorsCommand.triggered.connect(self.authors)


        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu("&File")
        self.fileMenu.addAction(self.newFileAct)

        self.brushesMenu = self.menubar.addMenu("&Brushes")
        self.brushesMenu.addMenu(self.typeBrushes)

        self.typeBrushes.addAction(self.pointBrush)
        self.typeBrushes.addAction(self.segmentBrush)
        self.typeBrushes.addAction(self.circleBrush)

        self.editMenu = self.menubar.addMenu("&Edit")
        self.editMenu.addAction(self.backCommand)
        self.editMenu.addAction(self.forwardCommand)

        self.viewMenu = self.menubar.addMenu("&View")
        self.viewMenu.addAction(self.backgroundColorCommand)
        self.viewMenu.addAction(self.foregroundColorCommand)

        self.helpMenu = self.menubar.addMenu("&Help")
        self.helpMenu.addAction(self.referenceCommand)
        self.helpMenu.addAction(self.authorsCommand)

        self.toolbar = self.addToolBar("Toolbar")
        self.toolbar.setMovable(False)
        self.toolbar.setToolTip("<b>Toolbar</b>")
        self.toolbar.setStatusTip("Toolbar")
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.pointBrush)
        self.toolbar.addAction(self.segmentBrush)
        self.toolbar.addAction(self.circleBrush)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.backCommand)
        self.toolbar.addAction(self.forwardCommand)
        self.toolbar.addAction(self.resetCommand)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.newFileAct)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.quitAct)
        self.toolbar.addSeparator()

        self.statusBar().showMessage("Paint")

app = QApplication(sys.argv)
interface = MainWidget()
sys.exit(app.exec_())
