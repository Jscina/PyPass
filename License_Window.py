from PyQt5 import QtCore, QtGui, QtWidgets
import Install_Window, os


class Ui_LicenseWindow(object):
    def proceed(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Install_Window.Ui_InstallWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        self.license_window.close()

    def __init__(self):
        self.gpl = self.get_license()

    def setupUi(self, LicenseWindow):
        LicenseWindow.setObjectName("LicenseWindow")
        LicenseWindow.resize(800, 600)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        LicenseWindow.setFont(font)
        LicenseWindow.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                    "color: rgb(255, 255, 255);\n")
        self.license_window = LicenseWindow
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.license_window.setWindowIcon(QtGui.QIcon(
            scriptDir + os.path.sep + 'locked.ico'))

        self.central_widget = QtWidgets.QWidget(LicenseWindow)
        self.central_widget.setObjectName("central_widget")
        self.gridLayout = QtWidgets.QGridLayout(self.central_widget)
        self.gridLayout.setObjectName("gridLayout")

        self.decline_button = QtWidgets.QPushButton(self.central_widget)
        self.decline_button.setStyleSheet("color: rgb(255, 255, 255);\n"
                                          "background-color: rgb(79, 79, 79);")
        self.decline_button.setObjectName("decline_button")
        self.decline_button.clicked.connect(self.decline)

        self.gridLayout.addWidget(self.decline_button, 1, 1, 1, 1)
        self.accept_button = QtWidgets.QPushButton(self.central_widget)
        self.accept_button.setStyleSheet("color: rgb(255, 255, 255);\n"
                                         "background-color: rgb(79, 79, 79);")
        self.accept_button.setObjectName("accept_button")
        self.accept_button.clicked.connect(self.proceed)

        self.gridLayout.addWidget(self.accept_button, 1, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)

        self.listWidget = QtWidgets.QListWidget(self.central_widget)
        self.listWidget.setObjectName("listWidget")

        self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 4)

        LicenseWindow.setCentralWidget(self.central_widget)
        self.show_license()
        self.listWidget.setItemAlignment(QtCore.Qt.AlignCenter)

        self.retranslateUi(LicenseWindow)
        QtCore.QMetaObject.connectSlotsByName(LicenseWindow)

    def retranslateUi(self, LicenseWindow):
        _translate = QtCore.QCoreApplication.translate
        LicenseWindow.setWindowTitle(_translate("LicenseWindow", "MainWindow"))
        self.decline_button.setText(_translate("LicenseWindow", "Decline"))
        self.accept_button.setText(_translate("LicenseWindow", "Accept"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        self.listWidget.setSortingEnabled(__sortingEnabled)


    def decline(self):
        self.license_window.close()

    def get_license(self):
        try:
            with open("LICENSE.txt", "r") as file:
                my_license = file.readlines()
            return my_license
        except FileNotFoundError:
            return ["License Missing"]

    def show_license(self):
        for line in self.gpl:
            item = QtWidgets.QListWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
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
    sys.exit(app.exec_())
