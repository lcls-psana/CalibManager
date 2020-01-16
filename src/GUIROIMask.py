#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#   GUIROIMask...
#------------------------------------------------------------------------

"""GUI for CalibManager.

This software was developed for the SIT project.  If you use all or 
part of it, please give an appropriate acknowledgment.

@version $Id$

@author Mikhail S. Dubrovin
"""
from __future__ import absolute_import

#--------------------------------
__version__ = "$Revision$"
#--------------------------------

import os
import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets

#-----------------------------
# Imports for other modules --
#-----------------------------

#from CalibManager.Frame   import Frame
from CalibManager.Logger  import logger
from .GUIMaskEditor        import *

#------------------------------
#class GUIROIMask(Frame) : 
class GUIROIMask(QtWidgets.QWidget) :
    """QWidger wrapping ROI mask processing.
    """

    def __init__(self, parent=None, app=None) :

        self.name = 'GUIROIMask'
        QtWidgets.QWidget.__init__(self, parent)
        #Frame.__init__(self, parent, mlw=1)

        self.setGeometry(10, 25, 800, 300)
        self.setWindowTitle('ROI Mask')

        self.win = GUIMaskEditor(self)
        #self.lab_status = QtGui.QLabel('Status: ')

        self.vbox = QtWidgets.QVBoxLayout() 
        self.vbox.addWidget(self.win)
        self.vbox.addStretch(1)
        #self.vbox.addWidget(self.lab_status)

        self.hbox = QtWidgets.QHBoxLayout() 
        self.hbox.addStretch(1)
        self.hbox.addLayout(self.vbox)
        self.hbox.addStretch(1)

        self.setLayout(self.hbox)
        
        self.showToolTips()
        self.setStyle()

        #self.setStatus(0)
        cp.guiroimask = self
        self.move(10,25)
        
        #print 'End of init'
        

    def showToolTips(self):
        pass
        #self.setToolTip('ROI mask wrapping widget') 


    def setStyle(self):
        self.setMinimumSize(800,300)
        #self.setMaximumWidth(800)


#    def resizeEvent(self, e):
#        pass


#    def moveEvent(self, e):
#        pass


    def closeEvent(self, event):
        logger.debug('closeEvent', self.name)

        try    : cp.maskeditor.close()
        except : pass

        cp.guiroimask = None


#    def onExit(self):
#        logger.debug('onExit', self.name)
#        self.close()


#    def setStatus(self, status_index=0, msg='Waiting for the next command'):
#        list_of_states = ['Good','Warning','Alarm']
#        if status_index == 0 : self.lab_status.setStyleSheet(cp.styleStatusGood)
#        if status_index == 1 : self.lab_status.setStyleSheet(cp.styleStatusWarning)
#        if status_index == 2 : self.lab_status.setStyleSheet(cp.styleStatusAlarm)
#        #self.lab_status.setText('Status: ' + list_of_states[status_index] + msg)
#        self.lab_status.setText(msg)

#------------------------------

if __name__ == "__main__" :
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ex  = GUIROIMask()
    ex.show()
    app.exec_()

#------------------------------
