#!/usr/bin/env python
from __future__ import division

"""
    Class for plot management
    
    == Currently under development ======================================
    
    Copyright (C) 2015
    Arthur Fages - Loic Fagot - Vincent Labourdette - Thomas Lamant - Guillaume Loizeau
    Arts et Metiers ParisTech, centre de Bordeaux-Talence
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# Version 0.4
# Last update : 13/05/2015

import pyqtgraph as pg
import numpy as np

import sys

from PyQt4 import QtGui
from PyQt4 import Qt
from PyQt4 import QtCore
from PyQt4 import Qwt5 as Qwt

class Plot(Qwt.QwtPlot):
    """ Plot allowing to diplay data """
    
    def __init__(self, dataToDisplay, rate, *args):
        
        # record signal
        self.dataToDisplay = dataToDisplay
        
        # currently wrote for 2 channels
        #a1 = dataToDisplay[0]
        #a2 = dataToDisplay[1]
        dt = 1./rate
        
        # signal characteristics
        self.dt     = dt
        self.ti     = np.arange(0.0, 1.0, self.dt)
        #self.a1     = a1
        #self.a2     = a2
        self.a1   = 0.0*self.ti
        self.a2   = 0.0*self.ti
        self.offset = 0
        
        # Graphic user interface
        apply(Qwt.QwtPlot.__init__, (self,) + args)
        self.setFixedSize(600,400)
#######        self.setFixedSize(0.4*width_fenetre,0.8*height_fenetre)
        
        # define grid
        self.grid = Qwt.QwtPlotGrid()
        self.grid.enableXMin(True)
        self.grid.setMajPen(Qt.QPen(Qt.Qt.gray, 0, Qt.Qt.SolidLine))
        self.grid.attach(self)
        
        # define axes
        self.enableAxis(Qwt.QwtPlot.yRight);
        self.setAxisTitle(Qwt.QwtPlot.yLeft,  'Amplitude Chan. 1 [V]');
        self.setAxisTitle(Qwt.QwtPlot.yRight, 'Amplitude Chan. 2 [V]');
          
        self.setAxisMaxMajor(Qwt.QwtPlot.xBottom, 20);
        self.setAxisMaxMinor(Qwt.QwtPlot.xBottom, 0);

        self.setAxisScaleEngine(Qwt.QwtPlot.yRight, Qwt.QwtLinearScaleEngine());
        self.setAxisScaleEngine(Qwt.QwtPlot.yLeft, Qwt.QwtLinearScaleEngine());
        self.setAxisMaxMajor(Qwt.QwtPlot.yLeft, 10);
        self.setAxisMaxMinor(Qwt.QwtPlot.yLeft, 0);
        self.setAxisMaxMajor(Qwt.QwtPlot.yRight, 10);
        self.setAxisMaxMinor(Qwt.QwtPlot.yRight, 0);
        
        # set scale
        self.setVerticalScale(0.5)
        # horizontal scale stay in autoscale
        
        # curves for scope traces
        self.curve2 = Qwt.QwtPlotCurve('Trace2')
        self.curve2.setPen(Qt.QPen(Qt.Qt.magenta,1))
        self.curve2.setYAxis(Qwt.QwtPlot.yRight)
        self.curve2.attach(self)

        self.curve1 = Qwt.QwtPlotCurve('Trace1')
        self.curve1.setPen(Qt.QPen(Qt.Qt.blue,1))
        self.curve1.setYAxis(Qwt.QwtPlot.yLeft)
        self.curve1.attach(self)
        
        # curve display initialisation
        #l = len(self.a1)
        #self.curve1.setData(self.ti, self.a1)
        #self.curve2.setData(self.ti, self.a2)
        
        # plot scope traces
        
        # signal to display
        self.a1 = dataToDisplay[0]
        self.a2 = dataToDisplay[1]
        
        # display
        l1 = len(self.a1)
        l2 = len(self.a2)
        self.curve1.setData(self.ti[0:l1], self.a1[:l1])
        self.curve2.setData(self.ti[0:l2], self.a2[:l2])
        
        # set cursor
        self.setMouseTracking(True)
        
        self.picker1 = Qwt.QwtPlotPicker(Qwt.QwtPlot.xBottom, Qwt.QwtPlot.yLeft, Qwt.QwtPicker.PointSelection | Qwt.QwtPicker.DragSelection, Qwt.QwtPlotPicker.CrossRubberBand, Qwt.QwtPicker.ActiveOnly, self.canvas())
        self.picker1.setTrackerMode(Qwt.QwtPicker.AlwaysOn)
        
        self.marker = Qwt.QwtPlotMarker()
        self.marker.setLineStyle(Qwt.QwtPlotMarker.VLine | Qwt.QwtPlotMarker.HLine)
        self.marker.setLabelAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        self.marker.setLinePen(QtGui.QPen(QtCore.Qt.darkGray, 1, QtCore.Qt.DashLine))
        self.marker.setValue(1.0, 0.0)
        self.marker.attach(self)
        
        
        
        self.replot()
        
    def mouseMoveEvent(self, e) :
        canvasPos = self.canvas().mapFrom(self, e.pos())
        x = self.invTransform(Qwt.QwtPlot.xBottom, canvasPos.x())
        y = self.invTransform(Qwt.QwtPlot.yLeft, canvasPos.y())
        self.marker.setValue(x, y)
        self.replot()
        
        
    def setOffset(self, newOffset):
        self.offset = newOffset
        
    def update(self, dataToDisplay, rate):
        
        #print "data to display [0] : "+str(dataToDisplay[0])
        #print "data to display [1] : "+str(dataToDisplay[1])
        
        # get the new values of the plotted signal
        # currently wrote for 2 channels
        self.a1 = dataToDisplay[0]
        self.a2 = dataToDisplay[1]
        self.dt = 1./rate
        self.ti = np.arange(0.0, 1.0, self.dt)
        
        #print "----------------------"
        #print dataToDisplay
        #print self.a1
        #print self.a2
        l1 = len(self.a1)
        l2 = len(self.a2)
        
        if l1 == 2 :
            # display only channel 2
            self.curve1.setData([0.0,0.0], [0.0,0.0])
            self.curve2.setData(self.ti[0:l2], self.a2[:l2])
        elif l2 == 2 :
            # display only channel 1
            self.curve1.setData(self.ti[0:l1], self.a1[:l1])
            self.curve2.setData([0.0,0.0], [0.0,0.0])
        else :
            # display channel 1 and 2
            self.curve1.setData(self.ti[0:l1], self.a1[:l1])
            self.curve2.setData(self.ti[0:l2], self.a2[:l2])

        self.replot()
        
        #print "[Oh yeah, I update]"
    
    
        
