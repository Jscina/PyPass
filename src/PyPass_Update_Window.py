import os, datetime, PyPass_Main_Window

from PyQt6 import QtCore, QtGui, QtWidgets
from serial_cypher import File_Manager

# @Version: 4.0
# @ Author: Joshua Scina

class Ui_UpdateWindow(object):
    def __init__(self):
        self._crypter = File_Manager()

    # Reopen Main Window
    def _Main_Window(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = PyPass_Main_Window.Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        UpdateWindow.close()

    def setupUi(self, UpdateWindow):
        UpdateWindow.setObjectName("UpdateWindow")
        UpdateWindow.resize(647, 229)
        UpdateWindow.setStyleSheet("background-color: rgb(0, 0, 0);")

        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        UpdateWindow.setWindowIcon(QtGui.QIcon(os.path.abspath("locked.ico")))

        self.centralwidget = QtWidgets.QWidget(UpdateWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.username = QtWidgets.QLineEdit(self.centralwidget)
        self.username.setStyleSheet(
            "color: rgb(255, 255, 255);\n"
            "                                gridline-color: rgb(0, 0, 0);\n"
            "                                background-color: rgb(80, 80, 80);\n"
            "                                border-radius: 5px;\n"
            "                            "
        )
        self.username.setObjectName("username")
        self.gridLayout.addWidget(self.username, 2, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.gridLayout.addItem(spacerItem, 2, 5, 3, 1)
        spacerItem1 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.gridLayout.addItem(spacerItem1, 1, 0, 5, 1)
        spacerItem2 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.gridLayout.addItem(spacerItem2, 0, 1, 1, 4)
        self.current_account_label = QtWidgets.QLabel(self.centralwidget)
        self.current_account_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.current_account_label.setObjectName("current_account_label")
        self.gridLayout.addWidget(self.current_account_label, 5, 1, 1, 3)
        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setStyleSheet(
            "color: rgb(255, 255, 255);\n"
            "                                gridline-color: rgb(0, 0, 0);\n"
            "                                background-color: rgb(80, 80, 80);\n"
            "                                border-radius: 5px;\n"
            "                            "
        )
        self.password.setObjectName("password")
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.gridLayout.addWidget(self.password, 2, 3, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.gridLayout.addItem(spacerItem3, 6, 1, 1, 4)
        self.current_login_label = QtWidgets.QLabel(self.centralwidget)
        self.current_login_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.current_login_label.setObjectName("current_login_label")
        self.gridLayout.addWidget(self.current_login_label, 4, 1, 1, 1)
        self.done = QtWidgets.QPushButton(self.centralwidget)
        self.done.setStyleSheet(
            "color: rgb(255, 255, 255);\n"
            "                                background-color: rgb(79, 79, 79);\n"
            "                            "
        )
        self.done.setObjectName("done")
        self.done.clicked.connect(self._Main_Window)
        self.gridLayout.addWidget(self.done, 4, 4, 1, 1)
        self.update_button = QtWidgets.QPushButton(self.centralwidget)
        self.update_button.setStyleSheet(
            "color: rgb(255, 255, 255);\n"
            "                                background-color: rgb(79, 79, 79);\n"
            "                            "
        )
        self.update_button.setObjectName("update_button")
        self.update_button.clicked.connect(self.update_login)

        self.gridLayout.addWidget(self.update_button, 2, 4, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.gridLayout.addItem(spacerItem4, 4, 3, 1, 1)
        self.p_label = QtWidgets.QLabel(self.centralwidget)
        self.p_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.p_label.setObjectName("p_label")
        self.gridLayout.addWidget(self.p_label, 1, 3, 1, 1)
        self.u_label = QtWidgets.QLabel(self.centralwidget)
        self.u_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.u_label.setObjectName("u_label")
        self.gridLayout.addWidget(self.u_label, 1, 1, 1, 1)
        UpdateWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(UpdateWindow)
        QtCore.QMetaObject.connectSlotsByName(UpdateWindow)

    def retranslateUi(self, UpdateWindow):
        _translate = QtCore.QCoreApplication.translate
        UpdateWindow.setWindowTitle(_translate("UpdateWindow", "Update Login"))
        self.current_account_label.setText(_translate("UpdateWindow", self.show_current()))
        self.current_login_label.setText(_translate("UpdateWindow", "Current Login:"))
        self.done.setText(_translate("UpdateWindow", "Done"))
        self.update_button.setText(_translate("UpdateWindow", "Update"))
        self.p_label.setText(_translate("UpdateWindow", "Password:"))
        self.u_label.setText(_translate("UpdateWindow", "Username:"))

        
    # Shows the current login
    def show_current(self):
        data = self._crypter.load_data()
        username = self._crypter.decrypt(data[0][0], data[2][0])
        password = self._crypter.decrypt(data[1][0], data[2][0])
        text = "Username: " + username + " Password: " + password
        self.current_account_label.setText(text)
        self.current_account_label.updateGeometry()
        del data, username, password
        return text

    # Updates the old login with the new one
    def update_login(self):
        key = self._crypter.gen_key()
        username = self._crypter.encrypt(self.username.text(), key)
        password = self._crypter.encrypt(self.password.text(), key)
        date = datetime.datetime.now()
        data = self._crypter.load_data()
        data[0][0], data[1][0], data[2][0], data[3][0], data[4][0] = username, password, key, date.strftime(
            "%x"), [""]
        del username, password, key, date
        self.username.clear()
        self.password.clear()
        self._crypter.dump_data(data)
        temp = self.show_current()
        del temp


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    UpdateWindow = QtWidgets.QMainWindow()
    ui = Ui_UpdateWindow()
    ui.setupUi(UpdateWindow)
    UpdateWindow.show()
    sys.exit(app.exec())
