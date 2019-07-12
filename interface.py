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
        self.console = Console(model=self.model, parent=self)
        self.console.move(0, 600)
        self.console.resize(900, 100)
        self.canvas = Canvas(parent=self, model=self.model)
        self.canvas.resize(900, 600)
        self.brushes = []
        self.brushundertypes = {}
        self.brushtype = "point"
        self.brushundertype = "point"
        self.flag = False
        self.lastname = -1
        self.pointCoords = []
        self.fieldWidth = 900
        self.fieldHeight = 735
        self.zoomValue = 100
        self.operations = []
        self.programTitle = "Prototype"

        self.select = list()
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
        self.messageSend(
            "Brush Type is \"" + self.brushtype + "\"" + " " * 10 + "Brush UnderType is \"" + self.brushundertype + "\"")

    def setBrushType(self, typeOfBrush, brushObject):
        self.pointCoords = []
        for brush in self.brushes:
            for action in self.brushundertypes[brush]:
                self.toolbar.removeAction(action)
        self.brushtype = typeOfBrush
        self.brushMessage()
        self.select = list()
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
        elif self.brushtype == "congruency":
            self.brushundertype = "congruency"
            self.congruencyNormalBrush.setChecked(True)

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

    def reset(self):
        self.pointCoords = []
        self.select = list()

    def addCongruency(self):
        if not self.select:
            return
        s = self.select[0]
        for segment in self.select:
            if segment is not s:
                segment1 = f'segment({segment.point1.name}, {segment.point2.name})'
                segment2 = f'segment({s.point1.name}, {s.point2.name})'
                self.model.translator.connector.prolog.assertz(f'congruent({segment1}, {segment2})')
                s = segment
        self.model.updateCongruencyClasses()
    def fixScheme(self):
        self.model.correctingScheme()
        self.model.updateEverything()
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.flag = True
        elif event.button() == Qt.RightButton:
            self.update()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_QuoteLeft:
            self.console.show()

    def mouseReleaseEvent(self, event):
        self.update()

    def centering(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def clear(self):
        self.model.reset_prolog()
        self.paint = QPainter(self.image)
        self.paint.setBrush(QBrush(self.canvas.backgroundColor))
        self.select = list()
        for point in tuple(self.model.points.keys()):
            del (self.model.points[point])
        for segment in tuple(self.model.segments.keys()):
            del (self.model.segments[segment])
        for circle in tuple(self.model.circles.keys()):
            del (self.model.circles[circle])
        self.paint.drawRect(-20, 20, self.fieldWidth + 30, self.fieldHeight + 30)

    def reference(self):
        webbrowser.open("reference.html")

    def authors(self):
        pass

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
        self.pointPointBrush.triggered.connect(
            lambda event: self.setUnderType("point", self.pointPointBrush, self.pointBrush))
        self.pointPointBrush.setChecked(True)
        self.newUnderType(self.pointBrush, self.pointPointBrush)

        self.pointInObjectBrush = QAction("&Point In Object", self, checkable=True)
        self.pointInObjectBrush.setStatusTip("Making Point In Object")
        self.pointInObjectBrush.setToolTip("Making <b>Point In Object</b>")
        self.pointInObjectBrush.triggered.connect(
            lambda event: self.setUnderType("pointinobject", self.pointInObjectBrush, self.pointBrush))
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
        self.segmentSegmentBrush.triggered.connect(
            lambda event: self.setUnderType("segment", self.segmentSegmentBrush, self.segmentBrush))
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
        self.circleRadiusBrush.triggered.connect(
            lambda event: self.setUnderType("radius", self.circleRadiusBrush, self.circleBrush))
        self.circleRadiusBrush.setChecked(True)
        self.newUnderType(self.circleBrush, self.circleRadiusBrush)

    def congruencyBrushActionCreating(self):
        self.congruencyBrush = QAction("&Congruency", self, checkable=True)
        self.congruencyBrush.setShortcut("Ctrl+4")
        self.congruencyBrush.setStatusTip("Set congruency")
        self.congruencyBrush.setToolTip("Set <b>congruency</b>")
        self.congruencyBrush.triggered.connect(lambda event: self.setBrushType("congruency", self.congruencyBrush))
        self.congruencyBrush.setChecked(False)
        self.newBrush(self.congruencyBrush)

        self.congruencyNormalBrush = QAction("&Congruency", self, checkable=True)
        self.congruencyNormalBrush.setStatusTip("Set congruency")
        self.congruencyNormalBrush.setToolTip("Set <b>congruency</b>")
        self.congruencyNormalBrush.triggered.connect(
            lambda event: self.setUnderType("congruency", self.congruencyNormalBrush, self.congruencyBrush))
        self.congruencyNormalBrush.setChecked(True)
        self.newUnderType(self.congruencyBrush, self.congruencyNormalBrush)

    def editActionsCreating(self):

        self.resetCommand = QAction("&Reset", self)
        self.resetCommand.setShortcut("Ctrl+R")
        self.resetCommand.setStatusTip("Reset point")
        self.resetCommand.setToolTip("<b>Reset</b> point")
        self.resetCommand.triggered.connect(self.reset)

        self.addCongruencyCommand = QAction("Add Con&gruency", self)
        self.addCongruencyCommand.setShortcut("Ctrl+G")
        self.addCongruencyCommand.setStatusTip("Congruency added")
        self.addCongruencyCommand.setToolTip("<b>Add Congruency</b>")
        self.addCongruencyCommand.triggered.connect(self.addCongruency)

        self.fixSchemeCommand = QAction("Fix Scheme", self)
        self.fixSchemeCommand.setShortcut("Ctrl+Space")
        self.fixSchemeCommand.setStatusTip("Oops")
        self.fixSchemeCommand.setToolTip("<b>Fix Scheme</b>")
        self.fixSchemeCommand.triggered.connect(self.fixScheme)

    def viewActionsCreating(self):
        self.backgroundColorCommand = QAction("&Background", self)
        self.backgroundColorCommand.setShortcut("Alt+B")
        self.backgroundColorCommand.setStatusTip("Change your background color")
        self.backgroundColorCommand.setToolTip("Change your <b>background color</b>")
        self.backgroundColorCommand.triggered.connect(self.canvas.backgroundColorSelect)

        self.foregroundPointColorCommand = QAction("&Foreground Point", self)
        self.foregroundPointColorCommand.setShortcut("Alt+P")
        self.foregroundPointColorCommand.setStatusTip("Change your point color")
        self.foregroundPointColorCommand.setToolTip("Change your <b>point color</b>")
        self.foregroundPointColorCommand.triggered.connect(self.canvas.foregroundPointColorSelect)

        self.foregroundDependingPointColorCommand = QAction("&Foreground Depending Point", self)
        self.foregroundDependingPointColorCommand.setShortcut("Alt+D")
        self.foregroundDependingPointColorCommand.setStatusTip("Change your depending point color")
        self.foregroundDependingPointColorCommand.setToolTip("Change your <b>depending point color</b>")
        self.foregroundDependingPointColorCommand.triggered.connect(self.canvas.foregroundDependingPointColorSelect)

        self.foregroundSegmentColorCommand = QAction("&Foreground Segment", self)
        self.foregroundSegmentColorCommand.setShortcut("Alt+S")
        self.foregroundSegmentColorCommand.setStatusTip("Change your segment color")
        self.foregroundSegmentColorCommand.setToolTip("Change your <b>segment color</b>")
        self.foregroundSegmentColorCommand.triggered.connect(self.canvas.foregroundSegmentColorSelect)

        self.foregroundTextColorCommand = QAction("&Foreground Text", self)
        self.foregroundTextColorCommand.setShortcut("Alt+T")
        self.foregroundTextColorCommand.setStatusTip("Change your text color")
        self.foregroundTextColorCommand.setToolTip("Change your <b>text color</b>")
        self.foregroundTextColorCommand.triggered.connect(self.canvas.foregroundTextColorSelect)

        self.foregroundSelectionSegmentsCommand = QAction("&Foreground Selecting Segments", self)
        self.foregroundSelectionSegmentsCommand.setShortcut("Alt+C")
        self.foregroundSelectionSegmentsCommand.setStatusTip("Change your selecting segments color")
        self.foregroundSelectionSegmentsCommand.setToolTip("Change your <b>selecting segments color</b>")
        self.foregroundSelectionSegmentsCommand.triggered.connect(self.canvas.foregroundSelectionSegmentsSelect)

        self.textFontCommand = QAction("&Font Text", self)
        self.textFontCommand.setStatusTip("Change your font")
        self.textFontCommand.setToolTip("Change your <b>font</b>")
        self.textFontCommand.triggered.connect(self.canvas.fontSelect)

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
        self.typeBrushes.addAction(self.congruencyBrush)

        self.undertypeBrushes.addAction(self.pointPointBrush)
        self.undertypeBrushes.addAction(self.pointInObjectBrush)

        self.editMenu = self.menubar.addMenu("&Edit")
        self.editMenu.addAction(self.resetCommand)
        self.editMenu.addAction(self.addCongruencyCommand)
        self.editMenu.addAction(self.fixSchemeCommand)

        self.viewMenu = self.menubar.addMenu("&View")
        self.foregroundMenu = QMenu("&Foreground", self)
        self.viewMenu.addAction(self.backgroundColorCommand)
        self.viewMenu.addMenu(self.foregroundMenu)
        self.foregroundMenu.addAction(self.foregroundPointColorCommand)
        self.foregroundMenu.addAction(self.foregroundDependingPointColorCommand)
        self.foregroundMenu.addAction(self.foregroundSegmentColorCommand)
        self.foregroundMenu.addAction(self.foregroundTextColorCommand)
        self.foregroundMenu.addAction(self.foregroundSelectionSegmentsCommand)
        self.viewMenu.addAction(self.textFontCommand)

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
        self.toolbar.addAction(self.congruencyBrush)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.resetCommand)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.newFileAct)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.quitAct)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.addCongruencyCommand)
        self.toolbar.addSeparator()

    def initUI(self):
        self.setFixedSize(self.fieldWidth, self.fieldHeight)
        self.saveState()
        self.setWindowTitle(self.programTitle)
        self.show()
        self.centering()

        self.image = QImage(self.width(), self.height(), QImage.Format_ARGB32)
        self.image.fill(QColor(64, 0, 128))

        self.setToolTip("<b>Drawing Place</b>")

        self.fileActionsCreating()
        self.pointBrushActionsCreating()
        self.segmentBrushActionsCreating()
        self.circlesBrushActionsCreating()
        self.congruencyBrushActionCreating()
        self.editActionsCreating()
        self.viewActionsCreating()
        self.helpActionsCreating()
        self.menuCreating()
        self.toolbarFilling()

        QApplication.setOverrideCursor(Qt.CrossCursor)

        QApplication.setOverrideCursor(Qt.CrossCursor)

        self.setBrushType("point", self.pointBrush)
        self.messageSend("Paint")


class Console(QTextEdit):
    def __init__(self, model, parent):
        super().__init__(parent=parent)
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
                    s += '; '.join(list(map(str, map(lambda x: self.model.points[x] if isinstance(x, geometry.Point) else x,sol.values())))) + '\n'
            except Exception as f:
                s += str(f) + '\n'
            finally:
                self.setText(s)
                self.moveCursor(QTextCursor.End)
        else:
            super().keyPressEvent(event)


class Canvas(QWidget):
    def __init__(self, parent, model):
        super().__init__(parent=parent)
        self.pointBrushColor = QColor(255, 0, 0)
        self.dependingPointBrushColor = QColor(255, 0, 255)
        self.segmentBrushColor = Qt.black
        self.textColor = Qt.black
        self.backgroundColor = Qt.white
        self.selectionSegmentBrushColor = QColor(0, 255, 255)
        self.textFont = QFont("Helvetica", 12)
        self.parent = parent
        self.model = model

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

    def foregroundSelectionSegmentsSelect(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.selectionSegmentBrushColor = color

    def fontSelect(self):
        (font, ok) = QFontDialog.getFont()
        if ok:
            self.textFont = QFont(font)

    def paintEvent(self, event):
        paint = QPainter(self)
        paint.drawImage(0, 0, self.parent.image)
        paint.setBrush(QBrush(self.backgroundColor))
        paint.drawRect(-20, 0, self.parent.fieldWidth+30, self.parent.fieldHeight+30)
        paint.setBrush(self.pointBrushColor)
        paint.setPen(QPen(self.segmentBrushColor, 2))
        for segment in self.parent.model.segments.values():
            if self.parent.select is not None:
                if segment in self.parent.select:
                    self.selectionSegmentDrawing(paint, segment.point1, segment.point2)
                else:
                    self.segmentDrawing(paint, segment.point1, segment.point2)
            else:
                self.segmentDrawing(paint, segment.point1, segment.point2)
        for circle in self.parent.model.circles.values():
            self.circleDrawing(paint, circle.center.x, circle.center.y, circle.radius)
        for point in self.parent.model.points.values():
            self.pointDrawing(paint, point.x, point.y, str(point))
        for point in self.parent.model.dependpoints.values():
            self.dependingPointDrawing(paint, point.x, point.y, str(point))
            # if str(type(point)) == "<class \'geom.Point\'>":
            #     self.pointDrawing(paint, point.x, point.y, str(point))
            # else:
            #     self.dependingPointDrawing(paint, point.x, point.y, str(point))
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawingObjects(event)

    def drawingObjects(self, event):
        if self.parent.brushtype == "point":
            self.pointControl(event)
        if self.parent.brushtype == "segment":
            self.segmentContol(event)
        if self.parent.brushtype == "circle":
            self.circleControl(event)
        if self.parent.brushtype == "congruency":
            self.congruencyControl(event)
        self.update()

    def pointControl(self, event):
        if self.parent.brushundertype == "point":
            self.pointCreating(event.x(), event.y())
        elif self.parent.brushundertype == "pointinobject":
            point = self.parent.model.correctingPoints(geometry.Point(event.x(), event.y()), \
                                                       self.parent.model.segments,
                                                       self.parent.model.circles)
            self.pointInObjectCreating(point.x, point.y)
        self.update()

    def segmentContol(self, event):
        if not self.parent.pointCoords:
            self.parent.pointCoords = [event.x(), event.y()]
        else:
            if self.parent.pointCoords == [event.x(), event.y()]:
                self.parent.messageSend("Error")
            else:
                pointCoords = self.parent.pointCoords
                self.parent.pointCoords = [event.x(), event.y()]
                point1 = geometry.Point(pointCoords[0], pointCoords[1])
                point2 = geometry.Point(self.parent.pointCoords[0], self.parent.pointCoords[1])
                if self.parent.brushundertype == "segment":
                    self.segmentCreating(point1, point2)
                self.update()
                self.parent.pointCoords = []

    def circleControl(self, event):
        if self.parent.pointCoords == []:
            self.parent.pointCoords = [event.x(), event.y()]
        else:
            firstPointCoords = self.parent.pointCoords
            self.parent.pointCoords = [event.x(), event.y()]

            center = geometry.Point(firstPointCoords[0], firstPointCoords[1])
            pointOnCircle = geometry.Point(self.parent.pointCoords[0], self.parent.pointCoords[1])

            self.circleWithRadiusCreating(center, pointOnCircle)

            self.update()
            self.parent.pointCoords = []

    def congruencyControl(self, event):
            newPoint = geometry.Point(event.x(), event.y())
            for segment in self.parent.model.segments.values():
                if segment.pointBelongs(newPoint):
                    if segment not in self.parent.select:
                        if not self.parent.pointCoords:
                            self.parent.pointCoords = [event.x(), event.y()]
                        self.parent.select.append(segment)
                        self.parent.messageSend("Segment selected")
                    else:
                        self.parent.messageSend("Error")

    def pointCreating(self, x, y):
        p = self.parent.newPoint(x, y)
        self.parent.messageSend("Point succesfully placed" + " " * 10 + str(p))

    def pointInObjectCreating(self, x, y):
        self.parent.newPoint(x, y)
        self.parent.messageSend("Point succesfully placed" + " " * 10 + str(x) + ", " + str(y))

    def segmentCreating(self, point1, point2):
        n_point1, n_point2 = self.parent.model.correcting_points(point1, point2)
        if n_point1 is point1:
            n_point1 = self.parent.newPoint(point1.x, point1.y)
        if n_point2 is point2:
            n_point2 = self.parent.newPoint(point2.x, point2.y)
        segment = self.parent.newSegment(n_point1, n_point2)
        # self.parent.messageSend(f"Segment With Points succesfully placed {' ' * 10}{segment.point1}-{segment.point2}")

    def circleWithRadiusCreating(self, center, point2):
        n_center, n_point2 = self.parent.model.correcting_points(center, point2)
        if self.parent.brushundertype == "radius":
            if n_center is center:
                n_center = self.parent.newPoint(center.x, center.y)
            if n_point2 is point2:
                n_point2 = self.parent.newPoint(point2.x, point2.y)
            circle = self.parent.newCircle(geometry.Segment(n_center, n_point2))
            self.parent.messageSend(
                f"Circle succesfully placed with{' ' * 10}center: {circle.center}; radius: {circle.radius}; point: {circle.point}")

    def pointDrawing(self, qp, x, y, name):
        qp.setBrush(self.pointBrushColor)
        qp.setPen(QPen(self.pointBrushColor, 2))
        qp.drawEllipse(QPoint(x, y), 2, 2)
        qp.setBrush(self.textColor)
        qp.setPen(QPen(self.textColor, 2))
        qp.setFont(self.textFont)
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

    def selectionSegmentDrawing(self, qp, point1, point2):
        qp.setBrush(self.selectionSegmentBrushColor)
        qp.setPen(QPen(self.selectionSegmentBrushColor, 2))
        qp.drawLine(QPoint(point1.x, point1.y), QPoint(point2.x, point2.y))

    def circleDrawing(self, qp, centerX, centerY, distance):
        alphaColor = QColor.fromRgbF(0, 0, 0, 0)
        qp.setBrush(self.segmentBrushColor)
        qp.setPen(QPen(self.segmentBrushColor, 2))
        qp.setBrush(alphaColor)
        qp.drawEllipse(float(centerX) - distance, float(centerY) - distance, float(distance) * 2, float(distance) * 2)
        qp.setBrush(self.pointBrushColor)


app = QApplication(sys.argv)
interface = MainWindow()
sys.exit(app.exec_())
