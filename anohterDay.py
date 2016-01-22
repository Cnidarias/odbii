import sys
from PyQt4 import QtGui, QtCore, QtWebKit


class QCustomWebView( QtWebKit.QWebView ):
    def __init__( self, parent = None ):
        super( QCustomWebView, self ).__init__( parent )
        self.load( QtCore.QUrl( 'http://localhost:6680/spotmop' ) )
        self.settings().setAttribute( QtWebKit.QWebSettings.JavascriptEnabled, True )


def main():
    app = QtGui.QApplication( [] )
    customView = QCustomWebView()
    customView.resize( 1024, 600 )
    #customView.showFullScreen()
    customView.show()
    sys.exit( app.exec_() )


if __name__ == '__main__':
    main()

