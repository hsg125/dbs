from mainWindow import *



class mainUI(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(mainUI, self).__init__(parent)
        self.setupUi(self)
        self.grand = None
        self.pushButton.clicked.connect(self.s)


    def s(self):
        print(self.grand)
