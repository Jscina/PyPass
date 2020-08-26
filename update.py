from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from cypher import Cypher
import MainWindow, sys, qdarkstyle

# @Author Joshua Scina
# @Version 1.7


class Ui_UpdateWindow(object):
    def switch(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = MainWindow.Ui_MainWindow()
        self.ui.setup(self.window)
        self.window.show()
        self.UpdateWindow.hide()

    def setup2(self, UpdateWindow):
        UpdateWindow.setObjectName("UpdateWindow")
        UpdateWindow.resize(800, 600)
        UpdateWindow.setWindowIcon(QIcon("locked.ico"))
        self.UpdateWindow = UpdateWindow

        self.centralwidget = QtWidgets.QWidget(UpdateWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.username = QtWidgets.QLineEdit(self.centralwidget)
        self.username.setGeometry(QtCore.QRect(180, 220, 171, 26))
        self.username.setObjectName("username")

        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(400, 220, 191, 26))
        self.password.setObjectName("password")

        self.update_button = QtWidgets.QPushButton(self.centralwidget)
        self.update_button.setGeometry(QtCore.QRect(640, 220, 89, 26))
        self.update_button.setObjectName("update_button")
        self.update_button.clicked.connect(self.update_login)

        self.switch_button = QtWidgets.QPushButton(self.centralwidget)
        self.switch_button.setGeometry(QtCore.QRect(640, 280, 89, 26))
        self.switch_button.setObjectName("switch_button")
        self.switch_button.clicked.connect(self.switch)
        self.switch_button.setText("Done")

        self.u_label = QtWidgets.QLabel(self.centralwidget)
        self.u_label.setGeometry(QtCore.QRect(180, 200, 141, 17))
        self.u_label.setObjectName("u_label")

        self.p_label = QtWidgets.QLabel(self.centralwidget)
        self.p_label.setGeometry(QtCore.QRect(400, 200, 131, 17))
        self.p_label.setObjectName("p_label")

        self.current_login_label = QtWidgets.QLabel(self.centralwidget)
        self.current_login_label.setGeometry(QtCore.QRect(180, 270, 131, 17))
        self.current_login_label.setObjectName("current_login_label")

        self.current_account_label = QtWidgets.QLabel(self.centralwidget)
        self.current_account_label.setGeometry(QtCore.QRect(180, 290, 61, 17))
        self.current_account_label.setObjectName("current_account_label")

        UpdateWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(UpdateWindow)
        self.statusbar.setObjectName("statusbar")
        UpdateWindow.setStatusBar(self.statusbar)

        self.retranslateUi(UpdateWindow)
        self.get_current_login()
        QtCore.QMetaObject.connectSlotsByName(UpdateWindow)

    # Gets the current login credentials and prints them
    def get_current_login(self):
        cypher = Cypher()
        try:
            with open("login.txt", "rb") as file:
                account = file.readlines()

            username, password = cypher.decrypt_phrase(account[0]), cypher.decrypt_phrase(account[1])

            self.current_account_label.setText(
                "Username: " + username + " Password: " + password
            )
            self.current_account_label.adjustSize()
        except FileNotFoundError:
            self.current_account_label.setText("Error login.txt doesn't exist")
            self.current_account_label.adjustSize()

    # Changes the login credentials based on the user input
    def update_login(self):
        username_new, password_new = self.username.text(), self.password.text()
        self.username.setText("")
        self.password.setText("")
        cypher = Cypher()
        try:
            with open("login.txt", "wb") as file:
                file.write(
                    cypher.encrypt_phrase(username_new)
                    + b"\n"
                    + cypher.encrypt_phrase(password_new)
                )
            self.get_current_login()
        except FileNotFoundError:
            self.current_account_label.setText("Error: login.txt does not exist")
            self.current_account_label.adjustSize()

    def retranslateUi(self, UpdateWindow):
        _translate = QtCore.QCoreApplication.translate
        UpdateWindow.setWindowTitle(_translate("UpdateWindow", "Update Login"))
        self.update_button.setText(_translate("UpdateWindow", "Update"))
        self.u_label.setText(_translate("UpdateWindow", "Username:"))
        self.p_label.setText(_translate("UpdateWindow", "Password:"))
        self.current_login_label.setText(_translate("UpdateWindow", "Current Login:"))
        self.current_account_label.setText(
            _translate("UpdateWindow", "Username: Password:")
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    UpdateWindow = QtWidgets.QMainWindow()
    ui = Ui_UpdateWindow()
    ui.setup2(UpdateWindow)
    UpdateWindow.show()
    sys.exit(app.exec_())
