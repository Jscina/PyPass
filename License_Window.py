import os, Install_Window

from PyQt6 import QtCore, QtGui, QtWidgets

# @Version: 4.0
# @ Author: Joshua Scina
class Ui_LicenseWindow(object):
     # Switch to main install window
    def proceed(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Install_Window.Ui_InstallWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        self.license_window.close()

    def setupUi(self, LicenseWindow):
        LicenseWindow.setObjectName("LicenseWindow")
        LicenseWindow.resize(688, 455)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        LicenseWindow.setFont(font)
        LicenseWindow.setStyleSheet(
            "background-color: rgb(0, 0, 0);\n"
            "                color: rgb(255, 255, 255);\n"
            "            "
        )
        LicenseWindow.setWindowIcon(QtGui.QIcon(os.path.abspath("locked.ico")))
        self.central_widget = QtWidgets.QWidget(LicenseWindow)
        self.central_widget.setObjectName("central_widget")
        self.gridLayout = QtWidgets.QGridLayout(self.central_widget)
        self.gridLayout.setObjectName("gridLayout")
        self.decline_button = QtWidgets.QPushButton(self.central_widget)
        self.decline_button.setStyleSheet(
            "color: rgb(255, 255, 255);\n"
            "                                background-color: rgb(79, 79, 79);\n"
            "                            "
        )
        self.decline_button.setObjectName("decline_button")
        self.decline_button.clicked.connect(self.decline)
        self.gridLayout.addWidget(self.decline_button, 1, 1, 1, 1)
        self.accept_button = QtWidgets.QPushButton(self.central_widget)
        self.accept_button.setStyleSheet(
            "color: rgb(255, 255, 255);\n"
            "                                background-color: rgb(79, 79, 79);\n"
            "                            "
        )
        self.accept_button.setObjectName("accept_button")
        self.accept_button.clicked.connect(self.proceed)
        self.gridLayout.addWidget(self.accept_button, 1, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.listWidget = QtWidgets.QListWidget(self.central_widget)
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.listWidget.addItem(item)
        self.show_license()
        self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 4)
        spacerItem1 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.gridLayout.addItem(spacerItem1, 1, 3, 1, 1)
        LicenseWindow.setCentralWidget(self.central_widget)

        self.retranslateUi(LicenseWindow)
        QtCore.QMetaObject.connectSlotsByName(LicenseWindow)

    def retranslateUi(self, LicenseWindow):
        _translate = QtCore.QCoreApplication.translate
        LicenseWindow.setWindowTitle(_translate("LicenseWindow", "MainWindow"))
        self.decline_button.setText(_translate("LicenseWindow", "Decline"))
        self.accept_button.setText(_translate("LicenseWindow", "Accept"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("LicenseWindow", "License"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
    # If the user doesn't agree to the license close the installer
    def decline(self):
        self.license_window.close()

    # Load in the license from the LICENSE.txt file if not found replace with License Missing
    def get_license(self):
        try:
            with open("LICENSE.txt", "r") as file:
                my_license = file.readlines()
            return my_license
        except FileNotFoundError:
            return ["License Missing"]

    # Show the license
    def show_license(self):
        for line in self.get_license():
            item = QtWidgets.QListWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            item.setText(line)
            self.listWidget.addItem(item)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    LicenseWindow = QtWidgets.QMainWindow()
    ui = Ui_LicenseWindow()
    ui.setupUi(LicenseWindow)
    LicenseWindow.show()
    sys.exit(app.exec())
