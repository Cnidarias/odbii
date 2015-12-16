import sys, os
from PyQt4 import QtGui
from PyQt4 import QtCore

app = QtGui.QApplication(sys.argv)    
win = QtGui.QWidget()
win.resize(800, 600)

container = QtGui.QX11EmbedContainer(win)
container.setGeometry( 0, 0, 800, 600 )
container.show()
winId = container.winId()
process = QtCore.QProcess(container)
os.environ['NAVIT_XID'] = str( winId )
#options = ["--socketid", str(winId)]
process.startDetached("navit")

win.show()    
sys.exit(app.exec_())
