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
        self.setGeometry( 0, 0, 1024, 620 )
        self.setWindowTitle( 'Board Computer' )
        self.setStyleSheet( "background-color:#ccc;" )
        self.availableSpace =  8 * self.width() / 8
        self.margin = self.width() / 8
        self.addGraphs()
        self.addTextLabels()
        self.show()

        if self.isDebug is not True:
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
        pLayout.addWidget( scroll )
        #pLayout.setMargin( 70 )


        button = qt.QPushButton( "PlayList" )
        button.setFixedHeight( 50 )
        pLayout.addWidget( button )
        button.clicked.connect( self.showPlayList )

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
            self.RPMplot.setData( self.RPMData )

        self.RPMplot.setData( self.RPMData )


        ### if len( self.SPEEDData ) < 120:
        ###    self.SPEEDData.append( self.data['speed'])
        ### else:
        ###     self.SPEEDAxisMover += 1
        ###     self.SPEEDData[:-1] = self.SPEEDData[1:]
        ###     self.SPEEDData[-1] = self.data['speed']
        ###     self.SPEEDplot.setPos( self.SPEEDAxisMover, 0 )
        ###     self.SPEEDplot.setData( self.SPEEDData )
        ###     self.SPEEDplot.setData( self.SPEEDData )

        ### self.SPEEDplot.setData( self.SPEEDData )

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

        #self.drawCircle( paint,  self.margin + self.availableSpace / 3, self.height() / 2, 325, 325 )
        #self.drawCircle( paint,  self.margin + 2 * self.availableSpace / 3 + 100, self.height() / 2, 325, 325 )

        paint.end()



    def drawCircle( self, paint, xCenter, yCenter, xRad, yRad, color = qt.QColor( 255, 255, 255 ) ):
        paint.setBrush( qt.QBrush( color ) )
        paint.drawEllipse( xCenter - xRad / 2 , yCenter - yRad / 2, xRad, yRad )



    def addGraphs( self ):
        self.RPMplot = pg.PlotWidget( self )
        self.RPMplot.resize( 900, 120 )
        self.RPMplot.move( 62, self.height() / 3  + 300 )
        self.RPMplot.hideAxis( 'left' )
        self.RPMplot.hideAxis( 'bottom' )
        self.RPMplot = self.RPMplot.plot( self.RPMData, fillLevel = 1, brush = ( 50, 50, 200, 255 ) )

        ### self.SPEEDplot = pg.PlotWidget( self )
        ### self.SPEEDplot.resize( 250, 120 )
        ### self.SPEEDplot.move( self.margin + 2 * self.availableSpace / 3 - 25 , self.height() / 3 + 270 )
        ### self.SPEEDplot.hideAxis( 'left' )
        ### self.SPEEDplot.hideAxis( 'bottom' )
        ### self.SPEEDplot = self.SPEEDplot.plot( self.SPEEDData, fillLevel = 1, brush = ( 50, 50, 200, 255 ) )



    def addTextLabels( self ):
        fontNumber = qt.QFont( "Arial", 45, qt.QFont.Bold )
        fontUnit = qt.QFont( "Arial", 25, qt.QFont.Bold )

        smallFontNumber = qt.QFont( "Arial", 25, qt.QFont.Bold )
        smallFontUnit = qt.QFont( "Arial", 18, qt.QFont.Bold )

        self.rpmText = qt.QLabel( "1900", self )
        self.rpmText.setFont( fontNumber )
        self.rpmText.setAlignment( qtc.Qt.AlignCenter )
        self.rpmText.resize( 200, 80 )
        self.rpmText.move( 50, self.height() / 3 - 180 )
        #self.rpmText.setStyleSheet( "color:#000;" )
        self.rpmText.setStyleSheet( "background-color:rgba(0,0,0,0%);" )

        rpmUnit = qt.QLabel( "RPM", self )
        rpmUnit.setFont( fontUnit )
        rpmUnit.setAlignment( qtc.Qt.AlignCenter )
        rpmUnit.resize( 200, 30 )
        rpmUnit.move( self.margin - 80, self.height() / 3 - 108 )
        rpmUnit.setStyleSheet( "background-color:rgba(0,0,0,0%);" )

        self.speedText = qt.QLabel( "100", self )
        self.speedText.setFont( fontNumber )
        self.speedText.setAlignment( qtc.Qt.AlignCenter )
        self.speedText.resize( 200, 80 )
        self.speedText.move( self.margin/2 + 2 * self.availableSpace / 3 + 0, self.height() / 3 - 180 )
        self.speedText.setStyleSheet( "color:#000;" )

        speedUnit = qt.QLabel( "km/h", self )
        speedUnit.setFont( fontUnit )
        speedUnit.setAlignment( qtc.Qt.AlignCenter )
        speedUnit.resize( 200, 30 )
        speedUnit.move( self.margin/2 + 2 * self.availableSpace / 3 + 0, self.height() / 3 - 108 )
        speedUnit.setStyleSheet( "color:#000;" )

        self.usageText = qt.QLabel( "1900 L/h", self )
        self.usageText.setFont( smallFontNumber )
        self.usageText.setAlignment( qtc.Qt.AlignCenter )
        self.usageText.resize( 200, 80 )
        self.usageText.move( self.availableSpace/2-50, self.height()/3-180 )
        self.usageText.setStyleSheet( "color:#000;" )

        usageUnit = qt.QLabel( "Usage", self )
        usageUnit.setFont( smallFontUnit )
        usageUnit.setAlignment( qtc.Qt.AlignCenter )
        usageUnit.resize( 200, 30 )
        usageUnit.move( self.availableSpace / 2 - 50, self.height() / 3 - 128 )
        usageUnit.setStyleSheet( "color:#000;" )


        ### self.mileageText = qt.QLabel( "1900 km", self )
        ### self.mileageText.setFont( smallFontNumber )
        ### self.mileageText.setAlignment( qtc.Qt.AlignCenter )
        ### self.mileageText.resize( 200, 80 )
        ### self.mileageText.move( self.margin / 2, self.height() / 3 - 180 )
        ### self.mileageText.setStyleSheet( "color:#000;" )


        ### mileageUnit = qt.QLabel( "Mileage", self )
        ### mileageUnit.setFont( smallFontUnit )
        ### mileageUnit.setAlignment( qtc.Qt.AlignCenter )
        ### mileageUnit.resize( 200, 30 )
        ### mileageUnit.move( self.margin / 2, self.height() / 3 - 128 )
        ### mileageUnit.setStyleSheet( "color:#000;" )
        
        
        ### self.gasText = qt.QLabel( "1900 L", self )
        ### self.gasText.setFont( smallFontNumber )
        ### self.gasText.setAlignment( qtc.Qt.AlignCenter )
        ### self.gasText.resize( 200, 80 )
        ### self.gasText.move( self.margin / 2, 2 * self.height() / 3 - 180 )
        ### self.gasText.setStyleSheet( "color:#000;" )

        ### gasUnit = qt.QLabel( "Tank", self )
        ### gasUnit.setFont( smallFontUnit )
        ### gasUnit.setAlignment( qtc.Qt.AlignCenter )
        ### gasUnit.resize( 200, 30 )
        ### gasUnit.move( self.margin / 2, 2 * self.height() / 3 - 128 )
        ### gasUnit.setStyleSheet( "color:#000;" )





def main():
    pg.setConfigOption( 'background', ( 204, 204, 204 ) )

    data = { 'speed' : 125.0, 'rpm' : 2000.0, 'gas' : 20, 'km' : 3300, 'usage' : 3.5, 'mileage': 10, 'time' : "12:12" }
    app = qt.QApplication( [] )
    w = GUI( data )
    sys.exit( app.exec_() )



if __name__ == '__main__':
    main()
