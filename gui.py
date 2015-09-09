import os
import sys
import time
import random

import subprocess

from PyQt4 import QtGui as qt
from PyQt4 import QtCore as qtc
import pyqtgraph as pg


from client import tester
import kw1281Audi


class GUI( qt.QWidget ):
    def __init__( self, data ):
        super( GUI, self ).__init__()

        self.data = data

        self.task = kw1281Audi.kw1281( data )
        self.task.daemon = True
        # self.task.start()

        self.RPMplot = None
        self.RPMData = []
        self.RPMtext = None
        self.RPMAxisMover = 0

        self.SPEEDplot = None
        self.SPEEDtext = None
        self.SPEEDData = []
        self.SPEEDAxisMover = 0
        self.timeCounter = 0;

        self.GAStext = None
        self.MILEAGEtext = None
        self.USAGEtext = None

        self.initUI()



    def initUI( self ):
        self.setGeometry( 0, 0, 1024, 620 )
        self.setWindowTitle( 'Board Computer' )
        self.setStyleSheet( "background-color:#ccc;" )
        self.availableSpace =  7 * self.width() / 8
        self.margin = self.width() / 8
        self.addGraphs()
        self.addTextLabels()
        self.show()

        ### self.showFullScreen() ###
        self.timer = qtc.QTimer( self )
        self.timer.setInterval( 200 )
        self.timer.timeout.connect( self.custUpdate )
        self.timer.start()



    def custUpdate( self ):

        self.RPMtext.setText( str( int( self.data['rpm'] ) ) )
        self.SPEEDtext.setText( str( self.data['speed'] ) )

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


        if len( self.SPEEDData ) < 120:
           self.SPEEDData.append( self.data['speed'])
        else:
            self.SPEEDAxisMover += 1
            self.SPEEDData[:-1] = self.SPEEDData[1:]
            self.SPEEDData[-1] = self.data['speed']
            self.SPEEDplot.setPos( self.SPEEDAxisMover, 0 )
            self.SPEEDplot.setData( self.SPEEDData )
            self.SPEEDplot.setData( self.SPEEDData )

        self.SPEEDplot.setData( self.SPEEDData )

        # if self.task.isAlive() is not True:
        #     time.sleep( 1 )
        #     self.task = kw1281Audi.kw1281( self.data )
        #     self.task.daemon = True
        #     self.task.run()




    def paintEvent( self, e ):
        paint = qt.QPainter()
        paint.begin( self )
        paint.setRenderHint( qt.QPainter.Antialiasing )

        self.drawCircle( paint,  self.margin + self.availableSpace / 3, self.height() / 2, 325, 325 )
        self.drawCircle( paint,  self.margin + 2 * self.availableSpace / 3 + 100, self.height() / 2, 325, 325 )

        paint.end()



    def drawCircle( self, paint, xCenter, yCenter, xRad, yRad, color = qt.QColor( 255, 255, 255 ) ):
        paint.setBrush( qt.QBrush( color ) )
        paint.drawEllipse( xCenter - xRad / 2 , yCenter - yRad / 2, xRad, yRad )



    def addGraphs( self ):
        self.RPMplot = pg.PlotWidget( self )
        self.RPMplot.resize( 250, 120 )
        self.RPMplot.move( self.margin + self.availableSpace / 3 - 125 , self.height() / 3  + 270 )
        self.RPMplot.hideAxis( 'left' )
        self.RPMplot.hideAxis( 'bottom' )
        self.RPMplot = self.RPMplot.plot( self.RPMData, fillLevel = 1, brush = ( 50, 50, 200, 255 ) )

        self.SPEEDplot = pg.PlotWidget( self )
        self.SPEEDplot.resize( 250, 120 )
        self.SPEEDplot.move( self.margin + 2 * self.availableSpace / 3 - 25 , self.height() / 3 + 270 )
        self.SPEEDplot.hideAxis( 'left' )
        self.SPEEDplot.hideAxis( 'bottom' )
        self.SPEEDplot = self.SPEEDplot.plot( self.SPEEDData, fillLevel = 1, brush = ( 50, 50, 200, 255 ) )



    def addTextLabels( self ):
        fontNumber = qt.QFont( "Arial", 45, qt.QFont.Bold )
        fontUnit = qt.QFont( "Arial", 25, qt.QFont.Bold )

        smallFontNumber = qt.QFont( "Arial", 25, qt.QFont.Bold )
        smallFontUnit = qt.QFont( "Arial", 18, qt.QFont.Bold )

        self.RPMtext = qt.QLabel( "1900", self )
        self.RPMtext.setFont( fontNumber )
        self.RPMtext.setAlignment( qtc.Qt.AlignCenter )
        self.RPMtext.resize( 200, 80 )
        self.RPMtext.move( self.margin + self.availableSpace / 3 - 100, self.height() / 3 - 180 )
        self.RPMtext.setStyleSheet( "color:#000;" )

        RPMUnit = qt.QLabel( "RPM", self )
        RPMUnit.setFont( fontUnit )
        RPMUnit.setAlignment( qtc.Qt.AlignCenter )
        RPMUnit.resize( 200, 30 )
        RPMUnit.move( self.margin + self.availableSpace / 3 - 100, self.height() / 3 - 108 )
        RPMUnit.setStyleSheet( "color:#000;" )

        self.SPEEDtext = qt.QLabel( "100", self )
        self.SPEEDtext.setFont( fontNumber )
        self.SPEEDtext.setAlignment( qtc.Qt.AlignCenter )
        self.SPEEDtext.resize( 200, 80 )
        self.SPEEDtext.move( self.margin + 2 * self.availableSpace / 3 + 0, self.height() / 3 - 180 )
        self.SPEEDtext.setStyleSheet( "color:#000;" )

        SPEEDUnit = qt.QLabel( "km/h", self )
        SPEEDUnit.setFont( fontUnit )
        SPEEDUnit.setAlignment( qtc.Qt.AlignCenter )
        SPEEDUnit.resize( 200, 30 )
        SPEEDUnit.move( self.margin + 2 * self.availableSpace / 3 + 0, self.height() / 3 - 108 )
        SPEEDUnit.setStyleSheet( "color:#000;" )

        #RX 22 00 C0 02 36




        self.MILEAGEtext = qt.QLabel( "1900 km", self )
        self.MILEAGEtext.setFont( smallFontNumber )
        self.MILEAGEtext.setAlignment( qtc.Qt.AlignCenter )
        self.MILEAGEtext.resize( 200, 80 )
        self.MILEAGEtext.move( self.margin / 2, self.height() / 3 - 180 )
        self.MILEAGEtext.setStyleSheet( "color:#000;" )


        MILEAGEUnit = qt.QLabel( "Mileage", self )
        MILEAGEUnit.setFont( smallFontUnit )
        MILEAGEUnit.setAlignment( qtc.Qt.AlignCenter )
        MILEAGEUnit.resize( 200, 30 )
        MILEAGEUnit.move( self.margin / 2, self.height() / 3 - 128 )
        MILEAGEUnit.setStyleSheet( "color:#000;" )
        
        self.USAGEtext = qt.QLabel( "1900 L/h", self )
        self.USAGEtext.setFont( smallFontNumber )
        self.USAGEtext.setAlignment( qtc.Qt.AlignCenter )
        self.USAGEtext.resize( 200, 80 )
        self.USAGEtext.move( self.margin / 2, self.height() / 2 - 180 )
        self.USAGEtext.setStyleSheet( "color:#000;" )

        USAGEUnit = qt.QLabel( "Usage", self )
        USAGEUnit.setFont( smallFontUnit )
        USAGEUnit.setAlignment( qtc.Qt.AlignCenter )
        USAGEUnit.resize( 200, 30 )
        USAGEUnit.move( self.margin / 2, self.height() / 2 - 128 )
        USAGEUnit.setStyleSheet( "color:#000;" )
        
        self.GasText = qt.QLabel( "1900 L", self )
        self.GasText.setFont( smallFontNumber )
        self.GasText.setAlignment( qtc.Qt.AlignCenter )
        self.GasText.resize( 200, 80 )
        self.GasText.move( self.margin / 2, 2 * self.height() / 3 - 180 )
        self.GasText.setStyleSheet( "color:#000;" )

        GasUnit = qt.QLabel( "Tank", self )
        GasUnit.setFont( smallFontUnit )
        GasUnit.setAlignment( qtc.Qt.AlignCenter )
        GasUnit.resize( 200, 30 )
        GasUnit.move( self.margin / 2, 2 * self.height() / 3 - 128 )
        GasUnit.setStyleSheet( "color:#000;" )





def main():
    pg.setConfigOption( 'background', ( 204, 204, 204 ) )

    data = { 'speed' : 125.0, 'rpm' : 2000.0, 'gas' : 20, 'km' : 3300, 'usage' : 3.5 }
    app = qt.QApplication( [] )
    w = GUI( data )
    sys.exit( app.exec_() )



if __name__ == '__main__':
    main()
