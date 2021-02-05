#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module PlotImgSpe...
#
#------------------------------------------------------------------------

"""Plots image and spectrum for 2d array.

This software was developed for the SIT project.  If you use all or 
part of it, please give an appropriate acknowledgment.

@version $Id$ 

@author Mikhail S. Dubrovin
"""
from __future__ import print_function
from __future__ import absolute_import

#--------------------------------
__version__ = "$Revision$"
#--------------------------------

import sys
import os
import random
import numpy as np

if __name__ == "__main__" :
    import matplotlib
    matplotlib.use('Qt4Agg') # forse Agg rendering to a Qt4 canvas (backend)

#if matplotlib.get_backend() != 'Qt4Agg' : matplotlib.use('Qt4Agg')
#import matplotlib.pyplot as plt
#from matplotlib.figure import Figure
from PyQt5 import QtCore, QtGui, QtWidgets
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

#-----------------------------

#import ImgSpeNavToolBar     as imgtb
from . import PlotImgSpeWidget         as imgwidg
from . import PlotImgSpeButtons        as imgbuts

from .ConfigParametersForApp import cp
from . import GlobalUtils          as     gu

#---------------------

#class PlotImgSpe(QtGui.QMainWindow) :
class PlotImgSpe(QtWidgets.QWidget) :
    """Plots image and spectrum for 2d array"""

    def __init__(self, parent=None, arr=None, ifname='', ofname='./fig.png', title='Plot 2d array', orient=0, y_is_flip=False, is_expanded=False, verb=False, fexmod=False ):
        #QtGui.QMainWindow.__init__(self, parent)
        QtWidgets.QWidget.__init__(self, parent)
        self.setGeometry(20, 40, 700, 800)
        self.setWindowTitle(title)

        if      arr is not None : self.arr = arr
        elif ifname != '' \
             and os.path.exists(ifname) : self.arr = gu.get_image_array_from_file(ifname)
        else                            : self.arr = get_array2d_for_test()

        if verb : print('     Image shape :', self.arr.shape)

        self.ext_ref = None

        self.widgimage = imgwidg.PlotImgSpeWidget(self, self.arr, orient, y_is_flip)
        self.widgbuts  = imgbuts.PlotImgSpeButtons(self, self.widgimage, ifname, ofname, None, is_expanded, fexmod, verb)
        #self.mpl_toolbar = imgtb.ImgSpeNavToolBar(self.widgimage, self)
 
        #---------------------

        vbox = QtWidgets.QVBoxLayout()                      # <=== Begin to combine layout 
        #vbox.addWidget(self.widgimage)                 # <=== Add figure as QWidget
        vbox.addWidget(self.widgimage.getCanvas())      # <=== Add figure as FigureCanvas 
        #vbox.addWidget(self.mpl_toolbar)                # <=== Add toolbar
        vbox.addWidget(self.widgbuts)                   # <=== Add buttons         
        self.setLayout(vbox)
        #self.show()
        #---------------------
        #self.main_frame = QtGui.QWidget()
        #self.main_frame.setLayout(vbox)
        #self.setCentralWidget(self.main_frame)
        #---------------------
        self.layout().setContentsMargins(0,0,0,0)
        #cp.plotimgspe = self


    def set_image_array(self,arr,title='Plot 2d array'):
        self.widgimage.set_image_array(arr)
        self.setWindowTitle(title)


    def set_image_array_new(self,arr,title='Plot 2d array', orient=0, y_is_flip=False):
        self.widgimage.set_image_array_new(arr, orient, y_is_flip)
        self.setWindowTitle(title)


    #def resizeEvent(self, e):
    #    #print 'resizeEvent' 
    #    pass


    def closeEvent(self, event): # is called for self.close() or when click on "x"

        try    : self.widgimage.close()
        except : pass

        try    : self.widgbuts.close()
        except : pass

        cp.plotimgspe = None

#-----------------------------
# Test
#-----------------------------

def get_array2d_for_test() :
    mu, sigma = 200, 25
    rows, cols = 1300, 1340
    arr = mu + sigma*np.random.standard_normal(size=rows*cols)
    #arr = 100*np.random.standard_exponential(size=2400)
    #arr = np.arange(2400)
    arr.shape = (rows,cols)
    return arr

#-----------------------------

if __name__ == "__main__" :
    app = QtWidgets.QApplication(sys.argv)
    #w = PlotImgSpe(None, get_array2d_for_test())
    w = PlotImgSpe(None, is_expanded=False)
    w.set_image_array(get_array2d_for_test())
    w.move(QtCore.QPoint(50,50))
    w.show()
    app.exec_()

#-----------------------------
