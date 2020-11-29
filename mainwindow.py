from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QIcon
from serial_cypher import File_Manager
import update, qdarkstyle, os

# @Author: Joshua Scina
# @Version: 2.0


class Ui_MainWindow(object):

    # Switches to the Update Window
    def switch_to_update(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = update.Ui_UpdateWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        self.MainWindow.hide()

    # Builds the Window
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(637, 618)
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        MainWindow.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'locked.ico'))
        self.MainWindow = MainWindow

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Username input
        self.usernames = QtWidgets.QLineEdit(self.centralwidget)
        self.usernames.setGeometry(QtCore.QRect(10, 50, 161, 26))
        self.usernames.setObjectName("usernames")

        # Password Input
        self.passwords = QtWidgets.QLineEdit(self.centralwidget)
        self.passwords.setGeometry(QtCore.QRect(210, 50, 161, 26))
        self.passwords.setObjectName("passwords")

        # Button to add new user
        self.add_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_button.setGeometry(QtCore.QRect(390, 50, 131, 26))
        self.add_button.setObjectName("add_button")
        self.add_button.clicked.connect(self.add_user)

        # Button to remove a single user
        self.remove_user = QtWidgets.QPushButton(self.centralwidget)
        self.remove_user.setGeometry(QtCore.QRect(490, 120, 131, 26))
        self.remove_user.setObjectName("remove_user")
        self.remove_user.clicked.connect(self.remove_user_single)

        # Label above the username input
        self.u_label = QtWidgets.QLabel(self.centralwidget)
        self.u_label.setGeometry(QtCore.QRect(10, 20, 91, 17))
        self.u_label.setObjectName("u_label")

        # Label above the password input
        self.p_label = QtWidgets.QLabel(self.centralwidget)
        self.p_label.setGeometry(QtCore.QRect(210, 20, 81, 17))
        self.p_label.setObjectName("p_label")

        # Label above the Scroll Area
        self.acc_label = QtWidgets.QLabel(self.centralwidget)
        self.acc_label.setGeometry(QtCore.QRect(0, 110, 81, 17))
        self.acc_label.setObjectName("acc_label")

        # Index to remove input
        self.index_input = QtWidgets.QLineEdit(self.centralwidget)
        self.index_input.setGeometry(QtCore.QRect(360, 120, 113, 26))
        self.index_input.setObjectName("index_input")

        # Label above the removal input
        self.index_label = QtWidgets.QLabel(self.centralwidget)
        self.index_label.setGeometry(QtCore.QRect(360, 100, 141, 17))
        self.index_label.setObjectName("index_label")

        # Button to switch to the Update Window
        self.update_login = QtWidgets.QPushButton(self.centralwidget)
        self.update_login.setGeometry(QtCore.QRect(490, 200, 131, 26))
        self.update_login.setObjectName("update_login")
        self.update_login.clicked.connect(self.switch_to_update)

        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(0, 140, 351, 471))
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
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 349, 469))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")

        # The account list label
        self.acc_list = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.acc_list.setObjectName("acc_list")

        self.verticalLayout.addWidget(self.acc_list)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.remove_all_button = QtWidgets.QPushButton(self.centralwidget)
        self.remove_all_button.setGeometry(QtCore.QRect(490, 160, 131, 27))
        self.remove_all_button.setObjectName("remove_all_button")
        self.remove_all_button.clicked.connect(self.remove_user_all)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        # Update the account label on startup
        self.show_user_list()

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def add_user(self):
        manage = File_Manager()
        try:
            # Load the three files
            with open("usernames.txt", "rb") as file:
                account_user = manage.load(file)

            with open("passwords.txt", "rb") as file:
                account_pass = manage.load(file)

            with open("dates.txt", "rb") as file:
                dates = manage.load(file)

            # Append and encrypt the new account
            account_user.append(manage.encrypt(self.usernames.text()))
            account_pass.append(manage.encrypt(self.passwords.text()))
            dates.append(self.getDate())

            # Dump the updated objects into files
            with open("usernames.txt", "wb") as file:
                manage.dump(account_user, file)

            with open("passwords.txt", "wb") as file:
                manage.dump(account_pass, file)

            with open("dates.txt", "wb") as file:
                manage.dump(dates, file)

            # Clear the inputs
            self.usernames.setText("")
            self.passwords.setText("")

            # Update the accounts list
            self.show_user_list()
        except FileNotFoundError:
            # Create the files if they don't exist
            self.fix()

    def remove_user_all(self):
        manage = File_Manager()
        try:
            # Load the three files
            with open("usernames.txt", "rb") as file:
                account_user = manage.load(file)

            with open("passwords.txt", "rb") as file:
                account_pass = manage.load(file)

            with open("dates.txt", "rb") as file:
                dates = manage.load(file)
        except FileNotFoundError:
            # Create the three files if they don't exist
            self.fix()

        # Clear the lists
        account_user.clear()
        account_pass.clear()
        dates.clear()

        # Dump the empty lists into the files
        with open("usernames.txt", "wb") as file:
            manage.dump(account_user, file)

        with open("passwords.txt", "wb") as file:
            manage.dump(account_pass, file)

        with open("dates.txt", "wb") as file:
            manage.dump(dates, file)

        # Update accounts list
        self.show_user_list()

    def remove_user_single(self):
        manage = File_Manager()
        # Get the index input
        index_to_remove = self.index_input.text()
        try:
            # Convert it into an int
            index_to_remove = int(index_to_remove)
        except ValueError:
            # Clear the text and exit the method
            self.index_input.setText("")
            return None
        try:
            # Load the three files
            with open("usernames.txt", "rb") as file:
                account_user = manage.load(file)

            with open("passwords.txt", "rb") as file:
                account_pass = manage.load(file)

            with open("dates.txt", "rb") as file:
                dates = manage.load(file)
        except FileNotFoundError:
            # Create the files if they don't exist
            self.fix()
        try:
            # Delete the specified index from the lists
            del account_user[index_to_remove]
            del account_pass[index_to_remove]
            del dates[index_to_remove]
        except IndexError:
            # Exit and clear input on index error
            self.index_input.setText("")
            return None

        # Dump the updated lists into files
        with open("usernames.txt", "wb") as file:
            manage.dump(account_user, file)

        with open("passwords.txt", "wb") as file:
            manage.dump(account_pass, file)

        with open("dates.txt", "wb") as file:
            manage.dump(dates, file)

        # Clear the index input and update account list
        self.index_input.setText("")
        self.show_user_list()

    def show_user_list(self):
        manage = File_Manager()
        try:
            # Load the three files
            with open("usernames.txt", "rb") as file:
                account_user = manage.load(file)

            with open("passwords.txt", "rb") as file:
                account_pass = manage.load(file)

            with open("dates.txt", "rb") as file:
                dates = manage.load(file)

        except FileNotFoundError:
            # Create the three files if they don't exist and set the variable to empty lists
            self.fix()
            account_user, account_pass, dates = [], [], []

        accounts, account_string = [], ""

        # If the lists aren't empty append the items onto a new list
        if len(account_user) != 0 and len(account_pass) != 0:
            for index in range(len(account_user)):
                accounts.append(
                    str(index)
                    + ": "
                    + manage.decrypt(account_user[index])
                    + " "
                    + manage.decrypt(account_pass[index])
                    + " "
                    + dates[index]
                    + "\n"
                )
            # Convert the list to a string
            for index in range(len(accounts)):
                account_string += accounts[index]
            # Set the account text to the new string
            self.acc_list.setText(account_string)
        else:
            # Set the account text to None
            self.acc_list.setText("None")
        # Update the geometry
        self.acc_list.updateGeometry()

    # Get and return today's date
    def getDate(self):
        today = QDate.currentDate()
        date = today.toString(Qt.DefaultLocaleLongDate)
        return date

    # Create the three files
    def fix(self):
        manage = File_Manager()
        with open("usernames.txt", "wb") as file:
            manage.dump([], file)

        with open("passwords.txt", "wb") as file:
            manage.dump([], file)

        with open("dates.txt", "wb") as file:
            manage.dump([], file)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.add_button.setText(_translate("MainWindow", "Add User"))
        self.remove_user.setText(_translate("MainWindow", "Remove User"))
        self.u_label.setText(_translate("MainWindow", "Username:"))
        self.p_label.setText(_translate("MainWindow", "Password:"))
        self.acc_label.setText(_translate("MainWindow", "Accounts:"))
        self.index_label.setText(_translate("MainWindow", "Index to Remove:"))
        self.update_login.setText(_translate("MainWindow", "Update Login"))
        self.acc_list.setText(_translate("MainWindow", "None"))
        self.remove_all_button.setText(_translate("MainWindow", "Remove All"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
