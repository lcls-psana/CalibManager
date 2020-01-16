#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module GUIDark...
#------------------------------------------------------------------------

"""GUI works with dark runs"""
from __future__ import absolute_import

#--------------------------------
__version__ = "$Revision$"
#--------------------------------

import os

from PyQt4 import QtGui, QtCore

from .ConfigParametersForApp import cp
from CalibManager.Logger                 import logger

from .GUIStatus              import *
from .GUIDarkControlBar      import *
from .GUIDarkList            import *

#------------------------------

class GUIDark(QtGui.QWidget) :
    """GUI works with dark runs"""

    def __init__(self, parent=None) :
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(200, 400, 800, 300)
        self.setWindowTitle('Dark run processing')

        self.guistatus   = GUIStatus(self)
        self.guidarkcbar = GUIDarkControlBar(self)
        self.guidarklist = GUIDarkList(self)

        self.vbox = QtGui.QVBoxLayout() 
        self.vbox.addWidget(self.guidarkcbar)
        self.vbox.addWidget(self.guidarklist)
        self.vwidg = QtGui.QWidget(self)
        self.vwidg.setLayout(self.vbox) 

        self.vsplit = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.vsplit.addWidget(self.guistatus)
        self.vsplit.addWidget(self.vwidg)

        self.hbox = QtGui.QHBoxLayout(self) 
        self.hbox.addWidget(self.vsplit)
        #self.hbox.addStretch(1)

        self.setLayout(self.hbox)

        self.showToolTips()
        self.setStyle()

        cp.guidark = self
        self.guistatus.updateStatusInfo()


    def showToolTips(self):
        self.setToolTip('Dark run GUI')
        pass


    def setStyle(self):
        self.setContentsMargins (QtCore.QMargins(-5,-5,-5, 2))
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        #self.vsplit.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Ignored)
        #self.setMinimumSize(790,210)
        #self.setMinimumHeight(320)
        #self.vsplit.setMinimumHeight(200)
        #self.vsplit.setHandleWidth(150)
        #self.vsplit.moveSplitter(10, self.vsplit.indexOf(self.guistatus))
        #self.vsplit.moveSplitter(300, self.vsplit.indexOf(self.vwidg))
        #self.setBaseSize(750,700)
        #self.setStyleSheet(cp.styleBkgd)
        self.setContentsMargins(QtCore.QMargins(-9,-9,-9,-9))


    #def resizeEvent(self, e):
        #logger.debug('resizeEvent', self.name)
        #print 'GUIDark resizeEvent: %s' % str(self.size())
        #pass


    #def moveEvent(self, e):
        #logger.debug('moveEvent', self.name) 
        #self.position = self.mapToGlobal(self.pos())
        #self.position = self.pos()
        #logger.debug('moveEvent - pos:' + str(self.position), __name__)       
        #pass


    def closeEvent(self, event):
        logger.debug('closeEvent', __name__)

        try    : self.guistatus.close()
        except : pass

        try    : self.guidarklist.close()        
        except : pass

        try    : self.guidarkcbar.close()        
        except : pass

#-----------------------------

if __name__ == "__main__" :
    import sys
    app = QtGui.QApplication(sys.argv)
    widget = GUIDark ()
    widget.show()
    app.exec_()

#-----------------------------
