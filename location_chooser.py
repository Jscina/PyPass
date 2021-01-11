import os
import Install_Window

from PyQt5 import QtCore, QtWidgets, QtGui



class Ui_FileLocationWindow(object):
    def proceed(self, locate: str):
        self.window = QtWidgets.QMainWindow()
        self.ui = Install_Window.Ui_InstallWindow(location=locate, show_install = True)
        self.ui.setupUi(self.window)
        self.window.show()
        self.FileLocationWindow.close()

    def setupUi(self, FileLocationWindow):
        FileLocationWindow.setObjectName("FileLocationWindow")
        FileLocationWindow.resize(634, 293)
        FileLocationWindow.setStyleSheet("color: rgb(255, 255, 255);\n"
                                         "background-color: rgb(0, 0, 0);")
        self.FileLocationWindow = FileLocationWindow
        self.FileLocationWindow.setWindowIcon(QtGui.QIcon(os.path.abspath("locked.ico")))

        self.centralwidget = QtWidgets.QWidget(FileLocationWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 3)

        self.cancel_button = QtWidgets.QPushButton(self.centralwidget)
        self.cancel_button.setStyleSheet("background-color: rgb(79, 79, 79);")
        self.cancel_button.setObjectName("cancel_button")
        self.cancel_button.clicked.connect(self.cancel)

        self.gridLayout.addWidget(self.cancel_button, 3, 1, 1, 1)
        self.install_label = QtWidgets.QLabel(self.centralwidget)
        self.install_label.setObjectName("install_label")

        self.gridLayout.addWidget(self.install_label, 2, 0, 1, 1)

        self.install_location = QtWidgets.QLineEdit(self.centralwidget)
        self.install_location.setStyleSheet("background-color: rgb(79, 79, 79);\n"
                                            "border-radius: 5px;\n"
                                            "border-style: none;")
        self.install_location.setText("")
        self.install_location.setObjectName("install_location")

        self.gridLayout.addWidget(self.install_location, 3, 0, 1, 1)

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
        self.install_location.setPlaceholderText(_translate("FileLocationWindow", "Default: C:/PyPass Warning: Use / character for paths only!!!"))
        self.ok_button.setText(_translate("FileLocationWindow", "Ok"))

    def cancel(self):
        self.FileLocationWindow.close()

    def ok(self):
        choice = self.install_location.text()
        self.install_location.clear()
        if choice == "":
            self.proceed("C:/PyPass")
        else:
            self.proceed(choice)



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    FileLocationWindow = QtWidgets.QMainWindow()
    ui = Ui_FileLocationWindow()
    ui.setupUi(FileLocationWindow)
    FileLocationWindow.show()
    sys.exit(app.exec_())
