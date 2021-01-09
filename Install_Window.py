from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QThread, pyqtSignal
import Installer, os, time

class Worker(QThread):
    countChanged = pyqtSignal(int)

    def run(self):
        count = 0
        while count < 100:
            count += 1
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
            self.install_script()
            self.finished_button.show()
            self.progress_label.setText("Done")

    def install_script(self):
        self.installer = Installer()




if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    InstallWindow = QtWidgets.QMainWindow()
    ui = Ui_InstallWindow()
    ui.setupUi(InstallWindow)
    InstallWindow.show()
    sys.exit(app.exec_())
