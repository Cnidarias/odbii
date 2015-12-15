import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

app = QtGui.QApplication(sys.argv)    
win = QtGui.QWidget()
win.resize(600, 800)

container = QtGui.QX11EmbedContainer(win)
container.show()
QtCore.QObject.connect(container, 
    QtCore.SIGNAL("clientClosed()"), 
    QtCore.QCoreApplication.instance().quit)
winId = container.winId()
process = QtCore.QProcess(container)
options = ["--socketid", str(winId)]
process.start("navit", options)

win.show()    
sys.exit(app.exec_())
