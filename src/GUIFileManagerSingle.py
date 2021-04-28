from __future__ import absolute_import
#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  GUIFileManagerSingle...
#------------------------------------------------------------------------

from PyQt5 import QtCore, QtGui, QtWidgets

from .ConfigParametersForApp import cp
from CalibManager.Logger                 import logger

from .GUIStatus                   import *
from .GUIFileManagerSingleControl import *

#------------------------------

#class GUIFileManagerSingle(Frame) :
class GUIFileManagerSingle(QtWidgets.QWidget) :
    """GUI for Single File Manager"""

    def __init__(self, parent=None) :
        QtWidgets.QWidget.__init__(self, parent)
        #Frame.__init__(self, parent, mlw=1)

        self.setGeometry(200, 400, 800, 300)
        self.setWindowTitle('Single File Manager')

        self.guistatus = GUIStatus(self)
        self.guifilemanagersinglecontrol  = GUIFileManagerSingleControl(self)
        #self.guifilemanagersinglecontrol  = QtGui.QTextEdit('Source file GUI is not implemented.') # GUIDark(self)

        self.vbox = QtWidgets.QVBoxLayout() 
        self.vbox.addWidget(self.guistatus)
        self.vbox.addWidget(self.guifilemanagersinglecontrol)
        #self.vwidg = QtGui.QWidget(self)
        #self.vwidg.setLayout(self.vbox) 

        #self.vsplit = QtGui.QSplitter(QtCore.Qt.Vertical)
        #self.vsplit.addWidget(self.guistatus)
        #self.vsplit.addWidget(self.guifilemanagersinglecontrol)

        self.hbox = QtWidgets.QHBoxLayout(self) 
        #self.hbox.addWidget(self.vsplit)
        self.hbox.addLayout(self.vbox)
        #self.hbox.addStretch(1)

        self.setLayout(self.hbox)

        self.showToolTips()
        self.setStyle()

        self.guistatus.updateStatusInfo()

        cp.guifilemanagersingle = self


    def showToolTips(self):
        self.setToolTip('Single file manager')


    def setStyle(self):
        self.layout().setContentsMargins(2,2,2,5)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        #self.vsplit.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Ignored)
        #self.setMinimumSize(790,210)
        #self.setMinimumHeight(320)
        #self.vsplit.setMinimumHeight(200)
        #self.vsplit.setHandleWidth(150)
        #self.vsplit.moveSplitter(10, self.vsplit.indexOf(self.guistatus))
        #self.vsplit.moveSplitter(300, self.vsplit.indexOf(self.vwidg))
        #self.setBaseSize(750,700)
        #self.setStyleSheet(cp.styleBkgd)

  
    #def resizeEvent(self, e):
        #logger.debug('resizeEvent', self.name)
        #print 'GUIFileManagerSingle resizeEvent: %s' % str(self.size())
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

        try    : self.guifilemanagersinglecontrol.close()        
        except : pass

        cp.guifilemanagersingle = None

#------------------------------

if __name__ == "__main__" :
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = GUIFileManagerSingle ()
    widget.show()
    app.exec_()

#------------------------------
#------------------------------
