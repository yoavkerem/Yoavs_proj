import socket
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import select
import mysql.connector
import random
from PyQt5 import QtCore, QtWidgets


# !usr/bin/env python
# -*-coding:utf-8-*-
# window class
class Client:
    def __init__(self):
        self.guessWord=''
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # responsible for changing text color, text font and back ground color ( personal task). [1;107;97m - white, "\033[1;97;40m" - dark, "\033[1;7;97m" - light
        CLIENT_PORT = 1729
        CLIENT_IP = "127.0.0.1"
        print("Client is starting")
        self.my_socket.connect((CLIENT_IP, CLIENT_PORT))

    def send_request_to_server(self, request):
        """Send the request to the server. First the length of the request (2 digits), then the request itself
        Example: '04EXIT'
        Example: '12DIR c:\cyber'
        """
        length = str(len(request))
        zfill_length = length.zfill(2)
        message = zfill_length + request
        self.my_socket.send(message.encode('utf-8'))

    def handle_client_response(self):
        length = self.my_socket.recv(2).decode()
        data = self.my_socket.recv(int(length)).decode()
        return data


class Act_Painter(QMainWindow):
    def __init__(self, _c, paintedwords):

        super().__init__()
        self._c = _c
        self.paintedwords = paintedwords

        # setting title
        self.setWindowTitle("Paint with PyQt5")

        # setting geometry to main window
        self.setGeometry(100, 100, 800, 600)

        # creating image object
        self.image = QImage(self.size(), QImage.Format_RGB32)

        # making image color to white
        self.image.fill(Qt.white)

        # variables
        # drawing flag
        self.drawing = False
        self.start = False
        # default brush size
        self.brushSize = 2
        # default color
        self.brushColor = Qt.black

        # QPoint object to tract the point
        self.lastPoint = QPoint()
        # creating menu bar
        mainMenu = self.menuBar()

        # adding brush size to main menu
        b_size = mainMenu.addMenu("Brush Size")

        # adding brush color to ain menu
        b_color = mainMenu.addMenu("Brush Color")

        # creating file menu for save and clear action
        fileMenu = mainMenu.addMenu("clear")
        # creating clear action

        clearAction = QAction("Clear", self)
        # adding clear to the file menu
        fileMenu.addAction(clearAction)
        # adding action to the clear
        clearAction.triggered.connect(self.clear)
        # similarly repeating above steps for different color
        eraser = QAction("eraser", self)
        fileMenu.addAction(eraser)
        eraser.triggered.connect(self.whiteColor)

        # creating options for brush sizes
        # creating action for selecting pixel of 4px
        pix_4 = QAction("4px", self)
        # adding this action to the brush size
        b_size.addAction(pix_4)
        # adding method to this
        pix_4.triggered.connect(self.Pixel_4)

        # similarly repeating above steps for different sizes
        pix_7 = QAction("7px", self)
        b_size.addAction(pix_7)
        pix_7.triggered.connect(self.Pixel_7)

        pix_9 = QAction("9px", self)
        b_size.addAction(pix_9)
        pix_9.triggered.connect(self.Pixel_9)

        pix_12 = QAction("12px", self)
        b_size.addAction(pix_12)
        pix_12.triggered.connect(self.Pixel_12)

        # creating options for brush color
        # creating action for black color
        black = QAction("Black", self)
        # adding this action to the brush colors
        b_color.addAction(black)
        # adding methods to the black
        black.triggered.connect(self.blackColor)

        green = QAction("Green", self)
        b_color.addAction(green)
        green.triggered.connect(self.greenColor)

        yellow = QAction("Yellow", self)
        b_color.addAction(yellow)
        yellow.triggered.connect(self.yellowColor)

        red = QAction("Red", self)
        b_color.addAction(red)
        red.triggered.connect(self.redColor)
        self.menuBar().setDisabled(True)
        word1, word2 = self.chosen_words()
        self.opOne = QPushButton('yoav', self)
        self.opTwo = QPushButton('noga', self)
        self.UiComponents()

    def chosen_words(self):
        rand1 = random.randint(1, 30)
        rand2 = random.randint(1, 30)
        for i in self.paintedwords:
            if (i[1] == rand1):
                word1 = i[0]
            if (i[1] == rand2):
                word2 = i[0]
        return word1, word2

    def UiComponents(self):
        # creating a push button
        # setting geometry of button
        self.opOne.setGeometry(200, 150, 200, 60)
        self.opTwo.setGeometry(500, 150, 200, 60)

        # adding action to a button

        self.opOne.clicked.connect(self.click1)
        self.opTwo.clicked.connect(self.click2)

        # action method

    def click1(self):
        self.c.guessWord = self.opOne.text()
        self.startPaint()

    def click2(self):
        self.c.guessWord  = self.opTwo.text()
        self.startPaint()

    def startPaint(self):
        self.start = True
        self.menuBar().setDisabled(False)
        self.opOne.hide()
        self.opTwo.hide()

    # method for checking mouse cicks
    def mousePressEvent(self, event):
        # if left mouse button is pressed
        if event.button() == Qt.LeftButton and self.start:
            # make drawing flag truipconfigipe
            self.drawing = True
            # make last point to the point of cursor
            self.lastPoint = event.pos()

    # method for tracking mouse activity
    def mouseMoveEvent(self, event):

        # checking if left button is pressed and drawing flag is true
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            # creating painter object
            painter = QPainter(self.image)

            # set the pen of the painter
            painter.setPen(QPen(self.brushColor, self.brushSize,
                                Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

            # draw line from the last point of cursor to the current point
            # this will draw only one step

            painter.drawLine(self.lastPoint, event.pos())

            lst = [str(self.lastPoint.x()), str(self.lastPoint.y()), str(event.pos().x()), str(event.pos().y()),
                   str(self.brushColor), str(self.brushSize)]
            self.splitList(lst)

            # change the last point
            self.lastPoint = event.pos()
            # update

            self.update()

    def splitList(self, lst):
        str = ''
        for i in lst:
            str += i + ' '
        self._c.send_request_to_server(str)

        # method for mouse left button release

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.LeftButton:
            # make drawing flag false

            self.drawing = False

    # paint event
    def paintEvent(self, event):
        # create a canvas
        canvasPainter = QPainter(self)

        # draw rectangle  on the canvas
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    # method for clearing every thing on canvas
    def clear(self):
        # make the whole canvas white
        self.image.fill(Qt.white)
        # update
        self.update()

    # methods for changing pixel sizes
    def Pixel_4(self):
        self.brushSize = 4

    def Pixel_7(self):
        self.brushSize = 7

    def Pixel_9(self):
        self.brushSize = 9

    def Pixel_12(self):
        self.brushSize = 12

    # methods for changing brush color
    def blackColor(self):
        self.brushColor = Qt.black

    def whiteColor(self):
        self.brushColor = Qt.white

    def greenColor(self):
        self.brushColor = Qt.green

    def yellowColor(self):
        self.brushColor = Qt.yellow

    def redColor(self):
        self.brushColor = Qt.red


class Passive_Painter(QMainWindow):
    def __init__(self, c):
        self.c = c
        super().__init__()
        self.setWindowTitle("Paint with PyQt5")
        self.coLst = [Qt.black, Qt.green, Qt.yellow, Qt.red, Qt.white]
        # setting geometry to main window
        self.setGeometry(100, 100, 800, 600)
        # creating image object
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.textbox = QLineEdit(self)
        self.textbox.move(0, 0)
        self.textbox.resize(100, 28)

        # Create a button in the window
        self.button = QPushButton('Enter', self)
        self.button.move(100, 0)
        self.button.clicked.connect(self.on_click)
        self.image.fill(Qt.white)

    def on_click(self):

        self.c.send_request_to_server(self.textbox.text())
        self.textbox.clear()
        print(self.c.handle_client_response)

    def paintEvent(self, event):
        if (lstDat != []):
            # create a canvas
            canvasPainter = QPainter(self)
            # draw rectangle  on the canvas
            canvasPainter.drawImage(self.rect(), self.image, self.image.rect())
            painter = QPainter(self.image)

            for i in self.coLst:
                if (lstDat[4] == str(i)):
                    col = i

            painter.setPen(QPen(col, int(lstDat[5])))
            painter.drawLine(int(lstDat[0]), int(lstDat[1]), int(lstDat[2]), int(lstDat[3]))
        else:
            canvasPainter = QPainter(self)
            # draw rectangle  on the canvas
            canvasPainter.drawImage(self.rect(), self.image, self.image.rect())
        self.update()


class Timer(QMainWindow):
    def __init__(self,p):
        super().__init__()
        self.p=p
        self.setWindowTitle('Timer')
        self.setGeometry(100, 100, 400, 600)
        self.count = 900
        # start flag
        self.start = False

        # creating label to show the seconds
        self.label = QLabel("//TIMER//", self)

        # setting geometry of label
        self.label.setGeometry(100, 200, 200, 50)

        # setting border to the label
        self.label.setStyleSheet("border : 3px solid black")

        # setting font to the label
        self.label.setFont(QFont('Times', 15))

        # setting alignment ot the label
        self.label.setAlignment(Qt.AlignCenter)
        self.start_action()

        # creating a timer object
        timer = QTimer(self)

        # adding action to timer
        timer.timeout.connect(self.showTime)

        # update the timer every tenth second
        timer.start(100)
        self.show()

    def showTime(self):
        # checking if flag is true
        if self.start:
            # incrementing the counter
            self.count -= 1

            # timer is completed
            if self.count == 0:
                # making flag false
                self.start = False
                QMessageBox.about(self, "Over", "Time is over")

                # setting text to the label
                self.p.close()

            if self.start:
                # getting text from count
                text = str(self.count / 10) + " s"

                # showing text
                self.label.setText(text)

    def start_action(self):
        # making flag true
        self.start = True
        # count = 0
        if self.count == 0:
            self.start = False


class Network:

    def __init__(self, client):
        self.client = client

    def iterationBody(self):
        global lstDat
        lstDat = []
        infds, outfds, errfds = select.select([self.client.my_socket], [], [], 0.1)
        if len(infds) != 0:
            data = self.client.handle_client_response()
            if len(data) != 0:
                lstDat = data.split(' ')

    def loop(self):
        self.iterationBody()
        QtCore.QTimer.singleShot(1, self.loop)


def main():
    # create pyqt5 app
    App = QApplication(sys.argv)
    c = Client()

    if (c.handle_client_response() == 'Not painter'):

        network_handler = Network(c)

        pas = Passive_Painter(c)
        timer = Timer(pas)
        pas.show()
        network_handler.loop()
        sys.exit(App.exec())

    else:
        mydb = mysql.connector.connect(
            host="localhost",
            user="Yoav Kerem",
            password="yoavkay25",
            database="wordsdb"
        )
        mycursor = mydb.cursor()
        paintedWords = []
        mycursor.execute("SELECT * FROM PaintedWords")
        for x in mycursor:
            paintedWords.append(x)

        act = Act_Painter(c, paintedWords)
        # create the instance of our Window
        # showing the window
        act.show()
        # start the app
        sys.exit(App.exec())


if __name__ == "__main__":
    main()
