#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  GUIExpCalibDir...
#------------------------------------------------------------------------

"""GUI sets the calib directory from the instrument & experiment or selected non-standard directory."""
from __future__ import print_function
from __future__ import absolute_import

#--------------------------------
__version__ = "$Revision$"
#--------------------------------

import os

from PyQt5 import QtCore, QtGui, QtWidgets

from .ConfigParametersForApp import cp
from . import GlobalUtils          as     gu
from .FileNameManager        import fnm
from CalibManager.Logger                 import logger
from .GUIPopupSelectExp      import select_experiment_v3

#------------------------------

class GUIExpCalibDir(QtWidgets.QWidget) :
    """GUI sets the configuration parameters for source calibration directory; exp_name_src and calib_dir_src"""

    char_expand  = cp.char_expand
    #char_expand  = u' \u25BC' # down-head triangle
    #char_expand  = '' # down-head triangle

    def __init__(self, parent=None) :

        QtWidgets.QWidget.__init__(self, parent)

        cp.setIcons()

        self.instr_dir      = cp.instr_dir
        self.instr_name     = cp.instr_name
        self.exp_name_src   = cp.exp_name_src
        self.calib_dir_src  = cp.calib_dir_src
        self.but_current    = None

        self.list_of_exp    = None

        self.setGeometry(100, 50, 500, 30)
        self.setWindowTitle('Select source calibration directory')
 
        self.titExp = QtWidgets.QLabel('Source of files:')
        self.butExp = QtWidgets.QPushButton(self.exp_name_src.value() + self.char_expand)
        self.butBro = QtWidgets.QPushButton('Browse')

        self.ediDir = QtWidgets.QLineEdit(self.calib_dir_src.value())
        self.ediDir.setReadOnly(True) 

        self.hbox = QtWidgets.QHBoxLayout() 
        self.hbox.addWidget(self.titExp)
        self.hbox.addWidget(self.butExp)
        self.hbox.addWidget(self.ediDir)
        self.hbox.addWidget(self.butBro)
        self.hbox.addStretch(1)     

        self.setLayout(self.hbox)

        self.butExp.clicked.connect(self.onButExp)
        self.butBro.clicked.connect(self.onButBro)
  
        self.showToolTips()
        self.setStyle()

        #self.setStatusMessage()
        #if cp.guistatus is not None : cp.guistatus.updateStatusInfo()

        cp.guiexpcalibdir = self


    def showToolTips(self):
        # Tips for buttons and fields:
        #self        .setToolTip('This GUI deals with the configuration parameters.')
        self.butExp .setToolTip('Select the experiment name from the pop-up menu.')
        self.butBro .setToolTip('Select non-default calibration directory.')
        self.ediDir .setToolTip('Use buttons to change the calib derectory.')


    def setStyle(self):
        #self.setStyleSheet(cp.styleYellow)
        self.titExp  .setStyleSheet (cp.styleLabel)
        self.        setFixedHeight(40)
        self.butExp .setFixedWidth(90)
        self.butBro .setFixedWidth(90)
        self.ediDir .setMinimumWidth(310)

        #self.ediDir.setStyleSheet(cp.styleGray)
        self.ediDir.setStyleSheet(cp.styleEditInfo)
        self.ediDir.setEnabled(False)            

        self.butBro .setIcon(cp.icon_browser)
        self.layout().setContentsMargins(2,2,2,0)

        self.setStyleButtons()
        

    def setStyleButtons(self):
        #logger.info('setStyleButtons', __name__)        
        if self.instr_name.value() == 'Select' :
            self.butExp.setStyleSheet(cp.styleDefault)
            self.butExp.setEnabled(False)            
            self.butBro.setEnabled(False)            
            return

        if self.exp_name_src.value() == 'Select' :
            self.butExp.setStyleSheet(cp.styleButtonGood)
            self.butExp.setEnabled(True)            
            self.butBro.setEnabled(False)            
            if cp.guistatus is not None :
                cp.guistatus.setStatusMessage('Select experiment for source calibration files...')
            return

        self.butExp.setStyleSheet(cp.styleDefault)
        self.butExp.setEnabled(True)            
        self.butBro.setEnabled(True)            

        #self.but.setVisible(False)
        #self.but.setEnabled(True)
        #self.but.setFlat(True)
 

    def setParent(self,parent) :
        self.parent = parent


    def closeEvent(self, event):
        logger.info('closeEvent', __name__)
        #print 'closeEvent'
        #try: # try to delete self object in the cp
        #    del cp.guiexpcalibdir# GUIExpCalibDir
        #except AttributeError:
        #    pass # silently ignore

        cp.guiexpcalibdir = None


    def processClose(self):
        #print 'Close button'
        self.close()


    #def resizeEvent(self, e):
        #print 'resizeEvent' 


    #def moveEvent(self, e):
        #print 'moveEvent' 
        #cp.posGUIMain = (self.pos().x(),self.pos().y())


    def onButExp(self):
        #print 'onButExp'
        self.but_current = self.butExp
        dir = self.instr_dir.value() + '/' + self.instr_name.value()
        #print 'dir =', dir
        #if self.list_of_exp is None : self.list_of_exp=sorted(os.listdir(dir))
        self.list_of_exp=sorted(os.listdir(dir))
        #item_selected = gu.selectFromListInPopupMenu(self.list_of_exp)
        item_selected = select_experiment_v3(self.butExp, self.list_of_exp)
        if item_selected is None : return          # selection is cancelled
        #if item_selected == self.exp_name_src.value() : return # selected the same item 

        self.setExp(item_selected)
        self.setDir(fnm.path_to_calib_dir_src_default())
        self.setStyleButtons()

        path_to_xtc_dir = fnm.path_to_xtc_dir()
        if os.path.lexists(path_to_xtc_dir) : return        
        msg = 'XTC data are not seen on this computer for path: %s' % path_to_xtc_dir
        logger.warning(msg, __name__)
        print(msg)


    def onButBro(self):
        path0 = self.calib_dir_src.value()
        #print 'path0:', path0
        #dir, calib = self.calib_dir_src.value().rsplit('/',1)        
        dir, calib = os.path.split(path0)
        #print 'dir, calib =', dir, calib
        path1 = str(QtWidgets.QFileDialog.getExistingDirectory(self,
                                                           'Select non-standard calib directory',
                                                           dir,
                                                           QtWidgets.QFileDialog.ShowDirsOnly | QtWidgets.QFileDialog.DontResolveSymlinks))

        if path1 == ''    : return # if nothing is selected
        if path1 == path0 : return # is selected the same directory
        dir1, calib1 = path1.rsplit('/',1) 
        if calib1 != 'calib' :
            logger.warning('This is not a "calib" directory!', __name__)
            return
        self.setExp('Custom')
        self.setDir(path1)


    def setExp(self, txt='Select'):
        self.exp_name_src.setValue(txt)
        self.butExp.setText( txt + self.char_expand)
        if txt == 'Select' : self.list_of_exp = None        
        logger.info('Source experiment selected: ' + str(txt), __name__)


    def setDir(self, txt='Select'):
        self.calib_dir_src.setValue(txt) 
        self.ediDir.setText(self.calib_dir_src.value())
        logger.info('Set source calibration directory: ' + str(txt), __name__)
        self.updateDirTree()


    def updateDirTree(self):
        logger.info('Update calibration directory', __name__)
        if cp.guidirtree is None : return

        cp.guidirtree.update_dir_tree(self.calib_dir_src.value())

#-----------------------------

if __name__ == "__main__" :
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = GUIExpCalibDir()
    widget.show()
    app.exec_()

#-----------------------------
