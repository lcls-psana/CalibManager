#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#   GUIDarkListItemAdd ...
#------------------------------------------------------------------------

#--------------------------------
__version__ = "$Revision$"
#--------------------------------

#import os

from PyQt4 import QtGui, QtCore

from ConfigParametersForApp import cp
from Logger                 import logger
import GlobalUtils          as     gu
from GUIDarkMoreOpts        import *

#------------------------------

class GUIDarkListItemAdd(QtGui.QWidget) :
    """GUI extension of the Dark List Item"""

    def __init__(self, parent=None, run_number='0000') :

        QtGui.QWidget.__init__(self, parent)

        self.parent     = parent
        self.run_number = run_number

        self.setGeometry(100, 100, 600, 45)
        self.setWindowTitle('GUI Dark List Item')

        self.gui_more = GUIDarkMoreOpts(self, self.run_number)
        
        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addWidget(self.gui_more)
        self.vbox.addStretch(1)     

        self.setLayout(self.vbox)

        self.showToolTips()

        self.setStyle()


    def showToolTips(self):
        pass
        #self.lab_rnum.setToolTip('Data run for calibration.')


    def setStyle(self):
        self.setContentsMargins (QtCore.QMargins(-9,-9,-9,-9))
        self.setStyleSheet(cp.styleBkgd)


    #def resizeEvent(self, e):
        #logger.debug('resizeEvent', __name__) 
        #pass

        
    #def moveEvent(self, e):
        #logger.debug('moveEvent', __name__) 
        #cp.posGUIMain = (self.pos().x(),self.pos().y())
        #pass


    def closeEvent(self, event):
        logger.debug('closeEvent', __name__)
        #self.saveLogTotalInFile() # It will be saved at closing of GUIMain

        self.gui_more.close()

        try    : del self.gui_more
        except : pass


    def onClose(self):
        logger.info('onClose', __name__)
        self.close()


    def setStatusMessage(self):
        if cp.guistatus is None : return
        #cp.guistatus.setStatusMessage(msg)


    def getHeight(self):
        logger.debug('getHeight', __name__)
        h=0
        #if self.gui_table is not None :
        #    h += self.gui_table.height()
        h += 40 # for self.gui_more
        return h 
        
#-----------------------------

if __name__ == "__main__" :
    import sys
    app = QtGui.QApplication(sys.argv)
    w = GUIDarkListItemAdd(parent=None, run_number='0005')
    w.show()
    app.exec_()

#-----------------------------
