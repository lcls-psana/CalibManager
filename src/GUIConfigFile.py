#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#   GUIConfigFile...
#------------------------------------------------------------------------

"""GUI for configuration file parameters management"""
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

#class GUIConfigFile(QtGui.QWidget) :
class GUIConfigFile(Frame) :
    """GUI for configuration file parameters management"""

    def __init__(self, parent=None) :

        #QtGui.QWidget.__init__(self, parent)
        Frame.__init__(self, parent, mlw=1)

        #self.parent = cp.guimain

        self.setGeometry(370, 350, 500,150)
        self.setWindowTitle('Configuration File')
        
        self.titFile     = QtWidgets.QLabel('File with configuration parameters:')
        self.titPars     = QtWidgets.QLabel('Operations on file:')
        self.butFile     = QtWidgets.QPushButton('File:')
        self.butRead     = QtWidgets.QPushButton('Read')
        self.butWrite    = QtWidgets.QPushButton('Save')
        self.butDefault  = QtWidgets.QPushButton('Reset default')
        self.butPrint    = QtWidgets.QPushButton('Print current')
        self.ediFile     = QtWidgets.QLineEdit( cp.fname_cp )        
        self.cbxSave     = QtWidgets.QCheckBox('&Save at exit')
        self.cbxSave.setChecked( cp.save_cp_at_exit.value() )
 
        grid = QtWidgets.QGridLayout()
        grid.addWidget(self.titFile,       0, 0, 1, 5)
        grid.addWidget(self.butFile,       1, 0)
        grid.addWidget(self.ediFile,       1, 1, 1, 4)
        grid.addWidget(self.titPars,       2, 0, 1, 3)
        grid.addWidget(self.cbxSave,       2, 4)
        grid.addWidget(self.butRead,       3, 1)
        grid.addWidget(self.butWrite,      3, 2)
        grid.addWidget(self.butDefault,    3, 3)
        grid.addWidget(self.butPrint,      3, 4)
        #self.setLayout(grid)

        self.vbox = QtWidgets.QVBoxLayout() 
        self.vbox.addLayout(grid)
        self.vbox.addStretch(1)
        self.setLayout(self.vbox)

        self.ediFile.editingFinished .connect(self.onEditFile)
        self.butRead.clicked.connect(self.onRead)
        self.butWrite.clicked.connect(self.onSave)
        self.butPrint.clicked.connect(self.onPrint)
        self.butDefault.clicked.connect(self.onDefault)
        self.butFile.clicked.connect(self.onFile)
        self.cbxSave.stateChanged[int].connect(self.onCbxSave)
 
        self.showToolTips()
        self.setStyle()


    def showToolTips(self):
        # Tips for buttons and fields:
        #self           .setToolTip('This GUI deals with the configuration parameters.')
        self.ediFile   .setToolTip('Type the file path name here,\nor better use "Browse" button.')
        self.butFile   .setToolTip('Select the file path name\nto read/write the configuration parameters.')
        self.butRead   .setToolTip('Read the configuration parameters from file.')
        self.butWrite  .setToolTip('Save (write) the configuration parameters in file.')
        self.butDefault.setToolTip('Reset the configuration parameters\nto their default values.')
        self.butPrint  .setToolTip('Print current values of the configuration parameters.')


    def setStyle(self):
        self.setMinimumSize(500,150)
        self.setMaximumSize(700,150)
        #width = 80
        #self.butFile .setFixedWidth(width)
        #self.edi_kin_win_size   .setAlignment(QtCore.Qt.AlignRight)

        self           .setStyleSheet(cp.styleBkgd)
        self.titFile   .setStyleSheet(cp.styleLabel)
        self.titPars   .setStyleSheet(cp.styleLabel)
        self.ediFile   .setStyleSheet(cp.styleEdit) 

        self.butFile   .setStyleSheet(cp.styleButton) 
        self.butRead   .setStyleSheet(cp.styleButton)
        self.butWrite  .setStyleSheet(cp.styleButton)
        self.butDefault.setStyleSheet(cp.styleButton)
        self.butPrint  .setStyleSheet(cp.styleButton)
        self.cbxSave   .setStyleSheet(cp.styleLabel)
        #self.butClose  .setStyleSheet(cp.styleButtonClose)

        self.butFile   .setFixedWidth(50)

 
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
        #try    : del cp.guiconfigparameters 
        #except : pass


    def onClose(self):
        logger.debug('onClose', __name__)
        self.close()


    def onRead(self):
        logger.debug('onRead', __name__)
        cp.readParametersFromFile( self.getFileNameFromEditField() )
        self.ediFile.setText( cp.fname_cp )
        #self.parent.ediFile.setText( cp.fname_cp )
        #self.refreshGUIWhatToDisplay()


    def onWrite(self):
        fname = self.getFileNameFromEditField()
        logger.info('onWrite - save all configuration parameters in file: ' + fname, __name__)
        cp.saveParametersInFile( fname )


    def onSave(self):
        fname = cp.fname_cp
        logger.info('onSave - save all configuration parameters in file: ' + fname, __name__)
        cp.saveParametersInFile( fname )


    def onDefault(self):
        logger.info('onDefault - Set default values of configuration parameters.', __name__)
        cp.setDefaultValues()
        self.ediFile.setText( cp.fname_cp )
        #self.refreshGUIWhatToDisplay()


    def onPrint(self):
        logger.info('onPrint', __name__)
        cp.printParameters()


    def onFile(self):
        logger.debug('onFile', __name__)
        self.path = self.getFileNameFromEditField()
        self.dname,self.fname = os.path.split(self.path)
        logger.info('dname : %s' % (self.dname), __name__)
        logger.info('fname : %s' % (self.fname), __name__)
        self.path = str( QtWidgets.QFileDialog.getOpenFileName(self,'Open file',self.dname) )[0]
        self.dname,self.fname = os.path.split(self.path)

        if self.dname == '' or self.fname == '' :
            logger.info('Input directiry name or file name is empty... use default values', __name__)
        else :
            self.ediFile.setText(self.path)
            cp.fname_cp = self.path


    def onEditFile(self):
        logger.debug('onEditFile', __name__)
        self.path = self.getFileNameFromEditField()
        #cp.fname_cp.setValue(self.path)
        cp.fname_cp = self.path
        dname,fname = os.path.split(self.path)
        logger.info('Set dname : %s' % (dname), __name__)
        logger.info('Set fname : %s' % (fname), __name__)


    def getFileNameFromEditField(self):
        return str(self.ediFile.displayText())


    def onCbxSave(self):
        #if self.cbx.hasFocus() :
        par = cp.save_cp_at_exit
        cbx = self.cbxSave
        tit = cbx.text()

        par.setValue(cbx.isChecked())
        msg = 'check box ' + tit  + ' is set to: ' + str(par.value())
        logger.info(msg, __name__)


#------------------------------

if __name__ == "__main__" :
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = GUIConfigFile()
    widget.show()
    app.exec_()

#------------------------------
