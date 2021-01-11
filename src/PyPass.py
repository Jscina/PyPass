import os

from PyQt5 import QtCore, QtGui, QtWidgets

import PyPass_Main_Window
from serial_cypher import File_Manager


class Ui_LoginWindow(object):
    def __init__(self):
        self._crypter = File_Manager()
        if os.path.exists(os.path.abspath("data.pp")):
            pass
        else:
            self._crypter.gen_data()

    def _Main_Window(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = PyPass_Main_Window.Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        self.LoginWindow.close()

    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(591, 194)
        LoginWindow.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                  "font: 11pt \"Segoe UI\";")
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        LoginWindow.setWindowIcon(QtGui.QIcon(
            scriptDir + os.path.sep + 'locked.ico'))
        self.LoginWindow = LoginWindow
        self.centralwidget = QtWidgets.QWidget(LoginWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.login = QtWidgets.QPushButton(self.centralwidget)
        self.login.setStyleSheet("color: rgb(255, 255, 255);\n"
                                 "background-color: rgb(79, 79, 79);")
        self.login.setObjectName("login")
        self.login.clicked.connect(self._login)

        self.gridLayout.addWidget(self.login, 3, 3, 1, 1)

        self.username = QtWidgets.QLineEdit(self.centralwidget)
        self.username.setStyleSheet("color: rgb(255, 255, 255);\n"
                                    "gridline-color: rgb(0, 0, 0);\n"
                                    "background-color: rgb(80, 80, 80);\n"
                                    "border-radius: 5px;")
        self.username.setText("")
        self.username.setObjectName("username")

        self.gridLayout.addWidget(self.username, 3, 1, 1, 1)

        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)

        self.pword_label = QtWidgets.QLabel(self.centralwidget)
        self.pword_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.pword_label.setAlignment(
            QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft)
        self.pword_label.setObjectName("pword_label")

        self.gridLayout.addWidget(self.pword_label, 2, 2, 1, 1)

        self.uname_label = QtWidgets.QLabel(self.centralwidget)
        self.uname_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.uname_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.uname_label.setAlignment(
            QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft)
        self.uname_label.setObjectName("uname_label")

        self.gridLayout.addWidget(self.uname_label, 2, 1, 1, 1)

        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setStyleSheet("color: rgb(255, 255, 255);\n"
                                    "gridline-color: rgb(0, 0, 0);\n"
                                    "background-color: rgb(80, 80, 80);\n"
                                    "border-radius: 5px;")
        self.password.setText("")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")

        self.gridLayout.addWidget(self.password, 3, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 4, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 4, 1, 1, 3)
        spacerItem3 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 0, 1, 1, 3)
        LoginWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(LoginWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)

    def retranslateUi(self, LoginWindow):
        _translate = QtCore.QCoreApplication.translate
        LoginWindow.setWindowTitle(_translate("LoginWindow", "Login"))
        self.login.setText(_translate("LoginWindow", "Login"))
        self.pword_label.setText(_translate("LoginWindow", "Password:"))
        self.uname_label.setText(_translate("LoginWindow", "Username:"))

    # Login Method
    def _login(self):
        username_str = self.username.text()
        password_str = self.password.text()
        data = self._crypter.load_data()
        username_list = data[0]
        password_list = data[1]
        keys = data[2]

        if username_str == self._crypter.decrypt(username_list[0], keys[0]) and password_str == self._crypter.decrypt(
                password_list[0], keys[0]):
            logged_in = True
            self._Main_Window()

        self.username.setText("")
        self.password.setText("")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('fusion')
    LoginWindow = QtWidgets.QMainWindow()
    ui = Ui_LoginWindow()
    ui.setupUi(LoginWindow)
    LoginWindow.show()
    sys.exit(app.exec_())
