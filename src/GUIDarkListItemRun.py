from __future__ import absolute_import
#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#   GUIDarkListItemRun ...
#------------------------------------------------------------------------

#--------------------------------
__version__ = "$Revision$"
#--------------------------------

from PyQt5 import QtCore, QtGui, QtWidgets
import time   # for sleep(sec)
from time import time

from .ConfigParametersForApp import cp
from CalibManager.Logger                 import logger
from . import GlobalUtils          as     gu
from .FileNameManager        import fnm
from .BatchJobPedestals      import *
from . import FileDeployer         as     fdmets
from .BatchLogScanParser     import blsp # Just in order to instatiate it
from .GUIRange               import *

#------------------------------

class GUIDarkListItemRun(QtWidgets.QWidget) :
    """GUI sets the source dark run number, validity range, and starts calibration of pedestals"""

    def __init__(self, parent=None, str_run_number='0000', str_run_type='Type N/A', comment='', xtc_in_dir=True) :

        self.t0_sec = time()

        QtWidgets.QWidget.__init__(self, parent)

        self.setGeometry(100, 100, 600, 35)
        self.setWindowTitle('GUI Dark Run Item')
        #try : self.setWindowIcon(cp.icon_help)
        #except : pass

        #self.list_of_runs   = None
        self.parent = parent

        self.run_number     = int(str_run_number) # int run number
        self.str_run_number = str_run_number # cp.str_run_number
        self.str_run_type   = str_run_type   # cp.str_run_number
        self.comment        = comment
        self.xtc_in_dir     = xtc_in_dir
        self.calib_dir      = cp.calib_dir
        self.det_name       = cp.det_name
        self.dict_bjpeds    = cp.dict_bjpeds

        self.create_or_use_butch_object()

        self.lab_run = QtWidgets.QLabel('Run')

        self.guirange = GUIRange(None, str_run_number, 'end')

        self.lab_rnum = QtWidgets.QLabel(self.str_run_number)
        self.lab_type = QtWidgets.QLabel(self.str_run_type + '  ' + comment)
        self.but_go   = QtWidgets.QPushButton('Go')
        self.but_depl = QtWidgets.QPushButton('Deploy')

        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.lab_run)
        self.hbox.addWidget(self.lab_rnum)
        #self.hbox.addStretch(1)     
        self.hbox.addWidget(self.guirange)
        #self.hbox.addSpacing(150)     
        self.hbox.addStretch(1)     
        self.hbox.addWidget(self.but_go)
        self.hbox.addWidget(self.but_depl)
        self.hbox.addStretch(1)     
        self.hbox.addWidget(self.lab_type)

        self.setLayout(self.hbox)

        self.but_go.clicked.connect(self.onButGo)
        self.but_depl.clicked.connect(self.onButDeploy)
   
        self.showToolTips()

        self.setStatusMessage()
        self.setFieldsEnabled(cp.det_name.value() != '' and self.xtc_in_dir)

        #cp.guidarkrunitem = self
        #print '  GUIDarkListItemRun Consumed time (sec) =', time()-self.t0_sec


    def create_or_use_butch_object(self) :
        """Creates BatchJobPedestals object for the 1st time or use existing in the dictionary
        """
        self.bjpeds = BatchJobPedestals(self.run_number) 

#        if self.run_number in self.dict_bjpeds.keys() :
#            #print 'Use existing BatchJobPedestals object for run %s' % self.str_run_number
#            self.bjpeds = self.dict_bjpeds[self.run_number]
#        else :
#            #print 'Create new BatchJobPedestals object for run %s' % self.str_run_number
#            self.bjpeds = self.dict_bjpeds[self.run_number] = BatchJobPedestals(self.run_number) 


    def showToolTips(self):
        self.lab_rnum.setToolTip('Data run for calibration.')
        self.lab_type.setToolTip('Type of file (data, dark, etc).')
        self.but_go  .setToolTip('Begin data processing for calibration.')
        self.but_depl.setToolTip('Deploy file with constants\nin the calib directory.')


    def setFieldsEnabled(self, is_enabled=True):

        logger.debug('Set fields enabled: %s' %  is_enabled, __name__)

        #self.lab_rnum .setEnabled(is_enabled)
        self.but_go  .setEnabled(is_enabled)
        self.but_depl.setEnabled(is_enabled)

        self.guirange.setFieldsEnable(is_enabled)

        #if self.str_run_number == 'None' : ...

        self.setStyle()


    def setStyle(self):
        self.setMinimumSize(600,35)
        self.setStyleSheet(cp.styleBkgd)
        #self.setStyleSheet(cp.styleYellowish)

        self.lab_run .setStyleSheet(cp.styleLabel)
        self.but_depl.setStyleSheet(cp.styleButtonGood)

        #self.lab_rnum .setFixedWidth(60)        
        self.lab_type.setMinimumWidth(250)
        self.but_go  .setFixedWidth(60)        
        self.but_depl.setFixedWidth(80)

        #self.but_go.setEnabled(self.str_run_number != 'None' and self.lab_rnum.isEnabled())

        self.layout().setContentsMargins(9,0,9,0)

        self.setStatusStyleOfButtons()


    def setStatusStyleOfButtons(self):
        #logger.debug('setStyleOfButtons - update buttons status for %s' % self.str_run_number, __name__)
        files_are_available = self.bjpeds.status_for_peds_files_essential()
        #print 'setStatusStyleOfButtons: files_are_available = ', files_are_available        
        #print 'Work files for run %s status: %s' % (self.str_run_number, files_are_available)

        self.but_depl.setVisible(self.but_depl.isEnabled() and files_are_available )
        self.but_go  .setVisible(self.but_go  .isEnabled())

        if files_are_available : self.but_go.setStyleSheet(cp.styleButton)
        else                   : self.but_go.setStyleSheet(cp.styleButtonGood)

        #if self.but_go.text() == 'Stop' : 
            #self.but_go.setText('Go')


    #def resizeEvent(self, e):
        #logger.debug('resizeEvent', __name__) 
        #self.box_txt.setGeometry(self.contentsRect())
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

        #self.box_txt.close()

        #try    : del cp.guistatus # GUIDarkListItemRun
        #except : pass


    def onClose(self):
        logger.info('onClose', __name__)
        self.close()


    def exportLocalPars(self):
        """Exports local parameters to configuration current"""
        cp.str_run_number.setValue(self.str_run_number)
        #cp.str_run_from.setValue(self.str_run_from)
        #cp.str_run_to  .setValue(self.str_run_to)


    def onButGo(self):
        logger.debug('onButGo', __name__)
        self.exportLocalPars()
        self.but_depl.setVisible(False)
        but = self.but_go
        but.setStyleSheet(cp.styleDefault)

        if but.text() == 'Go' : 
            logger.info('onButGo for run %s' % self.str_run_number, __name__)
            but.setEnabled(False)
            self.bjpeds.start_auto_processing()
            if self.bjpeds.autoRunStage :            
                but.setText('Stop')
            but.setEnabled(True)

        elif but.text() == 'Stop' : 
            logger.info('onButStop for run %s' % self.str_run_number, __name__)
            self.bjpeds.stop_auto_processing()
            but.setEnabled(True)
            but.setText('Go')

        but.setStyleSheet(cp.styleButtonWarning)


    def onStop(self):
        msg = 'onStop - buttons status should be updated now for %s' % (self.str_run_number)
        logger.info(msg, __name__)
        self.but_go.setEnabled(True)        
        self.but_go.setText('Go')
        self.updateButtons()


    def setStatusMessage(self):
        pass
        #if cp.guistatus is None : return
        #cp.guistatus.setStatusMessage(msg)


    def onButDeploy(self):
        logger.debug('onButDeploy', __name__)
        but = self.but_depl
        but.setText('Busy...')
        but.setStyleSheet(cp.styleDefault)
        but.setEnabled(False)
        status = fdmets.deploy_calib_files(self.str_run_number, self.strRunRange(), mode='calibman-dark', ask_confirm=True)

        if status :
            but.setText('Deploy')
            but.setStyleSheet(cp.styleButtonWarning)
            #logger.warning('Deployment command terminated.', __name__)
        else :
            but.setText('Deployed')
            logger.info('Deployment command completed.', __name__)

        but.setEnabled(True)

        if cp.guistatus is not None : cp.guistatus.updateStatusInfo()


    def strRunRange(self):
        return self.guirange.getRange()

#---------
# deployment stuff from here moved to FileDeployer
#---------

    def updateButtons(self, str_run_type='', comment='', xtc_in_dir=True) :
        #logger.info('update', __name__)
        self.str_run_type = str_run_type
        self.comment = comment
        self.xtc_in_dir = xtc_in_dir
        self.lab_type.setText(str_run_type + '  ' + comment)

        self.setFieldsEnabled(cp.det_name.value() != '' and self.xtc_in_dir)
        #self.setStatusStyleOfButtons()

#------------------------------

if __name__ == "__main__" :
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = GUIDarkListItemRun(parent=None, str_run_number='0016')
    w.setFieldsEnabled(True)
    w.show()
    app.exec_()

#------------------------------
