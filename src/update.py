from PyQt5 import QtCore, QtGui, QtWidgets
from cypher import Cypher

# @Author Joshua Scina
# @Version 1.1


class Ui_UpdateWindow(object):
    def setup2(self, MainWindow):
        MainWindow.setObjectName("UpdateWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
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

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.get_current_login()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # Gets the current login credentials and prints them
    def get_current_login(self):
        cypher = Cypher()
        try:
            with open("login.txt", "rb") as file:
                account = file.readlines()
            file.close()
            username = cypher.decrypt_phrase(account[0])
            password = cypher.decrypt_phrase(account[1])
            self.current_account_label.setText(
                "Username: " + username + " Password: " + password
            )
            self.current_account_label.adjustSize()
        except FileNotFoundError:
            self.current_account_label.setText("Error login.txt doesn't exist")
            self.current_account_label.adjustSize()

    # Changes the login credentials based on the user input
    def update_login(self):
        username_new = self.username.text()
        password_new = self.password.text()
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
            file.close()
            self.get_current_login()
        except FileNotFoundError:
            self.current_account_label.setText("Error: login.txt does not exist")
            self.current_account_label.adjustSize()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Update Login"))
        self.update_button.setText(_translate("MainWindow", "Update"))
        self.u_label.setText(_translate("MainWindow", "Username:"))
        self.p_label.setText(_translate("MainWindow", "Password:"))
        self.current_login_label.setText(_translate("MainWindow", "Current Login:"))
        self.current_account_label.setText(
            _translate("MainWindow", "Username: Password:")
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap("locked.ico"), QtGui.QIcon.Selected, QtGui.QIcon.On)
    MainWindow.setWindowIcon(icon)
    ui = Ui_UpdateWindow()
    ui.setup2(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
