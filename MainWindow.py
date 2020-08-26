from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate, Qt
from cryptography.fernet import Fernet
from cypher import Cypher
import update


# @Author Joshua Scina
# @Version 1.6.1
# Do not try to run this file on it's own it will not function properly


class Ui_MainWindow(object):
    def switch(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = update.Ui_UpdateWindow()
        self.ui.setup2(self.window)
        self.window.show()
        self.MainWindow.hide()

    def setup(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setWindowIcon(QIcon("locked.ico"))

        self.MainWindow = MainWindow
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.usernames = QtWidgets.QLineEdit(self.centralwidget)
        self.usernames.setGeometry(QtCore.QRect(130, 140, 161, 26))
        self.usernames.setObjectName("usernames")

        self.passwords = QtWidgets.QLineEdit(self.centralwidget)
        self.passwords.setGeometry(QtCore.QRect(340, 140, 161, 26))
        self.passwords.setObjectName("passwords")

        self.add_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_button.setGeometry(QtCore.QRect(520, 140, 89, 26))
        self.add_button.setObjectName("add_button")
        self.add_button.clicked.connect(self.add_user)

        self.update_button = QtWidgets.QPushButton(self.centralwidget)
        self.update_button.setGeometry(500, 260, 131, 26)
        self.update_button.setObjectName("update_button")
        self.update_button.setText("Update Login")
        self.update_button.clicked.connect(self.switch)

        self.remove_button = QtWidgets.QPushButton(self.centralwidget)
        self.remove_button.setGeometry(QtCore.QRect(500, 220, 131, 26))
        self.remove_button.setObjectName("remove_button")
        self.remove_button.clicked.connect(self.remove_user)

        self.u_label = QtWidgets.QLabel(self.centralwidget)
        self.u_label.setGeometry(QtCore.QRect(140, 110, 91, 17))
        self.u_label.setObjectName("u_label")

        self.acc_label = QtWidgets.QLabel(self.centralwidget)
        self.acc_label.setGeometry(QtCore.QRect(130, 210, 81, 17))
        self.acc_label.setObjectName("acc_label")

        self.p_label = QtWidgets.QLabel(self.centralwidget)
        self.p_label.setGeometry(QtCore.QRect(340, 110, 81, 17))
        self.p_label.setObjectName("p_label")

        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(80, 240, 271, 261))

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())

        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 267, 257))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")

        self.acc_list = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.acc_list.setObjectName("acc_list")

        self.verticalLayout.addWidget(self.acc_list)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.index_input = QtWidgets.QLineEdit(self.centralwidget)
        self.index_input.setGeometry(QtCore.QRect(370, 220, 113, 26))
        self.index_input.setObjectName("index_input")

        self.index_label = QtWidgets.QLabel(self.centralwidget)
        self.index_label.setGeometry(QtCore.QRect(370, 200, 141, 17))
        self.index_label.setObjectName("index_label")

        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.show_users()

    # This function adds a new account to the list
    def add_user(self):
        cypher, users, passwords= Cypher(), self.usernames.text(), self.passwords.text()
        try:
            with open("usernames.txt", "ab") as file:
                file.write(cypher.encrypt_phrase(users) + b"\n")

            with open("passwords.txt", "ab") as file:
                file.write(cypher.encrypt_phrase(passwords) + b"\n")

            with open("date-added.txt", "a") as file:
                file.write(self.getDate() + "\n")

        except FileNotFoundError:
            self.fix()

        self.passwords.setText("")
        self.usernames.setText("")
        self.show_users()

    # Gets today's date
    def getDate(self):
        today = QDate.currentDate()
        date = today.toString(Qt.DefaultLocaleLongDate)
        return date

    # Creates the username and password files if they don't exist
    def fix(self):
        with open("usernames.txt", "wb") as file:
            file.write(b"")
        with open("passwords.txt", "wb") as file:
            file.write(b"")
        with open("date-added.txt", "w") as file:
            file.write("")
    # This function prints the list of accounts on the screen
    def show_users(self):
        cypher, account_pair, acc = Cypher(), [], ""
        try:
            with open("usernames.txt", "rb") as file:
                usernames_list = file.readlines()

            with open("passwords.txt", "rb") as file:
                passwords_list = file.readlines()

            with open("date-added.txt", "r") as file:
                date_list = file.readlines()

        except FileNotFoundError:
            self.fix()
            usernames_list = []
            passwords_list = []

        if len(usernames_list) != 0 and len(passwords_list) != 0:
            for index in range(len(usernames_list)):
                account_pair.append(
                    str(index)
                    + ": "
                    + cypher.decrypt_phrase(usernames_list[index])
                    + "     "
                    + cypher.decrypt_phrase(passwords_list[index])
                    + "     " 
                    + date_list[index] 
                    + "\n"
                )
            for index in range(len(account_pair)):
                acc += account_pair[index]
                self.acc_list.setText(acc)
        else:
            self.acc_list.setText("None")
        self.update()

    # This function removes a user from the list then remakes the file
    def remove_user(self):
        try:
            index = int(self.index_input.text())

            with open("usernames.txt", "rb") as file:
                u_list = file.readlines()

            with open("passwords.txt", "rb") as file:
                p_list = file.readlines()

            with open("date-added.txt", "r") as file:
                d_list = file.readlines()
            # Remove the index specified
            u_list[index] = None
            u_list.remove(None)

            p_list[index] = None
            p_list.remove(None)

            d_list[index] = None
            d_list.remove(None)

            # Remove all line formatting
            while u_list.count(b"\n") > 0:
                u_list.remove(b"\n")

            while p_list.count(b"\n") > 0:
                p_list.remove(b"\n")

            while d_list.count("\n") > 0:
                d_list.remove("\n")

            # Empty the files
            with open("usernames.txt", "wb") as file:
                file.write(b"")

            with open("passwords.txt", "wb") as file:
                file.write(b"")

            with open("date-added.txt", "w") as file:
                file.write("")

            # Rewrite the files with the new list
            with open("usernames.txt", "ab") as file:
                for index in range(len(u_list)):
                    file.write(u_list[index])
        
            with open("passwords.txt", "ab") as file:
                for index in range(len(u_list)):
                    file.write(p_list[index])

            with open("date-added.txt", "a") as file:
                for index in range(len(d_list)):
                    file.write(d_list[index])
       
        except FileNotFoundError:
            self.fix()
        except ValueError:
            index = 0
        except IndexError:
            self.index_input.setText("")

        self.index_input.setText("")
        self.show_users()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PyPass"))
        self.add_button.setText(_translate("MainWindow", "Add User"))
        self.remove_button.setText(_translate("MainWindow", "Remove User"))
        self.u_label.setText(_translate("MainWindow", "Username:"))
        self.p_label.setText(_translate("MainWindow", "Password:"))
        self.acc_label.setText(_translate("MainWindow", "Accounts:"))
        self.acc_list.setText(_translate("MainWindow", "None"))
        self.index_label.setText(_translate("MainWindow", "Index to Remove:"))

    def update(self):
        self.acc_list.adjustSize()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setup(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
