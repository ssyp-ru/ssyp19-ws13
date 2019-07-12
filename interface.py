from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor, QFont, QImage, QPen, QBrush, QTextCursor
from PyQt5.QtCore import Qt, QPoint, QRect
import sys
import webbrowser
import geom as geometry
from model import Model

class WidgetWithText(QWidget):
    def __init__(self, text, title):
        super().__init__()
        self.text = text
        self.title = title
        self.initUI()

    def centering(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):
        self.lbl = QLabel(self)
        self.lbl.setText(self.text)
        self.lbl.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.lbl.move(30, 30)

        self.setWindowTitle(self.title)
        self.setFixedSize(400, 400)
        self.show()
        self.centering()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.model = Model()
        self.console = Console(self.model)
        self.brushes = []
        self.brushundertypes = {}
        self.brushtype = "point"
        self.brushundertype = "point"
        self.flag = False
        self.pointBrushColor = QColor(255, 0, 0)
        self.dependingPointBrushColor = QColor(255, 0, 255)
        self.segmentBrushColor = Qt.black
        self.textColor = Qt.black
        self.backgroundColor = Qt.white
        self.lastname = -1
        self.pointCoords = []
        self.fieldWidth = 900
        self.fieldHeight = 600
        self.zoomValue = 100
        self.operations = []
        self.selected = set()
        self.competitorFirstElement = None
        self.table = False

        self.initUI()

    def newPoint(self, x: float, y: float, alloperationsInserting=True):
        point = self.model.add_point(x, y)
        self.model.operations.append(geometry.Point(x, y))
        if alloperationsInserting:
            self.model.alloperations.append(geometry.Point(x, y))
        return point

    def newSegment(self, pointstart: geometry.Point, pointend: geometry.Point, alloperationsInserting=True):
        segment = self.model.check_segment(pointstart, pointend)
        self.model.operations.append(geometry.Segment(pointstart, pointend))
        if alloperationsInserting:
            self.model.alloperations.append(geometry.Segment(pointstart, pointend))
        return segment

    def newCircle(self, segment: geometry.Segment, alloperationsInserting=True):
        circle = self.model.check_circle(segment)
        self.model.operations.append(geometry.Circle(segment))
        if alloperationsInserting:
            self.model.alloperations.append(geometry.Circle(segment))
        return circle

    def newCompetitor(self, segment1, segment2):
        pass

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
        paint.drawImage(0,0, self.image)
        paint.setBrush(QBrush(self.backgroundColor))
        paint.drawRect(-20, 20, self.fieldWidth+30, self.fieldHeight+30)
        paint.setBrush(self.pointBrushColor)
        paint.setPen(QPen(self.segmentBrushColor, 2))
        for segment in self.model.segments.values():
            self.segmentDrawing(paint, segment.point1, segment.point2)
        for circle in self.model.circles.values():
            self.circleDrawing(paint, circle.center.x, circle.center.y, circle.radius)
        for point in self.model.points.values():
            if str(type(point)) == "<class \'geom.Point\'>":
                self.pointDrawing(paint, point.x, point.y, str(point))
            else:
                self.dependingPointDrawing(paint, point.x, point.y, str(point))
        self.update()

    def pointCreating(self, x, y):
        p = self.newPoint(x, y)
        self.messageSend("Point succesfully placed" + " " * 10 + str(p))

    def pointInObjectCreating(self, x, y):
        self.newPoint(x, y)
        self.messageSend("Point succesfully placed" + " " * 10 + str(x) + ", " + str(y))

    def segmentCreating(self, point1, point2):
        n_point1, n_point2 = self.model.correcting_points(point1, point2)
        if n_point1 is point1:
            n_point1 = self.newPoint(point1.x, point1.y)
        if n_point2 is point2:
            n_point2 = self.newPoint(point2.x, point2.y)
        segment = self.newSegment(n_point1, n_point2)
        if segment is not None:
            self.messageSend(f"Segment With Points succesfully placed {' ' * 10}{segment.point1}-{segment.point2}")

    def circleWithRadiusCreating(self, center, point2):
        n_center, n_point2 = self.model.correcting_points(center, point2)
        if self.brushundertype == "radius":
            if n_center is center:
                n_center = self.newPoint(center.x, center.y)
            if n_point2 is point2:
                n_point2 = self.newPoint(point2.x, point2.y)
            circle = self.newCircle(geometry.Segment(n_center, n_point2))
            self.messageSend(f"Circle succesfully placed with{' '*10}center: {circle.center}; radius: {circle.radius}; point: {circle.point}")

    def pointControl(self, event):
        if self.brushundertype == "point":
            self.pointCreating(event.x(), event.y())
        elif self.brushundertype == "pointinobject":
            point = self.model.correctingPoints(geometry.Point(event.x(), event.y()),\
                                                self.model.segments,
                                                self.model.circles)
            if point is not None:
                self.pointInObjectCreating(point.x, point.y)
        self.update()

    def segmentContol(self, event):
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
                if self.brushundertype == "segment":
                    self.segmentCreating(point1, point2)
                elif self.brushundertype == "segmentwithpoints":
                    self.segmentWithPointsCreating(point1, point2)
                self.update()
                self.pointCoords = []

    def circleControl(self, event):
        if self.pointCoords == []:
            self.pointCoords = [event.x(), event.y()]
        else:
            firstPointCoords = self.pointCoords
            self.pointCoords = [event.x(), event.y()]

            center = geometry.Point(firstPointCoords[0], firstPointCoords[1])
            pointOnCircle = geometry.Point(self.pointCoords[0], self.pointCoords[1])

            self.circleWithRadiusCreating(center, pointOnCircle)

            self.update()
            self.pointCoords = []

    def competitorControl(self, event):
        newPoint = geometry.Point(event.x(), event.y())
        for segment in self.model.segments.values():
            if segment.pointBelongs(newPoint):
                if segment not in self.selected:
                    if not self.pointCoords:
                        self.pointCoords = [event.x(), event.y()]
                    self.selected.add(segment)
                    self.messageSend("Segment selected")
                else:
                    self.messageSend('Error')

    def pointDrawing(self, qp, x, y, name):
        qp.setBrush(self.pointBrushColor)
        qp.setPen(QPen(self.pointBrushColor, 2))
        qp.drawEllipse(QPoint(x, y), 2, 2)
        qp.setBrush(self.textColor)
        qp.setPen(QPen(self.textColor, 2))
        qp.drawText(x + 3, y - 3, name)

    def dependingPointDrawing(self, qp, x, y, name):
        qp.setBrush(self.dependingPointBrushColor)
        qp.setPen(QPen(self.dependingPointBrushColor, 2))
        qp.drawEllipse(QPoint(x, y), 3, 3)
        qp.setBrush(self.textColor)
        qp.setPen(QPen(self.textColor, 2))
        qp.drawText(x + 3, y - 3, name)

    def segmentDrawing(self, qp, point1, point2):
        qp.setBrush(self.segmentBrushColor)
        qp.setPen(QPen(self.segmentBrushColor, 2))
        qp.drawLine(QPoint(point1.x, point1.y), QPoint(point2.x, point2.y))

    def circleDrawing(self, qp, centerX, centerY, distance):
        alphaColor = QColor.fromRgbF(0, 0, 0, 0)
        qp.setBrush(alphaColor)
        qp.drawEllipse(float(centerX) - distance, float(centerY) - distance, float(distance) * 2, float(distance) * 2)
        qp.setBrush(self.pointBrushColor)

    def drawingObjects(self, event):
        self.update()
        if self.brushtype == "point":
            self.pointControl(event)
        if self.brushtype == "segment":
            self.segmentContol(event)
        if self.brushtype == "circle":
            self.circleControl(event)
        if self.brushtype == "competitor":
            self.competitorControl(event)
        self.update()

    def createText(self, event, text):
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

    def zoom(self, value):
        if value == 0:
            self.zoomValue = 100
        elif self.zoomValue < abs(value) and value < 0 or value > 0:
            self.zoomValue += value



    def back(self):
        if len(self.model.operations):
            operation = self.model.operations[len(self.model.operations)-1]
            operationType = str(type(operation))
            if operationType == "<class \'geom.Point\'>":
                objectList = list(self.model.points.keys())
                name = objectList[len(objectList)-1][0]
                del(self.model.points[name])
                self.messageSend("Point succesfully deleted")

            elif operationType == "<class \'geom.Segment\'>":
                objectList = list(self.model.segments.keys())
                name = objectList[len(objectList)-1][0]
                del(self.model.segments[name])
                self.messageSend("Segment succesfully deleted")

            elif operationType == "<class \'geom.Circle\'>":
                objectList = list(self.model.circles.keys())
                name = objectList[len(objectList)-1][0]
                del(self.model.circles[name])
                self.messageSend("Circle succesfully deleted")

            self.model.operations.pop(len(self.model.operations)-1)

    def forwards(self):
        if len(self.model.operations) < len(self.model.alloperations):
            operation = self.model.alloperations[len(self.model.operations)]
            operationType = str(type(operation))
            if operationType == "<class \'geom.Point\'>":
                self.newPoint(operation.x, operation.y, alloperationsInserting=False)
            elif operationType == "<class \'geom.Segment\'>":
                self.newSegment(operation.point1, operation.point2, alloperationsInserting=False)
            elif operationType == "<class \'geom.Circle\'>":
                self.newCircle(operation.center, operation.radius, alloperationsInserting=False)

    def reset(self):
        self.pointCoords = []
        self.selected = set()

    def prove(self):
        solutions = self.model.translator.connector.get_n_ans_new("isCongruent(X, Y)")[0]
        for el in solutions[2::]:
            point1 = self.model.findPointFromName(el['X'].args[0])
            point2 = self.model.findPointFromName(el['X'].args[1])
            point3 = self.model.findPointFromName(el['Y'].args[0])
            point4 = self.model.findPointFromName(el['Y'].args[1])
            Xsegment = geometry.Segment(point1, point2)
            Ysegment = geometry.Segment(point3, point4)
            # print(XsYsegment)
            if Xsegment not in self.model.CongruentSegments:
                self.model.CongruentSegments[Xsegment] = set()
            self.model.CongruentSegments[Xsegment].add(Ysegment)
        # print(self.model.getCongruencyClass(0))
        # self.model.correctingScheme()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.flag = True
            self.drawingObjects(event)
        elif event.button() == Qt.RightButton:
            self.update()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_QuoteLeft:
            self.console.show()
        elif event.key() == Qt.Key_D:
            print(len(self.model.segments))
            for v in self.model.segments.values():
                print(v)


    def mouseReleaseEvent(self, event):
        self.update()


    def centering(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def clear(self):
        self.paint = QPainter(self.image)
        self.paint.setBrush(QBrush(self.backgroundColor))
        for point in list(self.model.points.keys()):
            del(self.model.points[point])
        for segment in list(self.model.segments.keys()):
            del(self.model.segments[segment])
        for circle in list(self.model.circles.keys()):
            del(self.model.circles[circle])
        self.paint.drawRect(-20, 20, self.fieldWidth+30, self.fieldHeight+30)
        self.model.reset_prolog()

    def reference(self):
        webbrowser.open("reference.html")

    def authors(self):
        pass

    def backgroundColorSelect(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.backgroundColor = color

    def foregroundPointColorSelect(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.pointBrushColor = color

    def foregroundSegmentColorSelect(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.segmentBrushColor = color

    def foregroundTextColorSelect(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.textColor = color

    def foregroundDependingPointColorSelect(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.dependingPointBrushColor = color

    def fileActionsCreating(self):
        self.newFileAct = QAction("&New", self)
        self.newFileAct.setShortcut("Ctrl+N")
        self.newFileAct.setStatusTip("Creating New File")
        self.newFileAct.setToolTip("Creating <b>New</b> File")
        self.newFileAct.triggered.connect(self.clear)

        self.quitAct = QAction("&Quit", self)
        self.quitAct.setShortcut("Ctrl+Q")
        self.quitAct.setStatusTip("Quit program")
        self.quitAct.setToolTip("<b>Quit</b> program")
        self.quitAct.triggered.connect(qApp.quit)

    def pointBrushActionsCreating(self):
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

    def segmentBrushActionsCreating(self):
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

    def circlesBrushActionsCreating(self):
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

    def competitorBrushActionCreating(self):
        self.competitorBrush = QAction("&Competitor", self, checkable=True)
        self.competitorBrush.setStatusTip("Set competitor")
        self.competitorBrush.setToolTip("Set <b>competitor</b>")
        self.competitorBrush.triggered.connect(lambda event: self.setBrushType("competitor", self.competitorBrush))
        self.competitorBrush.setChecked(False)
        self.newBrush(self.competitorBrush)

        self.competitorNormalBrush = QAction("&Competitor", self, checkable=True)
        self.competitorNormalBrush.setStatusTip("Set competitor")
        self.competitorNormalBrush.setToolTip("Set <b>competitor</b>")
        self.competitorNormalBrush.triggered.connect(lambda event: self.setUnderType("competitor", self.competitorNormalBrush, self.competitorBrush))
        self.competitorNormalBrush.setChecked(True)
        self.newUnderType(self.competitorBrush, self.competitorNormalBrush)

    def editActionsCreating(self):
        self.backCommand = QAction("&Back", self)
        self.backCommand.setShortcut("Ctrl+Z")
        self.backCommand.setStatusTip("Return back")
        self.backCommand.setToolTip("Return <b>back</b>")
        self.backCommand.triggered.connect(self.back)

        self.forwardCommand = QAction("&Forwards", self)
        self.forwardCommand.setShortcut("Shift+Ctrl+Z")
        self.forwardCommand.setStatusTip("Return forwards")
        self.forwardCommand.setToolTip("Return <b>forwards</b>")
        self.forwardCommand.triggered.connect(self.forwards)

        self.resetCommand = QAction("&Reset", self)
        self.resetCommand.setShortcut("Ctrl+R")
        self.resetCommand.setStatusTip("Reset point")
        self.resetCommand.setToolTip("<b>Reset</b> point")
        self.resetCommand.triggered.connect(self.reset)

        self.proveCommand = QAction("&Prove", self)
        self.proveCommand.setShortcut("Ctrl+P")
        self.proveCommand.setStatusTip("Proved")
        self.proveCommand.setToolTip("<b>Prove</b>")
        self.proveCommand.triggered.connect(self.prove)


    def viewActionsCreating(self):
        self.backgroundColorCommand = QAction("&Background", self)
        self.backgroundColorCommand.setShortcut("Alt+B")
        self.backgroundColorCommand.setStatusTip("Change your background color")
        self.backgroundColorCommand.setToolTip("Change your <b>background color</b>")
        self.backgroundColorCommand.triggered.connect(self.backgroundColorSelect)

        self.foregroundPointColorCommand = QAction("&Foreground Point", self)
        self.foregroundPointColorCommand.setShortcut("Shift+P")
        self.foregroundPointColorCommand.setStatusTip("Change your point color")
        self.foregroundPointColorCommand.setToolTip("Change your <b>point color</b>")
        self.foregroundPointColorCommand.triggered.connect(self.foregroundPointColorSelect)

        self.foregroundDependingPointColorCommand = QAction("&Foreground Depending Point", self)
        self.foregroundDependingPointColorCommand.setShortcut("Shift+D")
        self.foregroundDependingPointColorCommand.setStatusTip("Change your depending point color")
        self.foregroundDependingPointColorCommand.setToolTip("Change your <b>depending point color</b>")
        self.foregroundDependingPointColorCommand.triggered.connect(self.foregroundDependingPointColorSelect)

        self.foregroundSegmentColorCommand = QAction("&Foreground Segment", self)
        self.foregroundSegmentColorCommand.setShortcut("Shift+S")
        self.foregroundSegmentColorCommand.setStatusTip("Change your segment color")
        self.foregroundSegmentColorCommand.setToolTip("Change your <b>segment color</b>")
        self.foregroundSegmentColorCommand.triggered.connect(self.foregroundSegmentColorSelect)

        self.foregroundTextColorCommand = QAction("&Foreground Text", self)
        self.foregroundTextColorCommand.setShortcut("Shift+T")
        self.foregroundTextColorCommand.setStatusTip("Change your text color")
        self.foregroundTextColorCommand.setToolTip("Change your <b>text color</b>")
        self.foregroundTextColorCommand.triggered.connect(self.foregroundTextColorSelect)

    def helpActionsCreating(self):
        self.referenceCommand = QAction("&Reference", self)
        self.referenceCommand.setShortcut("F1")
        self.referenceCommand.setStatusTip("Reference show")
        self.referenceCommand.setToolTip("<b>Reference</b> show")
        self.referenceCommand.triggered.connect(self.reference)

        self.authorsCommand = QAction("&Authors", self)
        self.authorsCommand.setStatusTip("Authors show")
        self.authorsCommand.setToolTip("<b>Authors</b> show")
        self.authorsCommand.triggered.connect(self.authors)

    def menuCreating(self):
        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu("&File")
        self.fileMenu.addAction(self.newFileAct)

        self.brushesMenu = self.menubar.addMenu("&Brushes")
        self.typeBrushes = QMenu("&Brush Types", self)
        self.undertypeBrushes = QMenu("&Brush Under Types", self)
        self.brushesMenu.addMenu(self.typeBrushes)
        self.brushesMenu.addMenu(self.undertypeBrushes)

        self.typeBrushes.addAction(self.pointBrush)
        self.typeBrushes.addAction(self.segmentBrush)
        self.typeBrushes.addAction(self.circleBrush)
        self.typeBrushes.addAction(self.competitorBrush)

        self.undertypeBrushes.addAction(self.pointPointBrush)
        self.undertypeBrushes.addAction(self.pointInObjectBrush)

        self.editMenu = self.menubar.addMenu("&Edit")
        self.editMenu.addAction(self.backCommand)
        self.editMenu.addAction(self.forwardCommand)
        self.editMenu.addAction(self.resetCommand)
        self.editMenu.addAction(self.proveCommand)

        self.viewMenu = self.menubar.addMenu("&View")
        self.foregroundMenu = QMenu("&Foreground", self)
        self.viewMenu.addAction(self.backgroundColorCommand)
        self.viewMenu.addMenu(self.foregroundMenu)
        self.foregroundMenu.addAction(self.foregroundPointColorCommand)
        self.foregroundMenu.addAction(self.foregroundDependingPointColorCommand)
        self.foregroundMenu.addAction(self.foregroundSegmentColorCommand)
        self.foregroundMenu.addAction(self.foregroundTextColorCommand)

        self.helpMenu = self.menubar.addMenu("&Help")
        self.helpMenu.addAction(self.referenceCommand)
        self.helpMenu.addAction(self.authorsCommand)

    def toolbarFilling(self):
        self.toolbar = self.addToolBar("Toolbar")
        self.toolbar.setMovable(False)
        self.toolbar.setToolTip("<b>Toolbar</b>")
        self.toolbar.setStatusTip("Toolbar")
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.pointBrush)
        self.toolbar.addAction(self.segmentBrush)
        self.toolbar.addAction(self.circleBrush)
        self.toolbar.addAction(self.competitorBrush)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.backCommand)
        self.toolbar.addAction(self.forwardCommand)
        self.toolbar.addAction(self.resetCommand)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.newFileAct)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.quitAct)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.proveCommand)
        self.toolbar.addSeparator()

    def initUI(self):
        self.setFixedSize(self.fieldWidth, self.fieldHeight)
        self.saveState()
        self.setWindowTitle("Prototype")
        self.show()
        self.centering()

        self.image = QImage(self.width(), self.height(), QImage.Format_ARGB32)
        self.image.fill(QColor(255, 255, 255))

        self.setToolTip("<b>Drawing Place</b>")

        self.fileActionsCreating()
        self.pointBrushActionsCreating()
        self.segmentBrushActionsCreating()
        self.circlesBrushActionsCreating()
        self.competitorBrushActionCreating()
        self.editActionsCreating()
        self.viewActionsCreating()
        self.helpActionsCreating()
        self.menuCreating()
        self.toolbarFilling()

        self.setBrushType("point", self.pointBrush)
        self.messageSend("Paint")


class Console(QTextEdit):

    def __init__(self, model):
        super().__init__()
        self.resize(600, 300)
        self.setAlignment(Qt.AlignTop)
        self.setWindowTitle('Console')
        self.setFont(QFont('Hack', 14))
        self.model = model

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            s = self.toPlainText()
            try:
                query = s.rsplit('\n', maxsplit=1)[-1]
                s += '\n'
                answer = self.model.translator.connector.prolog.query(query)
                for sol in answer:
                    s += '; '.join(list(map(str, sol.values()))) + '\n'
            except Exception as f:
                s += str(f) + '\n'
            finally:
                self.setText(s)
                self.moveCursor(QTextCursor.End)
        else:
            super().keyPressEvent(event)

class MainWidget(QWidget):
    pass

app = QApplication(sys.argv)
interface = MainWindow()
sys.exit(app.exec_())
