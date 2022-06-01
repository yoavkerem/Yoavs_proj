import socket
import time

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import select
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi


# !usr/bin/env python
# -*-coding:utf-8-*-
# window class
class Client:
    def __init__(self,ip,port):
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # responsible for changing text color, text font and back ground color ( personal task). [1;107;97m - white, "\033[1;97;40m" - dark, "\033[1;7;97m" - light

        CLIENT_PORT = port
        CLIENT_IP = ip
        print(CLIENT_PORT)
        print(CLIENT_IP)
        print("Client is starting")
        self.my_socket.connect((CLIENT_IP, CLIENT_PORT))

    def send_request_to_server(self, request):
        """Send the request to the server. First the length of the request (2 digits), then the request itself
        Example: '04EXIT'
        Example: '12DIR c:\cyber'
        """
        length = str(len(request.encode('utf-8')))
        zfill_length = length.zfill(2)
        message = zfill_length + request
        self.my_socket.send(message.encode('utf-8'))

    def handle_client_response(self):
        length = self.my_socket.recv(2).decode()
        data = self.my_socket.recv(int(length)).decode()
        return data


class Act_Painter(QMainWindow):
    def __init__(self, _c,words ):

        super().__init__()
        print('painter')
        self._c = _c

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
        self.brushSize = 5
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
        words = words

        self.opOne = QPushButton(words[0], self)
        self.opTwo = QPushButton(words[1], self)
        self.UiComponents()

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
        self.guessWord = self.opOne.text()
        self.startPaint()

    def click2(self):
        self.guessWord = self.opTwo.text()
        self.startPaint()

    def startPaint(self):
        self._c.send_request_to_server('w' + self.guessWord)
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
        self.brushSize = 5

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
        print('not painer')
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
        """data=self.c.handle_client_response()
        data=data.split(' ')
        if data[0]=='true':
            print('true')
            self.points+=int(data[1])
            self.setDisabled(True)"""

    def paintEvent(self, event):
        if lstDat != [] and lstDat!=["done"] and lstDat[0]!="true":
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
    def __init__(self,painter,count):
        super().__init__()
        self.painter=painter
        self.setWindowTitle('Timer')
        self.setGeometry(900, 100, 0, 80)
        self.count = count
        # start flag
        self.start = False

        # creating label to show the seconds
        self.label = QLabel("//TIMER//", self)

        # setting geometry of label
        self.label.setGeometry(0,0 , 160, 80)

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


    def showTime(self):
        # checking if flag is true
        if self.start:
            # incrementing the counter
            self.count -= 1

            # timer is completed

            if self.count == 0 :
                # making flag false
                self.start = False
                #QMessageBox.about(self, "Over", "Time is over")

                # setting text to the label
                self.painter.close()
                self.close()



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

    def __init__(self, client,pas,timer,points):
        self.points=points
        self.client = client
        self.pas=pas
        self.timer=timer

    def iterationBody(self):
        global lstDat
        lstDat = []
        infds, outfds, errfds = select.select([self.client.my_socket], [], [], 0.1)
        if len(infds) != 0:
            data = self.client.handle_client_response()
            lstDat = data.split(' ')
            if len(data) != 0:
                if lstDat[0]=="done":
                    self.timer.close()
                    self.pas.close()
                elif lstDat[0]=="true":
                    self.pas.setDisabled(True)

                    self.points=int(lstDat[1])







    def loop(self):
        if startLoop==True:
            self.iterationBody()
            QtCore.QTimer.singleShot(1, self.loop)

class LoginApp(QDialog):
    def __init__(self,client):
        super(LoginApp, self).__init__()
        self.client=client
        loadUi("pyQt5Login.ui",self)
        self.b1.clicked.connect(self.login)
        self.b2.clicked.connect(self.show_reg)

    def login(self):
        un=self.tb1.text()
        pw=self.tb2.text()
        self.client.send_request_to_server("L"+un+ " "+pw)
        result=self.client.handle_client_response()
        print(result)
        self.tb1.setText("")
        self.tb2.setText("")
        if result=='suitability':
            QMessageBox.information(self,"Login Output", "Congrats! You login successfully!")
            self.client.send_request_to_server("logged in")
            widget.close()
        else:
            QMessageBox.information(self, "Login Output", "Invalid User.. Register for new user!")

    def show_reg(self):
        widget.setCurrentIndex(1)


class RegApp(QDialog):
    def __init__(self,client):
        super(RegApp, self).__init__()
        self.client = client
        loadUi("pyQt5Signin.ui",self)
        self.b3.clicked.connect(self.reg)
        self.b3.clicked.connect(self.show_login)

    def reg(self):
        un = self.tb3.text()
        pw = self.tb4.text()
        em = self.tb5.text()

        self.client.send_request_to_server('L'+un + ' ' + pw)
        result = self.client.handle_client_response()
        print(result)
        if result=='suitability':
            QMessageBox.information(self, "Login form", "There was problem with the registration")
            self.tb3.setText("")
            self.tb4.setText("")
            self.tb5.setText("")
        else:

            self.client.send_request_to_server('N'+un+' '+pw+' '+em)
            if(self.client.handle_client_response()=='unvalid'):
                QMessageBox.information(self, "Login form", "There was problem with the registration")
                self.tb3.setText("")
                self.tb4.setText("")
                self.tb5.setText("")
            else:
                QMessageBox.information(self, "Login form", "The user registered successfully, You can login now!")

    def show_login(self):
        widget.setCurrentIndex(0)

class actNetwork():
    def __init__(self,client,timer):
        self.client = client
        self.timer = timer

    def iterationBody(self):
        global lstDat
        lstDat = []
        infds, outfds, errfds = select.select([self.client.my_socket], [], [], 0.00000000000001)
        if len(infds) != 0:
            data = self.client.handle_client_response()
            print(data)
            if len(data) != 0:
                if data == "done":
                    self.timer.close()
                    self.timer.painter.close()

    def loop(self):
        if startActLoop == True:
            self.iterationBody()
            QtCore.QTimer.singleShot(2, self.loop)


class Table(QDialog):
    def __init__(self,c,num_of_players):
        super(Table,self).__init__()
        loadUi("stats and results.ui",self)
        self.c=c
        self.num_of_players =num_of_players
        self.tableWidget.setColumnWidth(0,117)
        self.tableWidget.setColumnWidth(1, 117)
        self.tableWidget2.setColumnWidth(0, 70)
        self.tableWidget2.setColumnWidth(1, 70)
        self.tableWidget2.setColumnWidth(2, 152)

        self.loaddata()

    def loaddata(self):
        dataLst=[]
        for i in range(self.num_of_players):
            data=self.c.handle_client_response().split(' ')
            name=data[0]
            points=data[1]
            dataLst.append((name,points))
        data=self.c.handle_client_response().split(' ')
        tempLst=dataLst
        newLst=[]

        i=0
        while i<self.num_of_players:
            print(i)
            max=self.maxPlayer(tempLst)
            tempLst.remove(max)
            newLst.append(max)
            i+=1

        self.tableWidget.setRowCount(self.num_of_players)
        self.tableWidget2.setRowCount(1)
        row=0
        for person in newLst:
            self.tableWidget.setItem(row,0,QtWidgets.QTableWidgetItem(person[0]))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(person[1])))
            row+=1
        avg=float(int(data[0])/int(data[2]))
        self.tableWidget2.setItem(0, 0, QtWidgets.QTableWidgetItem(data[2]))
        self.tableWidget2.setItem(0, 1, QtWidgets.QTableWidgetItem(data[1]))
        self.tableWidget2.setItem(0, 2, QtWidgets.QTableWidgetItem(str(avg)))

    def maxPlayer(self,tempLst):
        max=tempLst[0]
        print(tempLst)
        for i in tempLst:
            if int(i[1])>int(max[1]):
                max=i
        print('max' +max[1])
        return max




def main():
    with open('datas.txt', 'r') as f:
        data_list = []
        for line in f:
            data_list.append(line.split(' ')[1][:-1])

    c = Client(str(data_list[0]),int(data_list[1]))
    # create pyqt5 app
    App = QApplication(sys.argv)
    global widget
    widget = QtWidgets.QStackedWidget()
    widget.setGeometry(450, 100, 400, 500)
    loginform = LoginApp(c)
    registrationform = RegApp(c)
    widget.addWidget(loginform)
    widget.addWidget(registrationform)
    widget.setCurrentIndex(0)
    widget.show()
    App.exec()
    data=c.handle_client_response().split(' ')
    if data[0]=="start":
        num_of_players=data[1]
        points=0
        for i in range(int(num_of_players)):
            if (c.handle_client_response() == 'Not painter'):
                global startLoop
                startLoop = True
                pas = Passive_Painter(c)
                timer = Timer(pas,100)
                network_handler = Network(c,timer,pas,points)
                timer.show()
                pas.show()
                network_handler.loop()
                App.exec()
                points+=network_handler.points
            else:
                global startActLoop
                startActLoop = True
                words = c.handle_client_response()
                if(words[0][-1]==' '):
                    words = c.handle_client_response()
                words=words.split('&')
                print(words)
                act = Act_Painter(c,words)
                timer = Timer(act,100)
                actNet=actNetwork(c,timer)
                timer.show()
                # create the instance of our Window
                # showing the window
                act.show()
                # start the app
                actNet.loop()
                App.exec()
            startLoop=False
            startActLoop = False
            if i!=int(num_of_players)-1:
                c.send_request_to_server("Time over")
        c.send_request_to_server("end "+str(points))
        t = Table(c,int(num_of_players))
        widget2 = QtWidgets.QStackedWidget()
        widget2.addWidget(t)
        widget2.setFixedWidth(800)
        widget2.setFixedHeight(581)
        widget2.show()
        App.exec_()


if __name__ == "__main__":
    main()
