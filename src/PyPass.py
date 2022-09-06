#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### **Title: Pypass** ######
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### **Author: Joshua Scina** ######
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### **Version 5.0** ######
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### **Imports needed to run program: ** ######
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os, PyPass_Main_Window

from PyQt6 import QtCore, QtGui, QtWidgets
from PyPass_Engine import File_Manager
from PyPass_Engine import LoginMethods

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##### **Main Login UI** ######
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Ui_LoginWindow(object):
    # Checks to make sure the storage file exist if not create it
    def __init__(self):
        if os.path.exists(os.path.abspath("data.pp")):
            pass
        else:
            self._crypter.gen_data()

    def _Main_Window(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = PyPass_Main_Window.Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        LoginWindow.close()

    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(591, 194)
        LoginWindow.setStyleSheet(
            "background-color: rgb(0, 0, 0);\n"
            '                font: 11pt "Segoe UI";\n'
            "            "
        )
        LoginWindow.setWindowIcon(QtGui.QIcon(os.path.abspath("locked.ico")))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.centralwidget = QtWidgets.QWidget(LoginWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.login = QtWidgets.QPushButton(self.centralwidget)
        self.login.setStyleSheet(
            "color: rgb(255, 255, 255);\n"
            "                                background-color: rgb(79, 79, 79);\n"
            "                            "
        )
        self.login.setObjectName("login")
        self.login.clicked.connect(self._login)
        self.gridLayout.addWidget(self.login, 3, 3, 1, 1)
        self.username = QtWidgets.QLineEdit(self.centralwidget)
        self.username.setStyleSheet(
            "color: rgb(255, 255, 255);\n"
            "                                gridline-color: rgb(0, 0, 0);\n"
            "                                background-color: rgb(80, 80, 80);\n"
            "                                border-radius: 5px;\n"
            "                            "
        )
        self.username.setText("")
        self.username.setObjectName("username")
        self.gridLayout.addWidget(self.username, 3, 1, 1, 1)
        self.pword_label = QtWidgets.QLabel(self.centralwidget)
        self.pword_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.pword_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignBottom
            | QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
        )
        self.pword_label.setObjectName("pword_label")
        self.gridLayout.addWidget(self.pword_label, 2, 2, 1, 1)
        self.uname_label = QtWidgets.QLabel(self.centralwidget)
        self.uname_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.uname_label.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.uname_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignBottom
            | QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
        )
        self.uname_label.setObjectName("uname_label")
        self.gridLayout.addWidget(self.uname_label, 2, 1, 1, 1)
        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setStyleSheet(
            "color: rgb(255, 255, 255);\n"
            "                                gridline-color: rgb(0, 0, 0);\n"
            "                                background-color: rgb(80, 80, 80);\n"
            "                                border-radius: 5px;\n"
            "                            "
        )
        self.password.setText("")
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password.setObjectName("password")
        self.gridLayout.addWidget(self.password, 3, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.gridLayout.addItem(spacerItem, 4, 1, 1, 3)
        spacerItem1 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.gridLayout.addItem(spacerItem1, 0, 1, 1, 3)
        spacerItem2 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.gridLayout.addItem(spacerItem2, 2, 0, 2, 1)
        spacerItem3 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.gridLayout.addItem(spacerItem3, 2, 4, 2, 1)
        LoginWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(LoginWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)

    def retranslateUi(self, LoginWindow):
        _translate = QtCore.QCoreApplication.translate
        LoginWindow.setWindowTitle(_translate("LoginWindow", "Login"))
        self.login.setText(_translate("LoginWindow", "Login"))
        self.pword_label.setText(_translate("LoginWindow", "Password:"))
        self.uname_label.setText(_translate("LoginWindow", "Username:"))

    def _login(self):
        login = LoginMethods()
        if login.login(self.username.text(), self.password.text()):
            self._Main_Window()
            self.username.setText("")
            self.password.setText("")



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    LoginWindow = QtWidgets.QMainWindow()
    ui = Ui_LoginWindow()
    ui.setupUi(LoginWindow)
    LoginWindow.show()
    sys.exit(app.exec())
