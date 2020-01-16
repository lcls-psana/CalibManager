from __future__ import absolute_import
#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#------------------------------------------------------------------------

#---------------------------------
__version__ = "$Revision$"
#---------------------------------

import os

from PyQt5 import QtCore, QtGui, QtWidgets

from CalibManager.Frame     import Frame
from .ConfigParametersForApp import cp
from CalibManager.Logger                 import logger
from . import GlobalUtils          as     gu

#------------------------------

#class GUIConfigPars(QtGui.QWidget) :
class GUIConfigPars(Frame) :
    """GUI for management of configuration parameters"""

    def __init__(self, parent=None) :
        #QtGui.QWidget.__init__(self, parent)
        Frame.__init__(self, parent, mlw=1)

        self.setGeometry(200, 400, 500, 200)
        self.setWindowTitle('Configuration Parameters')

        #self.tit_dir_work = QtGui.QLabel('Parameters:')

        self.edi_dir_work = QtWidgets.QLineEdit(cp.dir_work.value())        
        self.but_dir_work = QtWidgets.QPushButton('Dir work:')
        self.edi_dir_work.setReadOnly(True)  

        self.edi_dir_results = QtWidgets.QLineEdit(cp.dir_results.value())        
        self.but_dir_results = QtWidgets.QPushButton('Dir results:')
        self.edi_dir_results.setReadOnly( True )  

        self.lab_fname_prefix = QtWidgets.QLabel('File prefix:')
        self.edi_fname_prefix = QtWidgets.QLineEdit(cp.fname_prefix.value())        

        self.lab_bat_queue  = QtWidgets.QLabel('Queue:') 
        self.box_bat_queue  = QtWidgets.QComboBox(self) 
        self.box_bat_queue.addItems(cp.list_of_queues)
        self.box_bat_queue.setCurrentIndex(cp.list_of_queues.index(cp.bat_queue.value()))

        self.lab_dark_start = QtWidgets.QLabel('Event start:') 
        self.lab_dark_end   = QtWidgets.QLabel('end:') 
        self.lab_dark_scan  = QtWidgets.QLabel('scan:') 
        self.lab_timeout    = QtWidgets.QLabel('t-out, sec:') 
        self.lab_pix_status = QtWidgets.QLabel('Pixel status parameters:') 
        self.lab_rms_thr_min= QtWidgets.QLabel('RMS MIN:') 
        self.lab_rms_thr_max= QtWidgets.QLabel('MAX:') 
        self.lab_min_thr    = QtWidgets.QLabel('Intensity MIN:') 
        self.lab_max_thr    = QtWidgets.QLabel('MAX:') 
        self.lab_dark_sele  = QtWidgets.QLabel('Event code:') 
        self.lab_rmsnlo     = QtWidgets.QLabel('nsigma LO:') 
        self.lab_rmsnhi     = QtWidgets.QLabel('HI:') 
        self.lab_intnlo     = QtWidgets.QLabel('nsigma LO:') 
        self.lab_intnhi     = QtWidgets.QLabel('HI:') 

        self.but_show_vers  = QtWidgets.QPushButton('Soft Vers')
        self.but_lsf_status = QtWidgets.QPushButton('LSF status')

        self.edi_dark_start = QtWidgets.QLineEdit(str(cp.bat_dark_start.value()))
        self.edi_dark_end   = QtWidgets.QLineEdit(str(cp.bat_dark_end.value()))
        self.edi_dark_scan  = QtWidgets.QLineEdit(str(cp.bat_dark_scan.value()))
        self.edi_timeout    = QtWidgets.QLineEdit(str(cp.job_timeout_sec.value()))
        self.edi_dark_sele  = QtWidgets.QLineEdit(str(cp.bat_dark_sele.value()))
        self.edi_rms_thr_min= QtWidgets.QLineEdit(str(cp.mask_rms_thr_min.value()))
        self.edi_rms_thr_max= QtWidgets.QLineEdit(str(cp.mask_rms_thr_max.value()))
        self.edi_min_thr    = QtWidgets.QLineEdit(str(cp.mask_min_thr.value()))
        self.edi_max_thr    = QtWidgets.QLineEdit(str(cp.mask_max_thr.value()))
        self.edi_rmsnlo = QtWidgets.QLineEdit(str(cp.mask_rmsnlo.value()))
        self.edi_rmsnhi = QtWidgets.QLineEdit(str(cp.mask_rmsnhi.value()))
        self.edi_intnlo = QtWidgets.QLineEdit(str(cp.mask_intnlo.value()))
        self.edi_intnhi = QtWidgets.QLineEdit(str(cp.mask_intnhi.value()))

        self.edi_dark_start .setValidator(QtGui.QIntValidator(0,9999999,self))
        self.edi_dark_end   .setValidator(QtGui.QIntValidator(1,9999999,self))
        self.edi_dark_scan  .setValidator(QtGui.QIntValidator(1,9999999,self))
        self.edi_timeout    .setValidator(QtGui.QIntValidator(1,9999999,self))
        #self.edi_dark_sele  .setValidator(QtGui.QIntValidator(-256,256,self)) # str like '1,2,3'
        self.edi_rms_thr_min.setValidator(QtGui.QDoubleValidator(0,65000,3,self))
        self.edi_rms_thr_max.setValidator(QtGui.QDoubleValidator(0,65000,3,self))
        self.edi_min_thr    .setValidator(QtGui.QDoubleValidator(0,65000,3,self))
        self.edi_max_thr    .setValidator(QtGui.QDoubleValidator(0,65000,3,self))
        self.edi_rmsnlo     .setValidator(QtGui.QDoubleValidator(0,1000000,3,self))
        self.edi_rmsnhi     .setValidator(QtGui.QDoubleValidator(0,1000000,3,self))
        self.edi_intnlo     .setValidator(QtGui.QDoubleValidator(0,1000000,3,self))
        self.edi_intnhi     .setValidator(QtGui.QDoubleValidator(0,1000000,3,self))

        #self.edi_events.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]\\d{0,3}|end$"),self))

        self.cbx_deploy_hotpix = QtWidgets.QCheckBox('Deploy pixel_status')
        self.cbx_deploy_hotpix.setChecked(cp.dark_deploy_hotpix.value())

        self.cbx_deploy_cmod = QtWidgets.QCheckBox('Deploy common_mode')
        self.cbx_deploy_cmod.setChecked(cp.dark_deploy_cmod.value())

        self.cbx_smd_or_xtc = QtWidgets.QCheckBox('smd is on')
        self.cbx_smd_or_xtc.setChecked(cp.smd_is_on.value())

        self.grid = QtWidgets.QGridLayout()
        self.grid_row = 0
        #self.grid.addWidget(self.tit_dir_work,      self.grid_row,   0, 1, 9)
        self.grid.addWidget(self.but_dir_work,      self.grid_row+1, 0)
        self.grid.addWidget(self.edi_dir_work,      self.grid_row+1, 1, 1, 8)
        self.grid.addWidget(self.but_dir_results,   self.grid_row+2, 0)
        self.grid.addWidget(self.edi_dir_results,   self.grid_row+2, 1, 1, 8)
        self.grid.addWidget(self.lab_fname_prefix,  self.grid_row+3, 0)
        self.grid.addWidget(self.edi_fname_prefix,  self.grid_row+3, 1, 1, 4)
        self.grid.addWidget(self.lab_bat_queue,     self.grid_row+4, 0)
        self.grid.addWidget(self.box_bat_queue,     self.grid_row+4, 1)
        self.grid.addWidget(self.but_lsf_status,    self.grid_row+4, 4) #, 1, 2)
        self.grid.addWidget(self.but_show_vers,     self.grid_row+4, 6) #, 1, 2)
        self.grid.addWidget(self.lab_dark_start,    self.grid_row+5, 0)
        self.grid.addWidget(self.edi_dark_start,    self.grid_row+5, 1)
        self.grid.addWidget(self.lab_dark_end,      self.grid_row+5, 3)
        self.grid.addWidget(self.edi_dark_end,      self.grid_row+5, 4)
        self.grid.addWidget(self.lab_dark_scan,     self.grid_row+5, 5)
        self.grid.addWidget(self.edi_dark_scan,     self.grid_row+5, 6)
        self.grid.addWidget(self.lab_timeout,       self.grid_row+5, 7)
        self.grid.addWidget(self.edi_timeout,       self.grid_row+5, 8)

        self.grid.addWidget(self.cbx_deploy_hotpix, self.grid_row+6, 0, 1, 2)
        self.grid.addWidget(self.cbx_deploy_cmod,   self.grid_row+6, 3, 1, 4)
        self.grid.addWidget(self.cbx_smd_or_xtc,    self.grid_row+6, 6, 1, 3)
        self.grid.addWidget(self.lab_dark_sele,     self.grid_row+6, 7)
        self.grid.addWidget(self.edi_dark_sele,     self.grid_row+6, 8)

        #self.grid.addWidget(self.lab_pix_status,    self.grid_row+7, 0, 1, 6)

        self.grid.addWidget(self.lab_min_thr,       self.grid_row+8, 0)
        self.grid.addWidget(self.edi_min_thr,       self.grid_row+8, 1)
        self.grid.addWidget(self.lab_max_thr,       self.grid_row+8, 2)
        self.grid.addWidget(self.edi_max_thr,       self.grid_row+8, 3)

        self.grid.addWidget(self.lab_intnlo,        self.grid_row+8, 4, 1, 2)
        self.grid.addWidget(self.edi_intnlo,        self.grid_row+8, 6)
        self.grid.addWidget(self.lab_intnhi,        self.grid_row+8, 7)
        self.grid.addWidget(self.edi_intnhi,        self.grid_row+8, 8)

        self.grid.addWidget(self.lab_rms_thr_min,   self.grid_row+9, 0)
        self.grid.addWidget(self.edi_rms_thr_min,   self.grid_row+9, 1)
        self.grid.addWidget(self.lab_rms_thr_max,   self.grid_row+9, 2)
        self.grid.addWidget(self.edi_rms_thr_max,   self.grid_row+9, 3)

        self.grid.addWidget(self.lab_rmsnlo,        self.grid_row+9, 4, 1, 2)
        self.grid.addWidget(self.edi_rmsnlo,        self.grid_row+9, 6)
        self.grid.addWidget(self.lab_rmsnhi,        self.grid_row+9, 7)
        self.grid.addWidget(self.edi_rmsnhi,        self.grid_row+9, 8)

        #self.setLayout(self.grid)

        self.vbox = QtWidgets.QVBoxLayout() 
        self.vbox.addLayout(self.grid)
        self.vbox.addStretch(1)
        self.setLayout(self.vbox)

        self.but_dir_work.clicked.connect(self.onButDirWork)
        self.but_dir_results.clicked.connect(self.onButDirResults)
        self.box_bat_queue.currentIndexChanged[int].connect(self.onBoxBatQueue)
        self.edi_fname_prefix.editingFinished .connect(self.onEditPrefix)
        self.edi_dark_start.editingFinished.connect(self.onEdiDarkStart)
        self.edi_dark_end.editingFinished.connect(self.onEdiDarkEnd)
        self.edi_dark_scan.editingFinished.connect(self.onEdiDarkScan)
        self.edi_timeout.editingFinished.connect(self.onEdiTimeOut)
        self.edi_dark_sele.editingFinished.connect(self.onEdiDarkSele)
        self.edi_rms_thr_min.editingFinished.connect(self.onEdiRmsThrMin)
        self.edi_rms_thr_max.editingFinished.connect(self.onEdiRmsThr)
        self.edi_min_thr.editingFinished.connect(self.onEdiMinThr)
        self.edi_max_thr.editingFinished.connect(self.onEdiMaxThr)
        self.edi_rmsnlo.editingFinished.connect(self.onEdiRmsNsigLo)
        self.edi_rmsnhi.editingFinished.connect(self.onEdiRmsNsigHi)
        self.edi_intnlo.editingFinished.connect(self.onEdiIntNsigLo)
        self.edi_intnhi.editingFinished.connect(self.onEdiIntNsigHi)
        self.cbx_deploy_hotpix.stateChanged[int].connect(self.on_cbx_deploy_hotpix)
        self.cbx_deploy_cmod.stateChanged[int].connect(self.on_cbx_deploy_cmod)
        self.cbx_smd_or_xtc.stateChanged[int].connect(self.on_cbx_smd_or_xtc)
        self.but_show_vers.clicked.connect(self.onButShowVers)
        self.but_lsf_status.clicked.connect(self.onButLsfStatus)
 
        self.showToolTips()
        self.setStyle()


    def showToolTips(self):
        self.edi_dir_work     .setToolTip('Click on "Dir work:" button\nto change the directory')
        self.but_dir_work     .setToolTip('Click on this button\nand select the directory')
        self.edi_dir_results  .setToolTip('Click on "Dir results:" button\nto change the directory')
        self.but_dir_results  .setToolTip('Click on this button\nand select the directory')
        self.edi_fname_prefix .setToolTip('Edit the common file prefix in this field')
        self.but_show_vers    .setToolTip('Show current package tags')
        self.but_lsf_status   .setToolTip('Show LSF status')
        self.edi_dark_sele    .setToolTip('Comma separated event codes;\nNone=off, +N=select, -N=discard.\nEx.: 43,45')
        self.cbx_smd_or_xtc   .setToolTip('Switch between .smd and .xtc modes')
        self.cbx_deploy_hotpix.setToolTip('Deploy or not pixel_status constants')
        self.cbx_deploy_cmod  .setToolTip('Deploy or not common_mode constants (for PNCCD only)')


    def setStyle(self):
        self.                 setStyleSheet (cp.styleBkgd)
        self.setMinimumSize(500,300)
        self.setMaximumSize(700,300)

        #self.tit_dir_work     .setStyleSheet(cp.styleTitle)
        self.edi_dir_work     .setStyleSheet(cp.styleEditInfo)       
        self.but_dir_work     .setStyleSheet(cp.styleButton) 
        self.edi_dir_results  .setStyleSheet(cp.styleEditInfo)       
        self.but_dir_results  .setStyleSheet(cp.styleButton) 
        self.lab_fname_prefix .setStyleSheet(cp.styleLabel)
        self.edi_fname_prefix .setStyleSheet(cp.styleEdit)
        self.lab_bat_queue    .setStyleSheet(cp.styleLabel)
        self.lab_dark_start   .setStyleSheet(cp.styleLabel)
        self.lab_dark_end     .setStyleSheet(cp.styleLabel)
        self.lab_dark_scan    .setStyleSheet(cp.styleLabel)
        self.lab_timeout      .setStyleSheet(cp.styleLabel)
        self.lab_dark_sele    .setStyleSheet(cp.styleLabel)
        self.lab_pix_status   .setStyleSheet(cp.styleTitleBold)
        self.lab_rms_thr_min  .setStyleSheet(cp.styleLabel)
        self.lab_rms_thr_max  .setStyleSheet(cp.styleLabel)
        self.lab_min_thr      .setStyleSheet(cp.styleLabel)
        self.lab_max_thr      .setStyleSheet(cp.styleLabel)
        self.cbx_deploy_hotpix.setStyleSheet(cp.styleLabel)
        self.cbx_deploy_cmod  .setStyleSheet(cp.styleLabel)
        self.cbx_smd_or_xtc   .setStyleSheet(cp.styleLabel)
        self.but_show_vers    .setStyleSheet(cp.styleButton) 
        self.but_lsf_status   .setStyleSheet(cp.styleButton) 
        self.lab_rmsnlo       .setStyleSheet(cp.styleLabel)
        self.lab_rmsnhi       .setStyleSheet(cp.styleLabel)
        self.lab_intnlo       .setStyleSheet(cp.styleLabel)
        self.lab_intnhi       .setStyleSheet(cp.styleLabel)

        #self.tit_dir_work    .setAlignment(QtCore.Qt.AlignLeft)
        self.edi_dir_work    .setAlignment(QtCore.Qt.AlignRight)
        self.edi_dir_results .setAlignment(QtCore.Qt.AlignRight)
        self.lab_fname_prefix.setAlignment(QtCore.Qt.AlignRight)
        self.lab_bat_queue   .setAlignment(QtCore.Qt.AlignRight)
        self.lab_dark_start  .setAlignment(QtCore.Qt.AlignRight)
        self.lab_dark_end    .setAlignment(QtCore.Qt.AlignRight)
        self.lab_dark_scan   .setAlignment(QtCore.Qt.AlignRight)
        self.lab_timeout     .setAlignment(QtCore.Qt.AlignRight)
        self.lab_dark_sele   .setAlignment(QtCore.Qt.AlignRight)
        self.lab_pix_status  .setAlignment(QtCore.Qt.AlignLeft)
        self.lab_rms_thr_min .setAlignment(QtCore.Qt.AlignRight)
        self.lab_rms_thr_max .setAlignment(QtCore.Qt.AlignRight)
        self.lab_min_thr     .setAlignment(QtCore.Qt.AlignRight)
        self.lab_max_thr     .setAlignment(QtCore.Qt.AlignRight)
        self.lab_rmsnlo      .setAlignment(QtCore.Qt.AlignRight)
        self.lab_rmsnhi      .setAlignment(QtCore.Qt.AlignRight)
        self.lab_intnlo      .setAlignment(QtCore.Qt.AlignRight)
        self.lab_intnhi      .setAlignment(QtCore.Qt.AlignRight)

        self.edi_dir_work    .setMinimumWidth(300)
        self.but_dir_work    .setFixedWidth(80)
        self.edi_dir_results .setMinimumWidth(300)
        self.but_dir_results .setFixedWidth(80)
        self.box_bat_queue   .setFixedWidth(100)
        self.edi_dark_start  .setFixedWidth(80)
        self.edi_dark_end    .setFixedWidth(80)
        self.edi_dark_scan   .setFixedWidth(80)
        self.edi_timeout     .setFixedWidth(80)
        self.edi_dark_sele   .setFixedWidth(80)
        self.edi_rms_thr_min .setFixedWidth(80)
        self.edi_rms_thr_max .setFixedWidth(80)
        self.edi_min_thr     .setFixedWidth(80)
        self.edi_max_thr     .setFixedWidth(80)
        self.but_show_vers   .setFixedWidth(80)
        self.but_lsf_status  .setFixedWidth(80)
        self.edi_rmsnlo      .setFixedWidth(80)
        self.edi_rmsnhi      .setFixedWidth(80)
        self.edi_intnlo      .setFixedWidth(80)
        self.edi_intnhi      .setFixedWidth(80)


    def setParent(self,parent) :
        self.parent = parent


    #def resizeEvent(self, e):
        #logger.debug('resizeEvent', __name__) 
        #pass


    #def moveEvent(self, e):
        #logger.debug('moveEvent', __name__) 
        #cp.posGUIMain = (self.pos().x(),self.pos().y())
        #pass


    def closeEvent(self, event):
        logger.debug('closeEvent', __name__)
        #try    : del cp.guiworkresdirs # GUIConfigPars
        #except : pass # silently ignore


    def onClose(self):
        logger.debug('onClose', __name__)
        self.close()


    def onButShowVers(self):
        #list_of_pkgs = ['CalibManager', 'ImgAlgos'] #, 'CSPadPixCoords', 'PSCalib', 'pdscalibdata']
        #msg = 'Package versions:\n'
        #for pkg in list_of_pkgs :
        #    msg += '%s  %s\n' % (gu.get_pkg_version(pkg).ljust(10), pkg.ljust(32))

        #msg = cp.package_versions.text_version_for_all_packages()
        msg = cp.package_versions.text_rev_and_tag_for_all_packages()
        logger.info(msg, __name__ )


    def onButLsfStatus(self):
        queue = cp.bat_queue.value()
        farm = cp.dict_of_queue_farm[queue]
        msg, status = gu.msg_and_status_of_lsf(farm)
        msgi = '\nLSF status for queue %s on farm %s: \n%s\nLSF status for %s is %s' % \
               (queue, farm, msg, queue, {False:'bad',True:'good'}[status])
        logger.info(msgi, __name__)

        cmd, msg = gu.text_status_of_queues(cp.list_of_queues)
        msgq = '\nStatus of queues for command: %s \n%s' % (cmd, msg)       
        logger.info(msgq, __name__)


    def onButDirWork(self):
        self.selectDirectory(cp.dir_work, self.edi_dir_work, 'work')


    def onButDirResults(self):
        self.selectDirectory(cp.dir_results, self.edi_dir_results, 'results')


    def selectDirectory(self, par, edi, label=''):        
        logger.debug('Select directory for ' + label, __name__)
        dir0 = par.value()
        path, name = os.path.split(dir0)
        dir = str(QtWidgets.QFileDialog.getExistingDirectory(None,'Select directory for '+label,path))

        if dir == dir0 or dir == '' :
            logger.info('Directiry for ' + label + ' has not been changed.', __name__)
            return
        edi.setText(dir)        
        par.setValue(dir)
        logger.info('Set directory for ' + label + str(par.value()), __name__)

        gu.create_directory(dir)


    def onBoxBatQueue(self):
        queue_selected = self.box_bat_queue.currentText()
        cp.bat_queue.setValue( queue_selected ) 
        logger.info('onBoxBatQueue - queue_selected: ' + queue_selected, __name__)


    def onEditPrefix(self):
        logger.debug('onEditPrefix', __name__)
        cp.fname_prefix.setValue(str(self.edi_fname_prefix.displayText()))
        logger.info('Set file name common prefix: ' + str( cp.fname_prefix.value()), __name__)


    def onEdiDarkStart(self):
        str_value = str(self.edi_dark_start.displayText())
        cp.bat_dark_start.setValue(int(str_value))      
        logger.info('Set start event for dark run: %s' % str_value, __name__)


    def onEdiDarkEnd(self):
        str_value = str(self.edi_dark_end.displayText())
        cp.bat_dark_end.setValue(int(str_value))      
        logger.info('Set last event for dark run: %s' % str_value, __name__)


    def onEdiDarkScan(self):
        str_value = str(self.edi_dark_scan.displayText())
        cp.bat_dark_scan.setValue(int(str_value))      
        logger.info('Set the number of events to scan: %s' % str_value, __name__)


    def onEdiTimeOut(self):
        str_value = str(self.edi_timeout.displayText())
        cp.job_timeout_sec.setValue(int(str_value))      
        logger.info('Job execution timout, sec : %s' % str_value, __name__)


    def onEdiDarkSele(self):
        str_value = str(self.edi_dark_sele.displayText())
        if str_value == '' : str_value = 'None'
        cp.bat_dark_sele.setValue(str_value)      
        logger.info('Set the event code for selector: %s' % str_value, __name__)


    def onEdiRmsThrMin(self):
        str_value = str(self.edi_rms_thr_min.displayText())
        cp.mask_rms_thr_min.setValue(float(str_value))  
        logger.info('Set hot pixel RMS MIN threshold: %s' % str_value, __name__)


    def onEdiRmsThr(self):
        str_value = str(self.edi_rms_thr_max.displayText())
        cp.mask_rms_thr_max.setValue(float(str_value))  
        logger.info('Set hot pixel RMS MAX threshold: %s' % str_value, __name__)


    def onEdiMinThr(self):
        str_value = str(self.edi_min_thr.displayText())
        cp.mask_min_thr.setValue(float(str_value))  
        logger.info('Set hot pixel intensity MIN threshold: %s' % str_value, __name__)


    def onEdiMaxThr(self):
        str_value = str(self.edi_max_thr.displayText())
        cp.mask_max_thr.setValue(float(str_value))  
        logger.info('Set hot pixel intensity MAX threshold: %s' % str_value, __name__)


    def onEdiRmsNsigLo(self):
        str_value = str(self.edi_rmsnlo.displayText())
        cp.mask_rmsnlo.setValue(float(str_value))  
        logger.info('Set nsigma low limit of rms: %s' % str_value, __name__)


    def onEdiRmsNsigHi(self):
        str_value = str(self.edi_rmsnhi.displayText())
        cp.mask_rmsnhi.setValue(float(str_value))  
        logger.info('Set nsigma high limit of rms: %s' % str_value, __name__)




    def onEdiIntNsigLo(self):
        str_value = str(self.edi_intnlo.displayText())
        cp.mask_intnlo.setValue(float(str_value))  
        logger.info('Set nsigma low limit of intensity: %s' % str_value, __name__)


    def onEdiIntNsigHi(self):
        str_value = str(self.edi_intnhi.displayText())
        cp.mask_intnhi.setValue(float(str_value))  
        logger.info('Set nsigma high limit of intensity: %s' % str_value, __name__)




    def on_cbx(self, par, cbx):
        #if cbx.hasFocus() :
        par.setValue(cbx.isChecked())
        msg = 'check box %s is set to: %s' % (cbx.text(), str(par.value()))
        logger.info(msg, __name__)


    def on_cbx_smd_or_xtc(self):
        self.on_cbx(cp.smd_is_on, self.cbx_smd_or_xtc)


    def on_cbx_deploy_hotpix(self):
        self.on_cbx(cp.dark_deploy_hotpix, self.cbx_deploy_hotpix)


    def on_cbx_deploy_cmod(self):
        self.on_cbx(cp.dark_deploy_cmod, self.cbx_deploy_cmod)

#-----------------------------

if __name__ == "__main__" :
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = GUIConfigPars()
    widget.show()
    app.exec_()

#-----------------------------
