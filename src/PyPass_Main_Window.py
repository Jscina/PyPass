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
##### ** Imports needed to run program: ** ######
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import PyPass_Update_Window

from PyQt6 import QtCore, QtGui, QtWidgets
from PyPass_Engine import Main_Window_Methods, General_Purpose

class Ui_MainWindow(object):

    def __init__(self):
        self.main_window_methods = Main_Window_Methods()
        self.general = General_Purpose()
        
    # Opens update window
    def _Update_Window(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = PyPass_Update_Window.Ui_UpdateWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        self.MainWindow.close()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(637, 618)
        MainWindow.setStyleSheet(
            "background-color: rgb(0, 0, 0);\n"
            "color: rgb(255, 255, 255);\n"
        )
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        MainWindow.setWindowIcon(QtGui.QIcon(self.general.get_icon_path()))
        self.MainWindow = MainWindow
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.index_label = QtWidgets.QLabel(self.centralwidget)
        self.index_label.setObjectName("index_label")
        self.gridLayout.addWidget(self.index_label, 3, 4, 1, 2)
        self.p_label = QtWidgets.QLabel(self.centralwidget)
        self.p_label.setObjectName("p_label")
        self.gridLayout.addWidget(self.p_label, 1, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setStyleSheet("")
        self.listWidget.setMovement(QtWidgets.QListView.Movement.Static)
        self.listWidget.setResizeMode(QtWidgets.QListView.ResizeMode.Adjust)
        self.listWidget.setObjectName("listWidget")
        self.listWidget.addItem(self.main_window_methods.check_for_accounts())
        
        self.gridLayout.addWidget(self.listWidget, 7, 1, 1, 3)
        self.usernames = QtWidgets.QLineEdit(self.centralwidget)
        self.usernames.setStyleSheet(
            "color: rgb(255, 255, 255);\n"
            "                                gridline-color: rgb(0, 0, 0);\n"
            "                                background-color: rgb(80, 80, 80);\n"
            "                                border-radius: 5px;\n"
            "                            "
        )
        self.usernames.setObjectName("usernames")
        self.gridLayout.addWidget(self.usernames, 2, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.gridLayout.addItem(spacerItem1, 1, 7, 7, 1)
        self.index_input = QtWidgets.QLineEdit(self.centralwidget)
        self.index_input.setStyleSheet(
            "color: rgb(255, 255, 255);\n"
            "                                gridline-color: rgb(0, 0, 0);\n"
            "                                background-color: rgb(80, 80, 80);\n"
            "                                border-radius: 5px;\n"
            "                            "
        )
        self.index_input.setObjectName("index_input")
        self.gridLayout.addWidget(self.index_input, 4, 4, 1, 2)
        self.web_label = QtWidgets.QLabel(self.centralwidget)
        self.web_label.setObjectName("web_label")
        self.gridLayout.addWidget(self.web_label, 1, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.gridLayout.addItem(spacerItem2, 1, 0, 7, 1)
        self.update_login = QtWidgets.QPushButton(self.centralwidget)
        self.update_login.setStyleSheet(
            "color: rgb(255, 255, 255);\n"
            "                                background-color: rgb(79, 79, 79);\n"
            "                            "
        )
        self.update_login.setObjectName("update_login")
        self.update_login.clicked.connect(self._Update_Window)

        self.gridLayout.addWidget(self.update_login, 6, 6, 1, 1)
        self.add_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_button.setStyleSheet(
            "color: rgb(255, 255, 255);\n"
            "                                background-color: rgb(79, 79, 79);\n"
            "                            "
        )
        self.add_button.setObjectName("add_button")
        self.add_button.clicked.connect(self.add_user)
        self.gridLayout.addWidget(self.add_button, 2, 4, 1, 2)
        self.acc_label = QtWidgets.QLabel(self.centralwidget)
        self.acc_label.setObjectName("acc_label")
        self.gridLayout.addWidget(self.acc_label, 6, 1, 1, 1)
        self.remove_user = QtWidgets.QPushButton(self.centralwidget)
        self.remove_user.setStyleSheet(
            "color: rgb(255, 255, 255);\n"
            "                                background-color: rgb(79, 79, 79);\n"
            "                            "
        )
        self.remove_user.setObjectName("remove_user")
        self.remove_user.clicked.connect(self.remove)
        self.gridLayout.addWidget(self.remove_user, 4, 6, 1, 1)
        self.website_input = QtWidgets.QLineEdit(self.centralwidget)
        self.website_input.setStyleSheet(
            "color: rgb(255, 255, 255);\n"
            "                                gridline-color: rgb(0, 0, 0);\n"
            "                                background-color: rgb(80, 80, 80);\n"
            "                                border-radius: 5px;\n"
            "                            "
        )
        self.website_input.setObjectName("website_input")
        self.gridLayout.addWidget(self.website_input, 2, 1, 1, 1)

        self.passwords = QtWidgets.QLineEdit(self.centralwidget)
        self.passwords.setStyleSheet(
            "color: rgb(255, 255, 255);\n"
            "                                gridline-color: rgb(0, 0, 0);\n"
            "                                background-color: rgb(80, 80, 80);\n"
            "                                border-radius: 5px;\n"
            "                            "
        )
        self.passwords.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.passwords.setObjectName("passwords")

        self.gridLayout.addWidget(self.passwords, 2, 3, 1, 1)
        self.u_label = QtWidgets.QLabel(self.centralwidget)
        self.u_label.setObjectName("u_label")
        self.gridLayout.addWidget(self.u_label, 1, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.gridLayout.addItem(spacerItem3, 8, 0, 1, 8)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.listWidget.addItem("")
        item = self.listWidget.item(0)

        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.index_label.setText(_translate("MainWindow", "Index to Remove:"))
        self.p_label.setText(_translate("MainWindow", "Password:"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item.setText(_translate("MainWindow", "None"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.web_label.setText(_translate("MainWindow", "Website"))
        self.update_login.setText(_translate("MainWindow", "Update Login"))
        self.add_button.setText(_translate("MainWindow", "Add User"))
        self.acc_label.setText(_translate("MainWindow", "Accounts:"))
        self.remove_user.setText(_translate("MainWindow", "Remove User"))
        self.u_label.setText(_translate("MainWindow", "Username:"))
    
    # Load and display accounts
    def show_accounts(self):
        self.listWidget.clear()
        account_list: list = self.main_window_methods.show_accounts()
        self.listWidget.addItems(account_list)

    # Remove account at the index
    def remove(self):
        try:
            self.main_window_methods.remove_accounts(account_to_be_removed = int(self.index_input.text()))
            self.show_accounts()
            self.index_input.clear()
        except ValueError:
            self.index_input.clear()
        except IndexError:
            self.index_input.clear()

    # Add a user to the storage file then show accounts
    def add_user(self):
        self.main_window_methods.add_user(username = self.usernames.text(), password = self.passwords.text(), website = self.website_input.text())
        self.usernames.clear()
        self.passwords.clear()
        self.website_input.clear()
        self.show_accounts()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
