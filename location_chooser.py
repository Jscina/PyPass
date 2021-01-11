import os

from PyQt5 import QtCore, QtWidgets, QtGui

import Install_Window


# @Version: 3.2
# @Author: Joshua Scina

class Ui_FileLocationWindow(object):
    # Reopen the main installation window with new parameters
    def proceed(self, locate: str = "", show_install: bool = False):
        self.window = QtWidgets.QMainWindow()
        self.ui = Install_Window.Ui_InstallWindow(location=locate, show_install=show_install)
        self.ui.setupUi(self.window)
        self.window.show()
        self.FileLocationWindow.close()

    def setupUi(self, FileLocationWindow):
        FileLocationWindow.setObjectName("FileLocationWindow")
        FileLocationWindow.resize(634, 293)
        FileLocationWindow.setStyleSheet("color: rgb(255, 255, 255);\n"
                                         "background-color: rgb(0, 0, 0);")
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.FileLocationWindow = FileLocationWindow
        self.FileLocationWindow.setWindowIcon(QtGui.QIcon(os.path.abspath("locked.ico")))

        self.centralwidget = QtWidgets.QWidget(FileLocationWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 3)

        # Reopens the main installation window with the default parameters
        self.cancel_button = QtWidgets.QPushButton(self.centralwidget)
        self.cancel_button.setStyleSheet("background-color: rgb(79, 79, 79);")
        self.cancel_button.setObjectName("cancel_button")
        self.cancel_button.clicked.connect(self.cancel)

        self.gridLayout.addWidget(self.cancel_button, 3, 1, 1, 1)
        self.install_label = QtWidgets.QLabel(self.centralwidget)
        self.install_label.setObjectName("install_label")

        self.gridLayout.addWidget(self.install_label, 2, 0, 1, 1)

        # Allows user to specify install location
        self.install_location = QtWidgets.QLineEdit(self.centralwidget)
        self.install_location.setStyleSheet("background-color: rgb(79, 79, 79);\n"
                                            "border-radius: 5px;\n"
                                            "border-style: none;")
        self.install_location.setObjectName("install_location")

        self.gridLayout.addWidget(self.install_location, 3, 0, 1, 1)

        # Runs the ok() function
        self.ok_button = QtWidgets.QPushButton(self.centralwidget)
        self.ok_button.setStyleSheet("background-color: rgb(79, 79, 79);")
        self.ok_button.setObjectName("ok_button")
        self.ok_button.clicked.connect(self.ok)

        self.gridLayout.addWidget(self.ok_button, 3, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 3)
        FileLocationWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(FileLocationWindow)
        QtCore.QMetaObject.connectSlotsByName(FileLocationWindow)

    def retranslateUi(self, FileLocationWindow):
        _translate = QtCore.QCoreApplication.translate
        FileLocationWindow.setWindowTitle(_translate("FileLocationWindow", "Choose Install Location"))
        self.cancel_button.setText(_translate("FileLocationWindow", "Cancel"))
        self.install_label.setText(_translate("FileLocationWindow", "Choose Install Location:"))
        self.install_location.setPlaceholderText(
            _translate("FileLocationWindow", "Default: C:/PyPass Warning: Use / character for paths only!!!"))
        self.ok_button.setText(_translate("FileLocationWindow", "Ok"))

    # Return to the main install window with default parameters
    def cancel(self):
        self.proceed()

    # Return to the main install window with new parameters
    def ok(self):
        choice = self.install_location.text()
        self.install_location.clear()
        # If the path exists continue
        if os.path.exists(choice.removesuffix("/")):
            self.proceed(choice.removesuffix("/"), True)
        # If the field is empty continue
        elif choice == "":
            self.proceed("C:/PyPass", True)
        # If the field isn't empty and doesn't exist
        else:
            self.install_location.setPlaceholderText(f"Error path doesn't exist: {choice} Default: C:/PyPass Warning: Use / character for paths only!!!")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    FileLocationWindow = QtWidgets.QMainWindow()
    ui = Ui_FileLocationWindow()
    ui.setupUi(FileLocationWindow)
    FileLocationWindow.show()
    sys.exit(app.exec_())
