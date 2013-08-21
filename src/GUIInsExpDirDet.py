#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module GUIInsExpDirDet...
#
#------------------------------------------------------------------------

"""GUI sets the calib directory from the instrument & experiment or selected non-standard directory."""

#------------------------------
#  Module's version from CVS --
#------------------------------
__version__ = "$Revision: 4 $"
# $Source$

#--------------------------------
#  Imports of standard modules --
#--------------------------------
import sys
import os

from PyQt4 import QtGui, QtCore
#import time   # for sleep(sec)

#-----------------------------
# Imports for other modules --
#-----------------------------

from ConfigParametersForApp import cp
import GlobalUtils          as     gu
from FileNameManager        import fnm
from Logger                 import logger

#---------------------
#  Class definition --
#---------------------
class GUIInsExpDirDet ( QtGui.QWidget ) :
    """GUI sets the configuration parameters for instrument, experiment, and run number"""

    char_expand    = u' \u25BE' # down-head triangle

    def __init__ ( self, parent=None ) :

        QtGui.QWidget.__init__(self, parent)

        cp.setIcons()

        self.instr_dir      = cp.instr_dir
        self.instr_name     = cp.instr_name
        self.exp_name       = cp.exp_name
        self.det_name       = cp.det_name
        self.calib_dir      = cp.calib_dir

        self.setGeometry(100, 50, 700, 30)
        self.setWindowTitle('Select calibration directory')
        self.setFrame()
 
        self.list_of_exp    = None

        self.titIns  = QtGui.QLabel('Ins:')
        self.titExp  = QtGui.QLabel('Exp:')
        self.titDet  = QtGui.QLabel('Det:')

        self.butIns  = QtGui.QPushButton( self.instr_name.value() + self.char_expand )
        self.butExp  = QtGui.QPushButton( self.exp_name.value()   + self.char_expand )
        self.butDet  = QtGui.QPushButton( self.det_name.value()   + self.char_expand )
        self.butBro  = QtGui.QPushButton( 'Browse' )

        self.ediDir = QtGui.QLineEdit  ( self.calib_dir.value() )
        self.ediDir.setReadOnly(True) 

        self.hbox = QtGui.QHBoxLayout() 
        self.hbox.addWidget(self.titIns)
        self.hbox.addWidget(self.butIns)
        self.hbox.addWidget(self.titExp)
        self.hbox.addWidget(self.butExp)
        self.hbox.addWidget(self.ediDir)
        self.hbox.addWidget(self.butBro)
        self.hbox.addStretch(1)     
        self.hbox.addWidget(self.titDet)
        self.hbox.addWidget(self.butDet)
        self.hbox.addStretch(1)     

        self.setLayout(self.hbox)

        #self.connect( self.ediExp,     QtCore.SIGNAL('editingFinished ()'), self.processEdiExp )
        self.connect( self.butIns,     QtCore.SIGNAL('clicked()'),          self.onButIns  )
        self.connect( self.butExp,     QtCore.SIGNAL('clicked()'),          self.onButExp )
        self.connect( self.butBro,     QtCore.SIGNAL('clicked()'),          self.onButBro )
        self.connect( self.butDet,     QtCore.SIGNAL('clicked()'),          self.onButDet )
        #self.connect( self.ediDir,     QtCore.SIGNAL('editingFinished()'),  self.onEdiDir )
  
        self.showToolTips()
        self.setStyle()

        self.setStatusMessage()

        cp.guiinsexpdirdet = self

    #-------------------
    #  Public methods --
    #-------------------

    def showToolTips(self):
        # Tips for buttons and fields:
        #self        .setToolTip('This GUI deals with the configuration parameters.')
        self.butIns .setToolTip('Select the instrument name from the pop-up menu.')
        self.butExp .setToolTip('Select the experiment name from the pop-up menu.')
        self.butBro .setToolTip('Select non-default calibration directory.')
        self.butDet .setToolTip('Select the detector for calibration.')
        self.ediDir .setToolTip('Use buttons to change the calib derectory.')

    def setFrame(self):
        self.frame = QtGui.QFrame(self)
        self.frame.setFrameStyle( QtGui.QFrame.Box | QtGui.QFrame.Sunken ) #Box, Panel | Sunken, Raised 
        self.frame.setLineWidth(0)
        self.frame.setMidLineWidth(1)
        self.frame.setGeometry(self.rect())
        self.frame.setVisible(False)

    def setStyle(self):
        
        #self.setStyleSheet(cp.styleYellow)
        self.titIns  .setStyleSheet (cp.styleLabel)
        self.titExp  .setStyleSheet (cp.styleLabel)
        self.titDet  .setStyleSheet (cp.styleLabel)

        self.        setFixedHeight(40)
        self.butIns .setFixedWidth(60)
        self.butExp .setFixedWidth(90)
        self.butBro .setFixedWidth(90)
        self.butDet .setFixedWidth(90)
        self.ediDir .setMinimumWidth(310)

        #self.ediDir.setStyleSheet(cp.styleGray)
        self.ediDir.setStyleSheet(cp.styleEditInfo)
        self.ediDir.setEnabled(False)            

        self.butBro .setIcon(cp.icon_browser)
        self.setContentsMargins(-5,-5,-5,-9) # (QtCore.QMargins(-9,-9,-9,-9))        

        self.setStyleButtons()
        

    def setStyleButtons(self):

        if self.instr_name.value() == 'Select' :
            self.butIns.setStyleSheet(cp.styleButtonGood)
            self.butExp.setStyleSheet(cp.styleDefault)
            self.butDet.setStyleSheet(cp.styleDefault)
            self.butExp.setEnabled(False)            
            self.butBro.setEnabled(False)            
            self.butDet.setEnabled(False)
            return

        self.butIns.setStyleSheet(cp.styleDefault)

        if self.exp_name.value() == 'Select' :
            self.butIns.setStyleSheet(cp.styleDefault)
            self.butExp.setStyleSheet(cp.styleButtonGood)
            self.butDet.setStyleSheet(cp.styleDefault)
            self.butExp.setEnabled(True)            
            self.butBro.setEnabled(False)            
            self.butDet.setEnabled(False)            
            return

        self.butExp.setStyleSheet(cp.styleDefault)
        self.butBro.setEnabled(True)            
        self.butDet.setStyleSheet(cp.styleDefault)
        self.butDet.setEnabled(True)            

        if self.det_name.value() == 'Select' :
            self.butDet.setStyleSheet(cp.styleButtonGood)

        #self.but.setVisible(False)
        #self.but.setEnabled(True)
        #self.but.setFlat(True)
 

    def setParent(self,parent) :
        self.parent = parent

    def closeEvent(self, event):
        logger.info('closeEvent', __name__)
        #print 'closeEvent'
        #try: # try to delete self object in the cp
        #    del cp.guiselectcalibdir# GUIInsExpDirDet
        #except AttributeError:
        #    pass # silently ignore

    def processClose(self):
        #print 'Close button'
        self.close()

    def resizeEvent(self, e):
        #print 'resizeEvent' 
        self.frame.setGeometry(self.rect())

    def moveEvent(self, e):
        #print 'moveEvent' 
        pass
#        cp.posGUIMain = (self.pos().x(),self.pos().y())


    def onButIns(self):
        #print 'onButIns'
        item_selected = gu.selectFromListInPopupMenu(cp.list_of_instr)
        if item_selected is None : return            # selection is cancelled
        if item_selected == self.instr_name.value() : return # selected the same item  

        self.setIns(item_selected)
        self.setExp('Select')
        self.setDir('Select')
        self.setDet('Select')
        self.setStyleButtons()


    def onButExp(self):
        #print 'onButExp'
        dir = self.instr_dir.value() + '/' + self.instr_name.value()
        #print 'dir =', dir
        if self.list_of_exp is None : self.list_of_exp=os.listdir(dir)
        item_selected = gu.selectFromListInPopupMenu(self.list_of_exp)
        if item_selected is None : return          # selection is cancelled
        #if item_selected == self.exp_name.value() : return # selected the same item 

        self.setExp(item_selected)
        self.setDir(fnm.path_to_calib_dir_default())
        self.setDet('Select')
        self.setStyleButtons()

        #if cp.guidarklist is not None : cp.guidarklist.updateList()

        path_to_xtc_dir = fnm.path_to_xtc_dir()
        if os.path.lexists(path_to_xtc_dir) : return
        
        msg = 'XTC data are not seen on this computer for path: %s' % path_to_xtc_dir
        logger.warning(msg, __name__)
        print msg


    def onButBro(self):
        path0 = self.calib_dir.value()
        #print 'path0:', path0
        #dir, calib = self.calib_dir.value().rsplit('/',1)        
        dir, calib = os.path.split(path0)
        #print 'dir, calib =', dir, calib
        path1 = str( QtGui.QFileDialog.getExistingDirectory(self,
                                                            'Select non-standard calib directory',
                                                            dir,
                                                            QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontResolveSymlinks) )

        if path1 == ''    : return # if nothing is selected
        if path1 == path0 : return # is selected the same directory
        self.setDir(path1)

    def onButDet(self):
        #print 'onButDet'
        item_selected = gu.selectFromListInPopupMenu(cp.list_of_dets)
        if item_selected is None : return            # selection is cancelled
        if item_selected == self.instr_name.value() : return # selected the same item  

        self.setDet(item_selected)
        self.setStyleButtons()

    def onEdiDir(self):
        pass

    def setIns(self, txt='Select'):
        self.instr_name.setValue( txt )
        self.butIns.setText( txt + self.char_expand )
        logger.info('Instrument selected: ' + str(txt), __name__)


    def setExp(self, txt='Select'):
        self.exp_name.setValue(txt)
        self.butExp.setText( txt + self.char_expand)
        if txt == 'Select' : self.list_of_exp = None        
        logger.info('Experiment selected: ' + str(txt), __name__)


    def setDir(self, txt='Select'):
        self.calib_dir.setValue(txt) 
        self.ediDir.setText(self.calib_dir.value())
        logger.info('Set calibration directory: ' + str(txt), __name__)


    def setDet(self, txt='Select'):
        
        self.det_name.setValue(txt)
        self.butDet.setText( txt + self.char_expand)
        #if txt == 'Select' : self.list_of_exp = None        
        logger.info('Selected detector: ' + str(txt), __name__)
        self.setStatusMessage()

        if cp.guidarklist is not None :

            cp.guidarklist.updateList()

            #if txt=='Select' or txt != self.det_name.value() : cp.guidarklist.setRun('Select')            
            if txt=='Select' : cp.guidarklist.setFieldsEnabled(False)
            else             : cp.guidarklist.setFieldsEnabled(True)



    def setStatusMessage(self):
        if cp.guistatus is None : return
        #msg = 'From %s to %s use dark run %s' % (self.str_run_from.value(), self.str_run_to.value(), self.str_run_number.value())
        msg = gu.get_text_content_of_calib_dir_for_detector(path=self.calib_dir.value(), det=self.det_name.value(), calib_type='pedestals')
        cp.guistatus.setStatusMessage(msg)

#-----------------------------

if __name__ == "__main__" :

    app = QtGui.QApplication(sys.argv)
    widget = GUIInsExpDirDet ()
    widget.show()
    app.exec_()

#-----------------------------
