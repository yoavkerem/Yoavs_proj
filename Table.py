import sys
import select
from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
class Table(QDialog):
    def __init__(self):
        super(Table,self).__init__()
        loadUi("stats and results.ui",self)
        self.tableWidget.setColumnWidth(0,117)
        self.tableWidget.setColumnWidth(1, 117)
        self.tableWidget2.setColumnWidth(0, 70)
        self.tableWidget2.setColumnWidth(1, 70)
        self.tableWidget2.setColumnWidth(2, 152)

        self.loaddata()

    def loaddata(self):
        people=[{"name":"Yoav","points":1},{"name": "Nadav","points":0}]
        stats=[{"games":14,"wins":9,"pointsPerGame":3.8}]
        self.tableWidget.setRowCount(len(people))
        self.tableWidget2.setRowCount(1)
        row=0
        for person in people:
            self.tableWidget.setItem(row,0,QtWidgets.QTableWidgetItem(person["name"]))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(person["points"])))
            row+=1
        self.tableWidget2.setItem(0, 0, QtWidgets.QTableWidgetItem(str(stats[0]["games"])))
        self.tableWidget2.setItem(0, 1, QtWidgets.QTableWidgetItem(str(stats[0]["wins"])))
        self.tableWidget2.setItem(0, 2, QtWidgets.QTableWidgetItem(str(stats[0]["pointsPerGame"])))

app=QApplication(sys.argv)
t=Table()
widget=QtWidgets.QStackedWidget()
widget.addWidget(t)
widget.setFixedWidth(800)
widget.setFixedHeight(581)
widget.show()
app.exec_()
