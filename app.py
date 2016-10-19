import sys
from main_window_qt import *
from source import *
from database import *
from tag import *
from app_window_1 import *



data = database.Database('C:\Users\OmarAli\Google Drive\Research'
                            '\Research Database Builder\\research-database-builder\\test-database')
s1 = source.Source("American Demographic Data",
                   'C:\Users\OmarAli\Google Drive\Research\Research '
                   'Database Builder\research-database-builder\test-database\1')
s2 = source.Source("Artificial Intelligence Lecture",
                   'C:\Users\OmarAli\Google Drive\Research\Research Database '
                   'Builder\research-database-builder\test-database\2')
s3 = source.Source("Lives Without Imagery",
                   'C:\Users\OmarAli\Google Drive\Research\Research Database '
                   'Builder\research-database-builder\test-database\2')
t1 = tag.Tag("Demographics")
t2 = tag.Tag("Artificial Intelligence")
t3 = tag.Tag("Aphantasia")

s1.addTag(t1)
s2.addTag(t2)
s3.addTag(t3)

t1.addSource(s1)
t2.addSource(s2)
t3.addSource(s3)

data.addTag(t1)
data.addTag(t2)
data.addTag(t3)

data.addSource(s1)
data.addSource(s2)
data.addSource(s3)


for item in os.walk(a):
    print item


app = QApplication(sys.argv)
form = MainAppWindow()
form.show()
app.exec_()