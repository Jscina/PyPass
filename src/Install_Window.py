import os, time, subprocess, Location_Chooser, Create_EXE, random

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QThread, pyqtSignal



# @Version: 4.0
# @ Author: Joshua Scina

class Worker(QThread):
    countChanged = pyqtSignal(int)

    def __init__(self, location: str):
        super().__init__()
        self.location = location

    def hide_script(self, run_file: str):
        path = os.path.abspath(run_file)
        with open("run_script.vbs", "w") as file:
            file.write(
                'Set WshShell = CreateObject("WScript.Shell")\n'
                f'WshShell.Run chr(34) & "{path}" & Chr(34), 0\n'
                "Set WshShell = None"
            )
        return path

       
    # Creates the PyPass files
    def _install(self):
        build = Create_EXE(["PyPass"])
        build.run()

    # Creates the cleanup batch file
    def create_cleanup(self):
        with open("cleanup.bat", "w") as file:
            file.write(
                "@echo off\n"
                "cd %CD%\n"
                "move /y python_env\\Scripts\\dist\\PyPass PyPass\n"
                "copy locked.ico PyPass\\locked.ico\n"
                "copy LICENSE.txt PyPass\\LICENSE.txt\n"
                f"move /y PyPass {self.location}\n"
                "rd /s /q python_env\n"
                "del *.vbs\n"
                "del *.bat"
            )

    # Mainloop of background worker
    def run(self):
        count = 0
        while count < 100:
            count += random.randint(1,6)
            if count == 25:
                self._install()
            elif count == 75:
                # Creates the batch cleanup file
                self.create_cleanup()
            elif count == 85:
                # Hides the script
                path = self.hide_script("cleanup.bat")
            elif count == 90:
                # Runs the cleanup.bat file
                subprocess.run(path, shell=False)
            self.countChanged.emit(count)
            # Wait a second
            time.sleep(1)


class Ui_InstallWindow(object):
    def __init__(self, location: str = "", show_install: bool = False):
        self.location = location
        self.show_install = show_install

    def setupUi(self, InstallWindow):
        InstallWindow.setObjectName("InstallWindow")
        InstallWindow.resize(800, 600)
        InstallWindow.setStyleSheet(
            "color: rgb(255, 255, 255);\n"
            "                background-color: rgb(0, 0, 0);\n"
            "            "
        )

        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.install_window = InstallWindow
        self.install_window.setWindowIcon(QtGui.QIcon(os.path.abspath("locked.ico")))

        self.centralwidget = QtWidgets.QWidget(InstallWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)

        self.gridLayout.setObjectName("gridLayout")
        # This button allows the install process to start
        self.install_button = QtWidgets.QPushButton(self.centralwidget)
        self.install_button.setStyleSheet("background-color: rgb(79, 79, 79);")
        self.install_button.setObjectName("install_button")
        self.install_button.clicked.connect(self.install)
        self.gridLayout.addWidget(self.install_button, 4, 1, 1, 2)

        spacerItem = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )

        self.gridLayout.addItem(spacerItem, 1, 0, 1, 4)
        spacerItem1 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )

        self.gridLayout.addItem(spacerItem1, 7, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )

        self.gridLayout.addItem(spacerItem2, 4, 3, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.gridLayout.addItem(spacerItem3, 4, 0, 1, 1)
        # This button mirrors the install button but opens the location window
        self.locate_button = QtWidgets.QPushButton(self.centralwidget)
        self.locate_button.setStyleSheet("background-color: rgb(79, 79, 79);")
        self.locate_button.setObjectName("locate_button")
        self.locate_button.clicked.connect(self.proceed)

        # Closes the window when the install is finished
        self.finished_button = QtWidgets.QPushButton(self.centralwidget)
        self.finished_button.setStyleSheet("background-color: rgb(79, 79, 79);")
        self.finished_button.setObjectName("finished_button")
        self.finished_button.clicked.connect(self.done)
        self.finished_button.hide()

        self.gridLayout.addWidget(self.locate_button, 7, 1, 1, 2)

        self.progress_bar = QtWidgets.QProgressBar(self.centralwidget)
        self.progress_bar.setStyleSheet("")
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setObjectName("progress_bar")
        self.gridLayout.addWidget(self.progress_bar, 3, 0, 1, 4)
        spacerItem4 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.gridLayout.addItem(spacerItem4, 7, 3, 1, 1)
        self.progress_label = QtWidgets.QLabel(self.centralwidget)
        self.progress_label.setObjectName("progress_label")
        self.gridLayout.addWidget(self.progress_label, 2, 0, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.gridLayout.addItem(spacerItem5, 8, 0, 1, 4)
        InstallWindow.setCentralWidget(self.centralwidget)

         # Closes the window when the install is finished
        self.finished_button = QtWidgets.QPushButton(self.centralwidget)
        self.finished_button.setStyleSheet("background-color: rgb(79, 79, 79);")
        self.finished_button.setObjectName("finished_button")
        self.finished_button.clicked.connect(self.done)
        self.finished_button.hide()

        self.retranslateUi(InstallWindow)
        QtCore.QMetaObject.connectSlotsByName(InstallWindow)

        # Hide the install button unless location window has been used
        if self.show_install == False:
            self.install_button.hide()
        else:
            self.install_button.show()
            self.locate_button.hide()

    # Open the install location chooser
    def proceed(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Location_Chooser.Ui_FileLocationWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        self.install_window.close()

    def retranslateUi(self, InstallWindow):
        _translate = QtCore.QCoreApplication.translate
        InstallWindow.setWindowTitle(_translate("InstallWindow", "MainWindow"))
        self.install_button.setText(_translate("InstallWindow", "Install"))
        self.locate_button.setText(_translate("InstallWindow", "Install"))
        self.finished_button.setText(_translate("InstallWindow", "Done"))
        self.progress_label.setText(_translate("InstallWindow", "Waiting..."))

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
    sys.exit(app.exec())
