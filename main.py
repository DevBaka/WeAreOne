import sys
import os
from PyQt5.QtWidgets import *
from mainWindow import WeAreOne , platform
import platform

platform = platform.system()
print platform

class Mainscreen(QMainWindow):
    def __init__(self):
        super(Mainscreen, self).__init__()
        self.ui = WeAreOne()
        self.ui.setupUi(self)

app = QApplication(sys.argv)
myapp = Mainscreen()
myapp.show()
print("it works!")

sys.exit(app.exec_())