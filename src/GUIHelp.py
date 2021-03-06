#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#   GUIHelp...
#------------------------------------------------------------------------

"""GUI for help messages"""
from __future__ import absolute_import
#--------------------------------
__version__ = "$Revision$"
#--------------------------------

import os

from PyQt5 import QtCore, QtGui, QtWidgets

from CalibManager.Frame     import Frame
from .ConfigParametersForApp import cp
from CalibManager.Logger                 import logger

#------------------------------
#class GUIHelp(QtGui.QWidget) :
class GUIHelp(Frame) :
    """GUI Help"""

    def __init__(self, parent=None, msg='No message in GUIHelp...') :

        #QtGui.QWidget.__init__(self, parent)
        Frame.__init__(self, parent, mlw=1)

        self.setGeometry(100, 100, 730, 200)
        self.setWindowTitle('GUI Help')
        try : self.setWindowIcon(cp.icon_help)
        except : pass

        self.box_txt    = QtWidgets.QTextEdit()
        self.tit_status = QtWidgets.QLabel('Status:')
        self.but_close  = QtWidgets.QPushButton('Close') 

        self.hboxM = QtWidgets.QHBoxLayout()
        self.hboxM.addWidget( self.box_txt )

        self.hboxB = QtWidgets.QHBoxLayout()
        self.hboxB.addWidget(self.tit_status)
        self.hboxB.addStretch(4)     
        self.hboxB.addWidget(self.but_close)

        self.vbox  = QtWidgets.QVBoxLayout()
        self.vbox.addLayout(self.hboxM)
        self.vbox.addLayout(self.hboxB)
        self.setLayout(self.vbox)
        
        self.but_close.clicked.connect(self.onClose)
 
        self.setHelpMessage(msg)

        self.showToolTips()
        self.setStyle()


    def showToolTips(self):
        #self           .setToolTip('This GUI is intended for run control and monitoring.')
        self.but_close .setToolTip('Close this window.')


    def setStyle(self):
        self.setMinimumHeight(300)
        self.           setStyleSheet(cp.styleBkgd)
        self.tit_status.setStyleSheet(cp.styleTitle)
        self.but_close .setStyleSheet(cp.styleButton)
        self.box_txt   .setReadOnly  (True)
        self.box_txt   .setStyleSheet(cp.styleWhiteFixed) 


    def setParent(self,parent) :
        self.parent = parent


    #def resizeEvent(self, e):
        #logger.debug('resizeEvent', __name__) 
        #self.frame.setGeometry(self.rect())
        #pass

    #def moveEvent(self, e):
        #logger.debug('moveEvent', __name__) 
        #cp.posGUIMain = (self.pos().x(),self.pos().y())
        #pass


    def closeEvent(self, event):
        logger.debug('closeEvent', __name__)
        #self.saveLogTotalInFile() # It will be saved at closing of GUIMain

        #try    : cp.guimain.butLogger.setStyleSheet(cp.styleButtonBad)
        #except : pass

        self.box_txt.close()

        try    : del cp.guihelp # GUIHelp
        except : pass


    def onClose(self):
        logger.debug('onClose', __name__)
        self.close()


    def setHelpMessage(self, msg) :
        logger.debug('Set help message',__name__)
        self.box_txt.setText(msg)
        self.setStatus(0, 'Status: show help info...')


    def setStatus(self, status_index=0, msg=''):
        list_of_states = ['Good','Warning','Alarm']
        if status_index == 0 : self.tit_status.setStyleSheet(cp.styleStatusGood)
        if status_index == 1 : self.tit_status.setStyleSheet(cp.styleStatusWarning)
        if status_index == 2 : self.tit_status.setStyleSheet(cp.styleStatusAlarm)

        #self.tit_status.setText('Status: ' + list_of_states[status_index] + msg)
        self.tit_status.setText(msg)

#------------------------------

if __name__ == "__main__" :
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = GUIHelp()
    w.setHelpMessage('This is a test message to test methods of GUIHelp...')
    w.show()
    app.exec_()

#------------------------------
