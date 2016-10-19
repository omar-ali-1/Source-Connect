import sys
from main_window_qt import *
from source import *
from database import *
from tag import *
from app_window_1 import *
import cPickle as pickle







app = QApplication(sys.argv)
form = MainAppWindow()
form.show()
app.exec_()