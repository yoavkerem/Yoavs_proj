import time
from cryptography.fernet import Fernet

import mysql.connector
from PyQt5.QtWidgets import *
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from PyQt5.uic import loadUi

class LoginApp(QDialog):
    def __init__(self):
        super(LoginApp, self).__init__()
        loadUi("pyQt5Login.ui",self)
        self.b1.clicked.connect(self.login)
        self.b2.clicked.connect(self.show_reg)

    def login(self):
        un=self.tb1.text()
        pw=self.tb2.text()
        result = False
        print(fernet)
        mycursor.execute("SELECT * FROM PlayerInfor")
        for x in mycursor:
            print(x)
            if(pw==fernet.decrypt(x[1].encode()).decode()):
                result = True
                print(909)
        self.tb1.setText("")
        self.tb2.setText("")
        if result:
            QMessageBox.information(self,"Login Output", "Congrats! You login successfully!")
            mycursor.execute("SELECT * FROM PlayerInfor")
            for x in mycursor:
                print(x)
            widget.close()
        else:
            QMessageBox.information(self, "Login Output", "Invalid User.. Register for new user!")

    def show_reg(self):

        widget.setCurrentIndex(1)



class RegApp(QMainWindow):
    def __init__(self):
        super(RegApp, self).__init__()
        loadUi("pyQt5Signin.ui",self)
        self.b3.clicked.connect(self.reg)
        self.b4.clicked.connect(self.show_login)

    def reg(self):
        print(33)
        un = self.tb3.text()
        pw = self.tb4.text()
        em = self.tb5.text()
        result = False
        mycursor.execute("SELECT * FROM PlayerInfor")
        for x in mycursor:
            if fernet.decrypt(x[1].encode()).decode()==pw and x[0]==un:
                result=True
        if result==True:
            QMessageBox.information(self, "Login form", "The user already registered")

        else:
            print(0)
            crypt_pw=fernet.encrypt(pw.encode())

            mycursor.execute("insert into PlayerInfor values ('" + un + "','" + str(crypt_pw.decode()) + "','" + em + "',0,0,0)")

            QMessageBox.information(self, "Login form", "The user registered successfully, You can login now!")
            mydb.commit()

    def show_login(self):
        widget.setCurrentIndex(0)


mydb = mysql.connector.connect(host="localhost", user="Yoav Kerem", password="yoavkay25", database="wordsdb")
mycursor = mydb.cursor()

#def main():
key = b'2gsTN-tzEllR1IdyV4KxCpdhi_qh2kCW5DDrUMSTZtk='
# Instance the Fernet class with the key
fernet = Fernet(key)
message = "yoav"

#mycursor.execute("CREATE TABLE PlayStats(username VARCHAR(100), password VARCHAR(1024), email VARCHAR(100), points int UNSIGNED , wins int UNSIGNED, games int UNSIGNED)")
App = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()

widget.setGeometry(100, 100, 800, 800)
loginform = LoginApp()
registrationform = RegApp()
widget.addWidget(loginform)
widget.addWidget(registrationform)
widget.setCurrentIndex(0)
widget.show()
App.exec()
time.sleep(10)


#if __name__ == "__main__":
#    main()








