from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from serial_cypher import File_Manager
import mainwindow, qdarkstyle

# @Author: Joshua Scina
# @Version: 2.0

class Ui_UpdateWindow(object):
    # Switch back to main window
    def switch_to_main(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = mainwindow.Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        self.UpdateWindow.hide()

    # Builds the window
    def setupUi(self, UpdateWindow):
        UpdateWindow.setObjectName("UpdateWindow")
        UpdateWindow.resize(647, 167)
        UpdateWindow.setWindowIcon(QIcon("locked.ico"))
        self.UpdateWindow = UpdateWindow

        self.centralwidget = QtWidgets.QWidget(UpdateWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Username input
        self.username = QtWidgets.QLineEdit(self.centralwidget)
        self.username.setGeometry(QtCore.QRect(50, 40, 171, 26))
        self.username.setObjectName("username")

        # Password input
        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(270, 40, 191, 26))
        self.password.setObjectName("password")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

        # Update login button
        self.update_button = QtWidgets.QPushButton(self.centralwidget)
        self.update_button.setGeometry(QtCore.QRect(510, 40, 89, 26))
        self.update_button.setObjectName("update_button")
        self.update_button.clicked.connect(self.change_login)

        # Label above the username input
        self.u_label = QtWidgets.QLabel(self.centralwidget)
        self.u_label.setGeometry(QtCore.QRect(50, 20, 141, 17))
        self.u_label.setObjectName("u_label")

        # Label above the password input
        self.p_label = QtWidgets.QLabel(self.centralwidget)
        self.p_label.setGeometry(QtCore.QRect(270, 20, 131, 17))
        self.p_label.setObjectName("p_label")

        # Label above the current login
        self.current_login_label = QtWidgets.QLabel(self.centralwidget)
        self.current_login_label.setGeometry(QtCore.QRect(50, 90, 131, 25))
        self.current_login_label.setObjectName("current_login_label")

        # Label for the current login
        self.current_account_label = QtWidgets.QLabel(self.centralwidget)
        self.current_account_label.setGeometry(QtCore.QRect(50, 110, 141, 25))
        self.current_account_label.setObjectName("current_account_label")

        # Switches back to main window
        self.done = QtWidgets.QPushButton(self.centralwidget)
        self.done.setGeometry(QtCore.QRect(510, 80, 89, 26))
        self.done.setObjectName("done")
        self.done.clicked.connect(self.switch_to_main)

        UpdateWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(UpdateWindow)
        self.current_login()

        QtCore.QMetaObject.connectSlotsByName(UpdateWindow)

    # Change the current login to new one
    def change_login(self):
        username, password, manage = (
            self.username.text(),
            self.password.text(),
            File_Manager(),
        )

        self.username.setText("")
        self.password.setText("")

        login = [manage.encrypt(username), manage.encrypt(password)]

        with open("login.txt", "wb") as file:
            manage.dump(login, file)
        self.current_login()
        
    # Gets the current login
    def current_login(self):
        manage = File_Manager()

        with open("login.txt", "rb") as file:
            login = manage.load(file)

        for index in range(len(login)):
            login[index] = manage.decrypt(login[index])

        login_string = login[0] + " " + login[1]

        self.current_account_label.setText(login_string)
        self.current_account_label.updateGeometry()

    def retranslateUi(self, UpdateWindow):
        _translate = QtCore.QCoreApplication.translate
        UpdateWindow.setWindowTitle(_translate("UpdateWindow", "Update Login"))
        self.update_button.setText(_translate("UpdateWindow", "Update"))
        self.u_label.setText(_translate("UpdateWindow", "Username:"))
        self.p_label.setText(_translate("UpdateWindow", "Password:"))
        self.current_login_label.setText(_translate("UpdateWindow", "Current Login:"))
        self.current_account_label.setText(_translate("UpdateWindow", "Error"))
        self.done.setText(_translate("UpdateWindow", "Done"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    UpdateWindow = QtWidgets.QMainWindow()
    ui = Ui_UpdateWindow()
    ui.setupUi(UpdateWindow)
    UpdateWindow.show()
    sys.exit(app.exec_())
