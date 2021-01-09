import os
import subprocess
import time

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QThread, pyqtSignal


class Worker(QThread):
    countChanged = pyqtSignal(int)

    def run(self):
        os.chdir(os.curdir)
        path_start, path_end = "start.vbs", "end.vbs"
        count = 0
        while count < 100:
            count += 1
            if count == 15:
                with open("install_start.bat", "w") as file:
                    file.write("""
                    @echo off\n
                    %CD%\\python_env\\Scripts\\activate.bat pip install cryptography PyQt5 && pyinstaller -F -w -i=locked.ico %CD%\\src\\PyPass.py && %CD%\\python_env\\Scripts\\deactivate.bat
                    """)
            elif count == 35:
                with open("start.vbs", "w") as file:
                    file.write("Set WshShell = CreateObject(\"WScript.Shell\")\n")
                    file.write(f"WshShell.Run chr(34) & \"{os.path.abspath('install_start.bat')}\" & Chr(34), 0\n")
                    file.write("set WshShell = Nothing\n")
            elif count == 50:
                subprocess.call(f"cmd /c {path_start}")
            elif count == 75:
                with open("install_end.bat", "w") as file:
                    file.write("""
                                @echo off \n
                                rd /s /q %CD%\\python_env \n
                                mkdir %CD%\\PyPass \n
                                copy %CD%\\locked.ico %CD%\\PyPass\\locked.ico \n
                                copy %CD%\\LICENSE.txt %CD%\\PyPass\\LICENSE.txt \n
                                rd /s /q %CD%\\build \n
                                move /y %CD%\\dist\\PyPass.exe %CD%\\PyPass\\PyPass.exe \n
                                rd /s /q %CD%\\dist \n
                                del %CD%\\PyPass.spec \n
                                rd /s /q %CD%\\src \n
                                move %CD%\\PyPass C:\\PyPass\n
                                del %CD%\\*.vbs\n
                                del %CD%\\*.bat
                                """)
            elif count == 80:
                with open("end.vbs", "w") as file:
                    file.write("Set WshShell = CreateObject(\"WScript.Shell\")\n")
                    file.write(f"WshShell.Run chr(34) & \"{os.path.abspath('install_end.bat')}\" & Chr(34), 0\n")
                    file.write("set WshShell = Nothing\n")
            elif count == 90:
                subprocess.call(f"cmd /c {path_end}")
            self.countChanged.emit(count)
            time.sleep(0.5)


class Ui_InstallWindow(object):
    def setupUi(self, InstallWindow):
        InstallWindow.setObjectName("InstallWindow")
        InstallWindow.resize(800, 600)
        InstallWindow.setStyleSheet("color: rgb(255, 255, 255);\n"
                                    "background-color: rgb(0, 0, 0);")
        self.install_window = InstallWindow
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.install_window.setWindowIcon(QtGui.QIcon(
            scriptDir + os.path.sep + 'locked.ico'))

        self.centralwidget = QtWidgets.QWidget(InstallWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.instal_button = QtWidgets.QPushButton(self.centralwidget)
        self.instal_button.setStyleSheet("background-color: rgb(79, 79, 79);")
        self.instal_button.setObjectName("instal_button")
        self.instal_button.clicked.connect(self.install)

        self.gridLayout.addWidget(self.instal_button, 4, 1, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 4)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 7, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 4, 3, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 4, 0, 1, 1)

        self.finished_button = QtWidgets.QPushButton(self.centralwidget)
        self.finished_button.setStyleSheet("background-color: rgb(79, 79, 79);")
        self.finished_button.setObjectName("finished_button")
        self.finished_button.clicked.connect(self.done)
        self.finished_button.hide()

        self.gridLayout.addWidget(self.finished_button, 7, 1, 1, 2)

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
        InstallWindow.setWindowTitle(_translate("InstallWindow", "MainWindow"))
        self.instal_button.setText(_translate("InstallWindow", "Install"))
        self.finished_button.setText(_translate("InstallWindow", "Done"))
        self.progress_label.setText(_translate("InstallWindow", "Begin Installation"))

    def install(self):
        self.instal_button.hide()
        self.progress_bar.show()
        self.progress_label.setText("Installing...")
        self.runner = Worker()
        self.runner.countChanged.connect(self.onCountChanged)
        self.runner.start()

    def done(self):
        self.install_window.close()

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
