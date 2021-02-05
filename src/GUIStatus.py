from __future__ import absolute_import
#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  GUIStatus ...
#------------------------------------------------------------------------

#--------------------------------
__version__ = "$Revision$"
#--------------------------------

import os

from PyQt5 import QtCore, QtGui, QtWidgets

from .ConfigParametersForApp import cp
from CalibManager.Logger                 import logger
from . import GlobalUtils          as     gu

#---------------------

#class GUIStatus(QtGui.QWidget) :
class GUIStatus(QtWidgets.QGroupBox) :
    """GUI State"""

    def __init__(self, parent=None, msg='No message in GUIStatus...') :

        QtWidgets.QGroupBox.__init__(self, 'State', parent)
        #QtGui.QWidget.__init__(self, parent)
        self.setGeometry(100, 100, 300, 60)
        self.setWindowTitle('GUI Status')
        #try : self.setWindowIcon(cp.icon_help)
        #except : pass

        #self.instr_dir      = cp.instr_dir
        self.instr_name     = cp.instr_name
        self.exp_name       = cp.exp_name
        self.det_name       = cp.det_name
        self.det_but_title  = cp.det_but_title
        self.calib_dir      = cp.calib_dir
        self.current_tab    = cp.current_tab

        self.box_txt        = QtWidgets.QTextEdit(self)
        #self.tit_status     = QtGui.QLabel(' State ', self)

        #self.setTitle('My status')

        self.vbox  = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.box_txt)
        self.setLayout(self.vbox)

        #self.connect( self.but_close, QtCore.SIGNAL('clicked()'), self.onClose )
 
        self.setStatusMessage(msg)

        self.showToolTips()
        self.setStyle()

        cp.guistatus = self


    def showToolTips(self):
        #self           .setToolTip('This GUI is intended for run control and monitoring.')
        #self.but_close .setToolTip('Close this window.')
        pass


    def setStyle(self):
        self.           setStyleSheet (cp.styleBkgd)
        #self.tit_status.setStyleSheet (cp.styleTitle)
        #self.tit_status.setStyleSheet (cp.styleDefault)
        #self.tit_status.setStyleSheet (cp.styleTitleInFrame)
        self.box_txt   .setReadOnly   (True)
        #self.box_txt   .setStyleSheet (cp.styleBkgd)
        self.box_txt   .setStyleSheet (cp.styleWhiteFixed)
        self.layout().setContentsMargins(2,4,2,2)

        #self.setMinimumHeight(60)
        self.setMinimumSize(300,60)


    def setParent(self,parent) :
        self.parent = parent


    #def resizeEvent(self, e):
        #logger.debug('resizeEvent', __name__) 
        #self.box_txt.setGeometry(self.contentsRect())
        
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

        try    : del cp.guistatus # GUIStatus
        except : pass

        cp.guistatus = None


    def onClose(self):
        logger.debug('onClose', __name__)
        self.close()


    def setStatusMessage(self, msg='msg is empty...') :
        logger.debug('Set status message',__name__)
        self.box_txt.setText(msg)
        #self.setStatus(0, 'Status: unknown')


    def updateStatusInfo(self) :

        msg = ''

        if self.instr_name.value() == 'Select' : 
            msg += 'Select instrument now!'

        elif self.exp_name.value() == 'Select' : 
            msg += 'Select experiment now!'

        elif self.det_but_title.value() == 'Select' : 
            msg += 'Select detector(s) now!'

            #try : cp.guiinsexpdirdet.butDet.setStyleSheet(cp.styleButtonBad)
            #except : pass

        else :
            msg += 'Selected list of detector(s): %s' % self.det_name.value()

            ctype = 'pedestals'
            if self.current_tab.value() == 'Dark'         : ctype = 'pedestals'
            if self.current_tab.value() == 'File Manager' : ctype = None
            #if self.current_tab.value() == cp.guitabs.list_of_tabs[0] : ctype='pedestals'
            
            #msg = 'From %s to %s use dark run %s' % (self.str_run_from.value(), self.str_run_to.value(), self.str_run_number.value())
            
            
            #for det_name in self.det_name.value().split() :
            for det_name in cp.list_of_dets_selected() :
                calib_subdir = cp.dict_of_det_calib_types[det_name]
                #print 'calib_subdir =', calib_subdir
                msg += '\n' + gu.get_text_content_of_calib_dir_for_detector(path=self.calib_dir.value(), subdir=calib_subdir, det=det_name, calib_type=ctype)

        self.setStatusMessage(msg)

#------------------------------

if __name__ == "__main__" :
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = GUIStatus()
    w.setStatusMessage('Test of GUIStatus...')
    #w.statusOfDir('./')
    w.show()
    app.exec_()

#------------------------------
