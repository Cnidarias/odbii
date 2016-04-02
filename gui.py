import os
import sys
import time
import random

import subprocess

from PyQt4 import QtGui as qt
from PyQt4 import QtCore as qtc

import pyqtgraph as pg


from client import tester
from extendedQLabel import *
import kw1281Audi
import spotifyPython


class GUI( qt.QWidget ):
    def __init__( self, data ):
        super( GUI, self ).__init__()

        self.data = data

        self.isDebug = True
        self.isFullScreenDebug = False

        self.task = kw1281Audi.kw1281( data )
        self.task.daemon = True
        if self.isDebug is not True:
          self.task.start()

        self.spotify = spotifyPython.Commander( False )
        self.spotify.do_relogin()

        self.RPMplot = None
        self.RPMData = []
        self.rpmText = None
        self.RPMAxisMover = 0

        self.SPEEDplot = None
        self.speedText = None
        self.SPEEDData = []
        self.SPEEDAxisMover = 0
        self.timeCounter = 0;

        self.GAStext = None
        self.mileageText = None
        self.usageText = None



        self.initUI()



    def initUI( self ):
        self.setGeometry( 0, 0, 840, 480 )
        self.setWindowTitle( 'Board Computer' )
        self.setStyleSheet( "background-color:#ccc;" )
        self.availableSpace =  8 * self.width() / 8
        self.margin = self.width() / 8
        self.addGraphs()
        self.addTextLabels()
        self.show()

        if self.isFullScreenDebug is  True:
          self.showFullScreen() 
        self.timer = qtc.QTimer( self )
        self.timer.setInterval( 200 )
        self.timer.timeout.connect( self.custUpdate )
        self.timer.start()
        #self.initNavit()
        self.initSpotify()



    def initNavit( self ):
        container = qt.QX11EmbedContainer( self )
        container.setGeometry( 112, 20, 800, 480 )
        container.show()
        winId = container.winId()
        process = qtc.QProcess(container)
        os.environ['NAVIT_XID'] = str( winId )
        process.startDetached("navit")



    def initSpotify( self ):
        playLists = self.spotify.do_get_Playlist()

        self.spotifyContainer = qt.QWidget()
        self.spotifyContainer.show()
        
        self.spotifyLayout = qt.QFormLayout()
        fontUnit = qt.QFont( "Arial", 35, qt.QFont.Bold )

        for ele in playLists:
            widget = ExtendedQLabel( self.spotifyContainer )
            widget.setText( ele[1] )
            widget.setData( ele[0] )
            widget.setFont( fontUnit )
            self.connect( widget, SIGNAL('clicked( QObject )'), self.playListClicked )
            self.spotifyLayout.addRow( widget )
            
        self.spotifyContainer.setLayout( self.spotifyLayout )
        scroll = qt.QScrollArea()
        scroll.setWidget( self.spotifyContainer )
        scroll.setWidgetResizable( True )
        scroll.setFixedHeight( 280 )
        scroll.setWidget( self.spotifyContainer )

        scroll.verticalScrollBar().setFixedWidth( 30 )

        pLayout = qt.QVBoxLayout( self )
        pLayout.setSpacing( 1 )
        pLayout.setAlignment( qtc.Qt.AlignCenter )
        pLayout.setContentsMargins( 70, 0, 70, 0 )
        #pLayout.addWidget( scroll )
        #pLayout.setMargin( 70 )



        nextButton = qt.QPushButton( "Next", self )
        nextButton.setFixedHeight( 50 )
        nextButton.clicked.connect( self.nextSpotify )
        nextButton.resize( 100, 50 )
        nextButton.move( 34, 140 )
        nextButton.show();


        playButton = qt.QPushButton( "Play", self )
        playButton.setFixedHeight( 50 )
        playButton.clicked.connect( self.playSpotify )
        playButton.resize( 100, 50 )
        playButton.move( 34, 230 )
        playButton.show();

        prevButton = qt.QPushButton( "Prev", self )
        prevButton.setFixedHeight( 50 )
        prevButton.clicked.connect( self.prevSpotify )
        prevButton.resize( 100, 50 )
        prevButton.move( 34, 320 )
        prevButton.show();

        playListButton = qt.QPushButton( "Playlist", self )
        playListButton.setFixedHeight( 50 )
        playListButton.clicked.connect( self.showPlayList )
        playListButton.resize( 100, 50 )
        playListButton.move( 34, 410 )
        playListButton.show();





        testLine2 = qt.QFrame( self )
        testLine2.setFrameShape( qt.QFrame.VLine )
        testLine2.setFrameShadow( qt.QFrame.Sunken )

        testLine2.move( self.width()/5 * 4, 0 )
        testLine2.resize( 1, self.height() )
        testLine2.show()

        testLine = qt.QFrame( self )
        testLine.setFrameShape( qt.QFrame.VLine )
        testLine.setFrameShadow( qt.QFrame.Sunken )

        testLine.move( self.width()/5 * 1, 0 )
        testLine.resize( 1, self.height() )
        testLine.show()


        

    def nextSpotify( self ):
        return



    def prevSpotify( self ):
        return



    def playSpotify( self ):
        return

    def showPlayList( self ):
        playLists = self.spotify.do_get_Playlist()
        for i in reversed( range( self.spotifyLayout.count() ) ):
            self.spotifyLayout.itemAt( i ).widget().setParent( None )

        fontUnit = qt.QFont( "Arial", 35, qt.QFont.Bold )

        for ele in playLists:
            widget = ExtendedQLabel( self.spotifyContainer )
            widget.setText( ele[1] )
            widget.setData( ele[0] )
            widget.setFont( fontUnit )
            self.connect( widget, SIGNAL('clicked( QObject )'), self.playListClicked )
            self.spotifyLayout.addRow( widget )
        


    def playListClicked( self, element):
        tracks = self.spotify.do_play_playlist( str(element.getData() ) )
        fontUnit = qt.QFont( "Arial", 15, qt.QFont.Bold )
        print "Label Clicked"
        for i in reversed( range( self.spotifyLayout.count() ) ):
            self.spotifyLayout.itemAt( i ).widget().setParent( None )

        for ele in tracks:
            boxLayout = qt.QHBoxLayout()
            widget = ExtendedQLabel( self.spotifyContainer )
            if ele[1] is not None:
                widget.setText( ele[1] )
            widget.setData( ele[0] )
            widget.setFont( fontUnit )

            widget2 = ExtendedQLabel( self.spotifyContainer )
            if ele[2] is not None:
                widget2.setText( self.milliSecondsToMin( ele[2] ) )
            widget2.setFont( fontUnit )
            widget2.setAlignment( qtc.Qt.AlignCenter )

            widget3 = ExtendedQLabel( self.spotifyContainer )
            if ele[3] is not None:
                widget3.setText( ele[3] )
            widget3.setFont( fontUnit )

            boxLayout.addWidget( widget2 )
            boxLayout.addWidget( widget3 )

            cont = qt.QWidget()
            cont.setLayout( boxLayout )

            self.spotifyLayout.addRow( widget, cont )



    def custUpdate( self ):
        self.data['rpm'] += 1
        self.rpmText.setText( str( int( self.data['rpm'] ) ) )
        self.speedText.setText( str( self.data['speed'] ) )
        self.usageText.setText( str( self.data['usage'] ) )

        if len( self.RPMData ) < 120:
            self.RPMData.append( self.data['rpm'])
        else:
            self.RPMAxisMover += 1
            self.RPMData[:-1] = self.RPMData[1:]
            self.RPMData[-1] = self.data['rpm']
            self.RPMplot.setPos( self.RPMAxisMover, 0 )

        self.RPMplot.setData( self.RPMData )

       
        if self.task.isAlive() is not True and self.isDebug is not True:
            self.task = kw1281Audi.kw1281( self.data )
            self.task.daemon = True
            self.task.start()



    def milliSecondsToMin( self, millis ):
        s = millis / 1000 
        m,s = divmod( s, 60 )
        
        if s < 10:
            s = "0" + str( s )
        return str(m)+":"+str(s)



    def paintEvent( self, e ):
        paint = qt.QPainter()
        paint.begin( self )
        paint.setRenderHint( qt.QPainter.Antialiasing )
        paint.end()



    def drawCircle( self, paint, xCenter, yCenter, xRad, yRad, color = qt.QColor( 255, 255, 255 ) ):
        paint.setBrush( qt.QBrush( color ) )
        paint.drawEllipse( xCenter - xRad / 2 , yCenter - yRad / 2, xRad, yRad )



    def addGraphs( self ):
        self.RPMplot = pg.PlotWidget( self )
        self.RPMplot.resize( self.width(), self.height() / 4 )
        self.RPMplot.move( -10, 0 )
        self.RPMplot.hideAxis( 'left' )
        self.RPMplot.hideAxis( 'bottom' )
        self.RPMplot = self.RPMplot.plot( self.RPMData, fillLevel = 1, brush = ( 50, 50, 200, 155 ) )



    def addTextLabels( self ):
        topRowParent = qt.QWidget()

        fontNumber = qt.QFont( "Arial", 40, qt.QFont.Bold )
        fontUnit = qt.QFont( "Arial", 15, qt.QFont.Bold )

        smallFontNumber = qt.QFont( "Arial", 25, qt.QFont.Bold )
        smallFontUnit = qt.QFont( "Arial", 18, qt.QFont.Bold )

        self.rpmText = qt.QLabel( "1900", self )
        self.rpmText.setFont( fontNumber )
        self.rpmText.setAlignment( qtc.Qt.AlignCenter )
        self.rpmText.resize( 200, 80 )
        self.rpmText.move( 40, 6 )
        self.rpmText.setStyleSheet( "color:#000;background-color:rgba(0,0,0,0%);" )

        rpmUnit = qt.QLabel( "RPM", self )
        rpmUnit.setFont( fontUnit )
        rpmUnit.setAlignment( qtc.Qt.AlignCenter )
        rpmUnit.resize( 200, 30 )
        rpmUnit.move( 40, 60 )
        rpmUnit.setStyleSheet( "color:#000;background-color:rgba(0,0,0,0%);" )

        self.speedText = qt.QLabel( "100", self )
        self.speedText.setFont( fontNumber )
        self.speedText.setAlignment( qtc.Qt.AlignCenter )
        self.speedText.resize( 200, 80 )
        self.speedText.move( 600, 6 )
        self.speedText.setStyleSheet( "color:#000;background-color:rgba(0,0,0,0%);" )

        speedUnit = qt.QLabel( "km/h", self )
        speedUnit.setFont( fontUnit )
        speedUnit.setAlignment( qtc.Qt.AlignCenter )
        speedUnit.resize( 200, 30 )
        speedUnit.move( 600, 60 )
        speedUnit.setStyleSheet( "color:#000;;background-color:rgba(0,0,0,0%);" )

        self.usageText = qt.QLabel( "1900 L/h", self )
        self.usageText.setFont( fontNumber )
        self.usageText.setAlignment( qtc.Qt.AlignCenter )
        self.usageText.resize( 200, 80 )
        self.usageText.move( 320, 6 )
        self.usageText.setStyleSheet( "color:#000;;background-color:rgba(0,0,0,0%);" )

        usageUnit = qt.QLabel( "L/h", self )
        usageUnit.setFont( fontUnit )
        usageUnit.setAlignment( qtc.Qt.AlignCenter )
        usageUnit.resize( 200, 30 )
        usageUnit.move( 320, 60 )
        usageUnit.setStyleSheet( "color:#000;;background-color:rgba(0,0,0,0%);" )


def main():
    pg.setConfigOption( 'background', ( 204, 204, 204 ) )

    data = { 'speed' : 125.0, 'rpm' : 2000.0, 'gas' : 20, 'km' : 3300, 'usage' : 3.5, 'mileage': 10, 'time' : "12:12" }
    app = qt.QApplication( [] )
    w = GUI( data )
    sys.exit( app.exec_() )



if __name__ == '__main__':
    main()
