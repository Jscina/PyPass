from PyQt5 import QtCore, QtGui, QtWidgets
from cypher import Cypher
from MainWindow import *


class Ui_LoginWindow(object):
    def switch(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setup(self.window)
        self.window.show()

    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(LoginWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.uname_label = QtWidgets.QLabel(self.centralwidget)
        self.uname_label.setGeometry(QtCore.QRect(230, 220, 81, 17))
        self.uname_label.setObjectName("uname_label")

        self.pword_label = QtWidgets.QLabel(self.centralwidget)
        self.pword_label.setGeometry(QtCore.QRect(390, 220, 91, 17))
        self.pword_label.setObjectName("pword_label")

        self.login = QtWidgets.QPushButton(self.centralwidget)
        self.login.setGeometry(QtCore.QRect(550, 250, 89, 26))
        self.login.setObjectName("login")
        self.login.clicked.connect(self.login_to_main)

        self.username = QtWidgets.QLineEdit(self.centralwidget)
        self.username.setGeometry(QtCore.QRect(230, 250, 113, 26))
        self.username.setObjectName("username")

        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(390, 250, 113, 26))
        self.password.setObjectName("password")

        LoginWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(LoginWindow)
        self.statusbar.setObjectName("statusbar")
        LoginWindow.setStatusBar(self.statusbar)

        self.retranslateUi(LoginWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)

    def login_to_main(self):
        user_name = self.username.text()
        pass_word = self.password.text()
        cypher = Cypher()
        with open("login.txt", "rb") as file:
            lines = file.readlines()
        file.close()
        if user_name == cypher.decrypt_phrase(lines[0]) and pass_word == cypher.decrypt_phrase(lines[1]):
            self.switch()
            LoginWindow.hide()
        else:
            self.username.setText("")
            self.password.setText("")

    def retranslateUi(self, LoginWindow):
        _translate = QtCore.QCoreApplication.translate
        LoginWindow.setWindowTitle(_translate("LoginWindow", "Login"))
        self.uname_label.setText(_translate("LoginWindow", "Username:"))
        self.pword_label.setText(_translate("LoginWindow", "Password:"))
        self.login.setText(_translate("LoginWindow", "Login"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    LoginWindow = QtWidgets.QMainWindow()
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap("locked.ico"), QtGui.QIcon.Selected, QtGui.QIcon.On)
    LoginWindow.setWindowIcon(icon)
    ui = Ui_LoginWindow()
    ui.setupUi(LoginWindow)
    LoginWindow.show()
    sys.exit(app.exec_())
