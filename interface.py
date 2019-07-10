from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor, QFont, QImage, QPen
from PyQt5.QtCore import Qt, QPoint
from random import *
import sys
import geom as geometry
import math
from model import Model


class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.model = Model()
        self.brushes = []
        self.brushundertypes = {}
        self.brushtype = "point"
        self.brushundertype = "point"
        self.flag = False
        self.brushColor = Qt.black
        self.backgorundColor = Qt.white
        self.lastname = -1
        self.pointCoords = []
        self.fieldWidth = 400
        self.fieldHeight = 400
        self.zoomValue = 100
        self.operations = []

        self.table = False

        self.initUI()
        self.grabKeyboard()

    def newPoint(self, x, y):
        self.model.add_point(x, y)
        self.model.operations.append(geometry.Point(x, y))

    def newSegment(self, pointstart, pointend):
        self.model.add_segment(pointstart, pointend)
        self.model.operations.append(geometry.Segment(pointstart, pointend))

    def newCircle(self, a, radius):
        self.model.add_circle(a, radius)
    # def newSegment(self, segment):
    #     self.segments.append(segment)
    #     self.operations.append(segment)
    #     self.segmentsValue += 1
    #
    # def newCircle(self, circle):
    #     self.circles.append(circle)
    #     self.circles.append(circle)
    #     self.circlesValue += 1


    def newBrush(self, brush):
        self.brushes.append(brush)

    def newUnderType(self, brush, brushundertype):
        try:
            self.brushundertypes[brush].append(brushundertype)
        except:
            self.brushundertypes[brush] = [brushundertype]

    def messageSend(self, message):
        self.statusBar().showMessage(message)

    def brushMessage(self):
        self.messageSend("Brush Type is \"" + self.brushtype + "\"")

    def undertypeMessage(self):
        self.messageSend("Brush Type is \"" + self.brushtype + "\"" + " " * 10 + "Brush UnderType is \"" + self.brushundertype + "\"")

    def paintEvent(self, event):
        paint = QPainter(self)
        paint.setBrush(QColor("black"))
        paint.setPen(QPen(Qt.black, 3))
        paint.setFont(QFont("Decorative", 10))
        for _, point in self.model.points.items():
            paint.drawEllipse(QPoint(point.x, point.y), 2, 2)
        for _, segment in self.model.segments.items():
            paint.drawLine(QPoint(segment.point1.x, segment.point1.y), QPoint(segment.point2.x, segment.point2.y))
        for _, circle in self.model.circles.items():
            circleX = circle.center.x
            circleY = circle.center.y
            distance = circle.radius
            alphaColor = QColor.fromRgbF(0, 0, 0, 0)
            paint.setBrush(alphaColor)
            paint.drawEllipse(float(circleX) - distance, float(circleY) - distance, float(distance) * 2, float(distance) * 2)
            paint.setBrush(QColor("black"))
        self.update()

    def pointDrawing(self, event):
        pass

    def drawingObjects(self, event):
        self.update()
        if self.brushtype == "point":
            self.pointCoords = [event.x(), event.y()]
            self.newPoint(event.x(), event.y())
            #if self.brushundertype == "point":
            #    self.paint.drawEllipse(self.pointCoords[0], self.pointCoords[1], 2, 2)
            #elif self.brushundertype == "pointinobject":
            #    self.pointDrawing()
            self.update()
            self.messageSend("Point succesfully placed")

        if self.brushtype == "segment":
            if not self.pointCoords:
                self.pointCoords = [event.x(), event.y()]
            else:
                if self.pointCoords == [event.x(), event.y()]:
                    self.messageSend("Error")
                else:
                    pointCoords = self.pointCoords
                    self.pointCoords = [event.x(), event.y()]
                    
                    point1 = geometry.Point(pointCoords[0], pointCoords[1])
                    point2 = geometry.Point(self.pointCoords[0], self.pointCoords[1])
                    list = self.correctingPoints(point1, point2, self.model.points)
                    if list:
                        newSegment = geometry.Segment(list[0], list[1])
                    else:
                        newSegment = geometry.Segment(point1, point2)
                    if self.brushundertype == "segment":
                        self.newSegment(newSegment.point1, newSegment.point2)
                        self.messageSend("Segment succesfully placed")
                    elif self.brushundertype == "segmentwithpoints":
                        self.newPoint(point1.x, point1.y)
                        self.newPoint(point2.x, point2.y)
                        self.newSegment(newSegment.point1, newSegment.point2)
                        #paint.drawEllipse(QPoint(pointCoords[0], pointCoords[1]), 2, 2)
                        #paint.drawEllipse(QPoint(self.pointCoords[0], self.pointCoords[1]), 2, 2)
                        self.messageSend("Segment With Points succesfully placed")
                    self.update()
                    self.pointCoords = []

        if self.brushtype == "circle":
            if self.pointCoords == []:
                self.pointCoords = [event.x(), event.y()]
            else:
                pointCoords = self.pointCoords
                self.pointCoords = [event.x(), event.y()]

                #print(pointCoords)
                #print(self.pointCoords)

                center = geometry.Point(pointCoords[0], pointCoords[1])
                list = self.correctingPoints(center, geometry.Point(self.pointCoords[0], self.pointCoords[1]), self.model.points)
                if list:
                    center = list[0]
                    radius = center.distToPoint(list[1])
                else:
                    radius = center.distToPoint(geometry.Point(self.pointCoords[0], self.pointCoords[1]))

                alphaColor = QColor.fromRgbF(0, 0, 0, 0)
                #self.paint.setBrush(alphaColor)

                if self.brushundertype == "radius":
                    #self.paint.drawEllipse(pointCoords[0] - radius, pointCoords[1] - radius, radius*2, radius*2)
                    self.newCircle(center, radius)
                    self.messageSend("Circle succesfully placed")
                
                #self.paint.setBrush(QColor("black"))

                self.update()
                self.pointCoords = []
        self.update()

    def createText(self, event, text):
        #self.paint.setPen(QColor(53, 8, 65))
        #self.paint.setFont(QFont("Decorative", 10))
        #self.paint.drawText(event.rect(), Qt.AlignCenter, text)
        pass

    def setBrushType(self, typeOfBrush, brushObject):
        self.pointCoords = []
        for brush in self.brushes:
            for action in self.brushundertypes[brush]:
                self.toolbar.removeAction(action)
        self.brushtype = typeOfBrush
        self.brushMessage()
        for brush in self.brushes:
            brush.setChecked(False)
        brushObject.setChecked(True)
        self.undertypeBrushes.clear()
        for action in self.brushundertypes[brushObject]:
            self.undertypeBrushes.addAction(action)
            self.toolbar.addAction(action)
            action.setChecked(False)
        if self.brushtype == "point":
            self.brushundertype = "point"
            self.pointPointBrush.setChecked(True)
        elif self.brushtype == "segment":
            self.brushundertype = "segment"
            self.segmentSegmentBrush.setChecked(True)
        elif self.brushtype == "circle":
            self.brushundertype = "radius"
            self.circleRadiusBrush.setChecked(True)

    def setUnderType(self, typeOfUnderType, underTypeObject, brushObject):
        self.brushundertype = typeOfUnderType
        self.undertypeMessage()
        for undertype in self.brushundertypes[brushObject]:
            undertype.setChecked(False)
        underTypeObject.setChecked(True)

    def zoom(self, zoomType):
        if zoomType == "-10":
            if zoomType > 10:
                self.zoomValue -= 10
        elif zoomType == "+10":
            self.zoomValue += 10
        elif zoomType == "100":
            self.zoomValue = 100


    def back(self):
        pass

    def forwards(self):
        pass

    def reset(self):
        self.pointCoords = []


    def mouseMoveEvent(self, event):
        self.update()

    def mousePressEvent(self, event):
        if event.button() == 1:
            self.flag = True
            #self.paint = QPainter(self.image)
            self.drawingObjects(event)
        elif event.button() == 2 or event.button() == 3:
            self.update()

    def mouseReleaseEvent(self, event):
        self.update()


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
        self.undertypeBrushes = QMenu("&Brush Under Types", self)

        self.pointBrush = QAction("&Point", self, checkable=True)
        self.pointBrush.setShortcut("Ctrl+1")
        self.pointBrush.setStatusTip("Take Point Brush")
        self.pointBrush.setToolTip("Take <b>Point</b> Brush")
        self.pointBrush.triggered.connect(lambda event: self.setBrushType("point", self.pointBrush))
        self.pointBrush.setChecked(True)
        self.newBrush(self.pointBrush)

        self.pointPointBrush = QAction("&Point", self, checkable=True)
        self.pointPointBrush.setStatusTip("Making Point")
        self.pointPointBrush.setToolTip("Making <b>Point</b>")
        self.pointPointBrush.triggered.connect(lambda event: self.setUnderType("point", self.pointPointBrush, self.pointBrush))
        self.pointPointBrush.setChecked(True)
        self.newUnderType(self.pointBrush, self.pointPointBrush)

        self.pointInObjectBrush = QAction("&Point In Object", self, checkable=True)
        self.pointInObjectBrush.setStatusTip("Making Point In Object")
        self.pointInObjectBrush.setToolTip("Making <b>Point In Object</b>")
        self.pointInObjectBrush.triggered.connect(lambda event: self.setUnderType("pointinobject", self.pointInObjectBrush, self.pointBrush))
        self.pointInObjectBrush.setChecked(False)
        self.newUnderType(self.pointBrush, self.pointInObjectBrush)


        self.segmentBrush = QAction("&Segment", self, checkable=True)
        self.segmentBrush.setShortcut("Ctrl+2")
        self.segmentBrush.setStatusTip("Take Segment Brush")
        self.segmentBrush.setToolTip("Take <b>Segment</b> Brush")
        self.segmentBrush.triggered.connect(lambda event: self.setBrushType("segment", self.segmentBrush))
        self.segmentBrush.setChecked(False)
        self.newBrush(self.segmentBrush)

        self.segmentSegmentBrush = QAction("&Segment", self, checkable=True)
        self.segmentSegmentBrush.setStatusTip("Making Segment")
        self.segmentSegmentBrush.setToolTip("Making <b>Segment</b>")
        self.segmentSegmentBrush.triggered.connect(lambda event: self.setUnderType("segment", self.segmentSegmentBrush, self.segmentBrush))
        self.segmentSegmentBrush.setChecked(True)
        self.newUnderType(self.segmentBrush, self.segmentSegmentBrush)

        self.segmentWithPointsBrush = QAction("&Segment With Points", self, checkable=True)
        self.segmentWithPointsBrush.setStatusTip("Making Segment With Points")
        self.segmentWithPointsBrush.setToolTip("Making <b>Segment With Points</b>")
        self.segmentWithPointsBrush.triggered.connect(lambda event: self.setUnderType("segmentwithpoints", self.segmentWithPointsBrush, self.segmentBrush))
        self.segmentWithPointsBrush.setChecked(False)
        self.newUnderType(self.segmentBrush, self.segmentWithPointsBrush)


        self.circleBrush = QAction("&Circle", self, checkable=True)
        self.circleBrush.setShortcut("Ctrl+3")
        self.circleBrush.setStatusTip("Take Circle Brush")
        self.circleBrush.setToolTip("Take <b>Circle</b> Brush")
        self.circleBrush.triggered.connect(lambda event: self.setBrushType("circle", self.circleBrush))
        self.circleBrush.setChecked(False)
        self.newBrush(self.circleBrush)

        self.circleRadiusBrush = QAction("&Radius", self, checkable=True)
        self.circleRadiusBrush.setStatusTip("Making Circle With Radius")
        self.circleRadiusBrush.setToolTip("Making Circle With <b>Radius</b>")
        self.circleRadiusBrush.triggered.connect(lambda event: self.setUnderType("radius", self.circleRadiusBrush, self.circleBrush))
        self.circleRadiusBrush.setChecked(True)
        self.newUnderType(self.circleBrush, self.circleRadiusBrush)


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


        self.zoomMinusCommand = QAction("&Zoom - 10%", self)
        self.zoomMinusCommand.setShortcut("Alt+Left")
        self.zoomMinusCommand.triggered.connect(lambda event: self.zoom(zoomType="-10"))

        self.zoomPlusCommand = QAction("&Zoom + 10%", self)
        self.zoomPlusCommand.setShortcut("Alt+Right")
        self.zoomPlusCommand.triggered.connect(lambda event: self.zoom(zoomType="+10"))

        self.zoomReturnCommand = QAction("&Zoom 100%", self)
        self.zoomReturnCommand.setShortcut("Alt+Up")
        self.zoomReturnCommand.triggered.connect(lambda event: self.zoom(zoomType="100"))


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
        self.brushesMenu.addMenu(self.undertypeBrushes)

        self.typeBrushes.addAction(self.pointBrush)
        self.typeBrushes.addAction(self.segmentBrush)
        self.typeBrushes.addAction(self.circleBrush)

        self.undertypeBrushes.addAction(self.pointPointBrush)
        self.undertypeBrushes.addAction(self.pointInObjectBrush)

        self.editMenu = self.menubar.addMenu("&Edit")
        self.editMenu.addAction(self.backCommand)
        self.editMenu.addAction(self.forwardCommand)

        self.zoomMenu = self.menubar.addMenu("&Zoom")
        self.zoomMenu.addAction(self.zoomMinusCommand)
        self.zoomMenu.addAction(self.zoomPlusCommand)
        self.zoomMenu.addSeparator()
        self.zoomMenu.addAction(self.zoomReturnCommand)

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

        self.setBrushType("point", self.pointBrush)
        self.messageSend("Paint")
    @staticmethod
    def correctingPoints(start, end, points):
        error = 4
        if points:
            for _, i in points.items():
                #print(start.x, start.y, end.x, end.y, i.x, i.y)
                if ((start.x <= i.x + error) and (start.x >= i.x - error)) and ((start.y <= i.y + error) and (start.y >= i.y - error)):
                    start.x = i.x
                    start.y = i.y
                if ((end.x <= i.x + error) and (end.x >= i.x - error)) and ((end.y <= i.y + error) and (end.y >= i.y - error)):
                    end.x = i.x
                    end.y = i.y
            list = [start, end]
            return list

app = QApplication(sys.argv)
interface = MainWidget()
sys.exit(app.exec_())
