from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from serial_cypher import File_Manager
import mainwindow, qdarkstyle

# @Author: Joshua Scina
# @Version: 2.0


class Ui_LoginWindow(object):
    # Switch to the Main Window
    def switch_to_main(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = mainwindow.Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        self.LoginWindow.hide()

    # Builds the window
    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(591, 230)
        LoginWindow.setWindowIcon(QIcon("locked.ico"))
        self.LoginWindow = LoginWindow

        self.centralwidget = QtWidgets.QWidget(LoginWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Label above the username input
        self.uname_label = QtWidgets.QLabel(self.centralwidget)
        self.uname_label.setGeometry(QtCore.QRect(100, 80, 81, 17))
        self.uname_label.setObjectName("uname_label")

        # Label above the password input
        self.pword_label = QtWidgets.QLabel(self.centralwidget)
        self.pword_label.setGeometry(QtCore.QRect(260, 80, 91, 17))
        self.pword_label.setObjectName("pword_label")

        # Login button
        self.login = QtWidgets.QPushButton(self.centralwidget)
        self.login.setGeometry(QtCore.QRect(420, 110, 89, 26))
        self.login.setObjectName("login")
        self.login.clicked.connect(self.__login__)

        # Username input
        self.username = QtWidgets.QLineEdit(self.centralwidget)
        self.username.setGeometry(QtCore.QRect(100, 110, 113, 26))
        self.username.setObjectName("username")

        # Password input
        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(260, 110, 113, 26))
        self.password.setObjectName("password")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

        LoginWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(LoginWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)

    # Login method
    def __login__(self):
        login = [self.username.text(), self.password.text()]
        manage = File_Manager()
        try:
            # Load the login file
            with open("login.txt", "rb") as file:
                log_user = manage.load(file)
            # If the input matches what's in the login switch to the main window
            if manage.decrypt(log_user[0]) == login[0] and manage.decrypt(log_user[1]) == login[1]:
                self.switch_to_main()
        except FileNotFoundError:
            # If the files don't exist create them then re-invoke the login method
            self.fix()
            self.__login__()

    def fix(self):
        # Create the login file if it doesn't exist
        manage = File_Manager()
        login_default = [manage.encrypt("username"), manage.encrypt("password")]

        with open("login.txt", "wb") as file:
            manage.dump(login_default, file)

    def retranslateUi(self, LoginWindow):
        _translate = QtCore.QCoreApplication.translate
        LoginWindow.setWindowTitle(_translate("LoginWindow", "Login"))
        self.uname_label.setText(_translate("LoginWindow", "Username:"))
        self.pword_label.setText(_translate("LoginWindow", "Password:"))
        self.login.setText(_translate("LoginWindow", "Login"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    LoginWindow = QtWidgets.QMainWindow()
    ui = Ui_LoginWindow()
    ui.setupUi(LoginWindow)
    LoginWindow.show()
    sys.exit(app.exec_())
