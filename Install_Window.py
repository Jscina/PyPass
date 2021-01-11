import os
import time
from subprocess import Popen

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QThread, pyqtSignal

import location_chooser

# @Version: 3.2
# @Author: Joshua Scina

# Runs in the background during installation
class Worker(QThread):
    countChanged = pyqtSignal(int)

    def __init__(self, location: str):
        super().__init__()
        self.location = location

    # Creates the installation batch file
    def create_install(self):
        path = os.path.abspath("activate.bat")
        with open("install.bat", "w") as file:
            file.write("@echo off \n"
                       "cd %CD%\\python_env\\Scripts\n"
                       "activate.bat && pyinstaller -F -w --i=src\\locked.ico src\\PyPass.py && exit()")

    # Creates the cleanup batch file
    def create_cleanup(self):
        with open("cleanup.bat", "w") as file:
            file.write("@echo off \n"
                       "cd %CD% \n"
                       "mkdir PyPass \n"
                       "copy locked.ico PyPass\\locked.ico \n"
                       "copy LICENSE.txt PyPass\\LICENSE.txt \n"
                       "move /y %CD%\\python_env\\Scripts\\dist\\PyPass.exe %CD%\\PyPass\\PyPass.exe \n"
                       f"move /y %CD%/PyPass {self.location}\n"
                       "rd /s /q python_env \n"
                       "del *.bat")

    # Mainloop of background worker
    def run(self):
        count = 0
        while count < 100:
            count += 1
            if count == 15:
                # Creates the first batch file to build the exe
                self.create_install()
            elif count == 20:
                # Builds the exe
                Popen("install.bat", cwd=os.getcwd(), shell=False)
            elif count == 75:
                # Creates the batch cleanup file
                self.create_cleanup()
            elif count == 85:
                # Runs the cleanup.bat file
                Popen("cleanup.bat", cwd=os.getcwd(), shell=False)
            self.countChanged.emit(count)
            # Wait a second
            time.sleep(1)


class Ui_InstallWindow(object):
    def __init__(self, location: str = "", show_install: bool = False):
        self.location = location
        self.show_install = show_install

    # Open the install location chooser
    def proceed(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = location_chooser.Ui_FileLocationWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        self.install_window.close()

    def setupUi(self, InstallWindow):
        InstallWindow.setObjectName("InstallWindow")
        InstallWindow.resize(800, 600)
        InstallWindow.setStyleSheet("color: rgb(255, 255, 255);\n"
                                    "background-color: rgb(0, 0, 0);")
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.install_window = InstallWindow
        self.install_window.setWindowIcon(QtGui.QIcon(os.path.abspath("locked.ico")))

        self.centralwidget = QtWidgets.QWidget(InstallWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        # This button mirrors the install button but opens the location window
        self.locate_button = QtWidgets.QPushButton(self.centralwidget)
        self.locate_button.setStyleSheet("background-color: rgb(79, 79, 79);")
        self.locate_button.setObjectName("locate_button")
        self.locate_button.clicked.connect(self.proceed)

        # This button allows the install process to start
        self.install_button = QtWidgets.QPushButton(self.centralwidget)
        self.install_button.setStyleSheet("background-color: rgb(79, 79, 79);")
        self.install_button.setObjectName("install_button")
        self.install_button.clicked.connect(self.install)

        # Hide the install button unless location window has been used
        if self.show_install == False:
            self.install_button.hide()
        else:
            self.install_button.show()
            self.locate_button.hide()

        self.gridLayout.addWidget(self.install_button, 4, 1, 1, 2)
        self.gridLayout.addWidget(self.locate_button, 4, 1, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 4)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 7, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 4, 3, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 4, 0, 1, 1)

        # Closes the window when the install is finished
        self.finished_button = QtWidgets.QPushButton(self.centralwidget)
        self.finished_button.setStyleSheet("background-color: rgb(79, 79, 79);")
        self.finished_button.setObjectName("finished_button")
        self.finished_button.clicked.connect(self.done)
        self.finished_button.hide()

        self.gridLayout.addWidget(self.finished_button, 7, 1, 1, 2)

        # Shows the install progress
        self.progress_bar = QtWidgets.QProgressBar(self.centralwidget)
        self.progress_bar.setStyleSheet("")
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setObjectName("progress_bar")
        self.progress_bar.hide()

        self.gridLayout.addWidget(self.progress_bar, 3, 0, 1, 4)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 7, 3, 1, 1)

        self.progress_label = QtWidgets.QLabel(self.centralwidget)
        self.progress_label.setObjectName("progress_label")

        self.gridLayout.addWidget(self.progress_label, 2, 0, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem5, 8, 0, 1, 4)
        InstallWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(InstallWindow)
        QtCore.QMetaObject.connectSlotsByName(InstallWindow)

    def retranslateUi(self, InstallWindow):
        _translate = QtCore.QCoreApplication.translate
        InstallWindow.setWindowTitle(_translate("InstallWindow", "Install"))
        self.install_button.setText(_translate("InstallWindow", "Install"))
        self.locate_button.setText(_translate("InstallWindow", "Install"))
        self.finished_button.setText(_translate("InstallWindow", "Done"))
        self.progress_label.setText(_translate("InstallWindow", "Begin Installation"))

    # Sets up the background worker
    def install(self):
        self.install_button.hide()
        self.progress_bar.show()
        self.progress_label.setText("Installing...")
        self.runner = Worker(self.location)
        self.runner.countChanged.connect(self.onCountChanged)
        self.runner.start()

    # Closes the window
    def done(self):
        self.install_window.close()

    # Updates the progress bar value
    def onCountChanged(self, value):
        self.progress_bar.setValue(value)

        if value == 100:
            self.finished_button.show()
            self.progress_label.setText("Done")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    InstallWindow = QtWidgets.QMainWindow()
    ui = Ui_InstallWindow()
    ui.setupUi(InstallWindow)
    InstallWindow.show()
    sys.exit(app.exec_())
