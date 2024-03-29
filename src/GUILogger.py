#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#   GUILogger
#------------------------------------------------------------------------

"""GUILogger - GUI for logger

This software was developed for the SIT project.  If you use all or 
part of it, please give an appropriate acknowledgment.

@see RelatedModule

@version $Id$

@author Mikhail S. Dubrovin
"""
from __future__ import absolute_import

#--------------------------------
__version__ = "$Revision$"
#--------------------------------

import os

from .ConfigParametersForApp import cp
from CalibManager.Logger import logger
from PyQt5 import QtCore, QtGui, QtWidgets

#------------------------------

class GUILogger(QtWidgets.QWidget) :
    """GUI for Logger"""

    name = 'GUILogger'

    def __init__(self, parent=None, show_buttons=True) :

        QtWidgets.QWidget.__init__(self, parent)

        self.show_buttons = show_buttons
        
        self.setGeometry(200, 400, 500, 400)
        self.setWindowTitle('GUI Logger')
        #self.setWindowIcon(cp.icon_logger)

        self.box_txt    = QtWidgets.QTextEdit()
 
        #self.tit_title = QtGui.QLabel('Logger')
        self.tit_status = QtWidgets.QLabel('Status:')
        self.tit_level  = QtWidgets.QLabel('Verbosity level:')
        self.but_close  = QtWidgets.QPushButton('&Close') 
        self.but_save   = QtWidgets.QPushButton('&Save log-file') 

        self.list_of_levels = logger.getListOfLevels()
        self.box_level      = QtWidgets.QComboBox(self) 
        self.box_level.addItems(self.list_of_levels)
        self.box_level.setCurrentIndex(self.list_of_levels.index(cp.log_level.value()))
        
        self.hboxM = QtWidgets.QHBoxLayout()
        self.hboxM.addWidget(self.box_txt)

        self.hboxB = QtWidgets.QHBoxLayout()
        self.hboxB.addWidget(self.tit_status)
        self.hboxB.addStretch(4)     
        self.hboxB.addWidget(self.tit_level)
        self.hboxB.addWidget(self.box_level)
        self.hboxB.addStretch(1)     
        self.hboxB.addWidget(self.but_save)
        self.hboxB.addWidget(self.but_close)

        self.vbox  = QtWidgets.QVBoxLayout()
        #self.vbox.addWidget(self.tit_title)
        self.vbox.addLayout(self.hboxM)
        self.vbox.addLayout(self.hboxB)
        self.setLayout(self.vbox)
        
        self.but_close.clicked.connect(self.onClose)
        self.but_save.clicked.connect(self.onSave)
        self.box_level.currentIndexChanged[int].connect(self.onBox)
 
        self.startGUILog()

        self.showToolTips()
        self.setStyle()

        self.guilogger = self


    def showToolTips(self):
        #self           .setToolTip('This GUI is for browsing log messages')
        self.box_txt    .setToolTip('Window for log messages')
        self.but_close  .setToolTip('Close this window')
        self.but_save   .setToolTip('Save current content of the GUI Logger\nin work directory file: '+os.path.basename(self.fname_log))
        self.tit_status .setToolTip('The file name, where this log \nwill be saved at the end of session')
        self.box_level  .setToolTip('Click on this button and \nselect the level of messages \nwhich will be displayed')


    def setStyle(self):
        self.           setStyleSheet(cp.styleBkgd)
        #self.tit_title.setStyleSheet(cp.styleTitleBold)
        self.tit_status.setStyleSheet(cp.styleTitle)
        self.tit_level .setStyleSheet(cp.styleTitle)
        self.but_close .setStyleSheet(cp.styleButton)
        self.but_save  .setStyleSheet(cp.styleButton) 
        self.box_level .setStyleSheet(cp.styleButton) 
        self.box_txt   .setReadOnly(True)
        self.box_txt   .setStyleSheet(cp.styleWhiteFixed) 
        #self.box_txt   .ensureCursorVisible()
        #self.tit_title.setAlignment(QtCore.Qt.AlignCenter)
        #self.titTitle.setBold()

        self.tit_status.setVisible(self.show_buttons)
        self.tit_level .setVisible(self.show_buttons)
        self.box_level .setVisible(self.show_buttons)
        self.but_save  .setVisible(self.show_buttons)
        self.but_close .setVisible(self.show_buttons)

        if not self.show_buttons: self.layout().setContentsMargins(0,0,0,0)
        self.setMinimumHeight(50)
        self.setMinimumSize(300,50)
        #self.setBaseSize(500,200)


    def setParent(self,parent) :
        self.parent = parent


    #def resizeEvent(self, e):
        #logger.debug('resizeEvent', self.name) 
        #pass


    #def moveEvent(self, e):
        #logger.debug('moveEvent', self.name) 
        #cp.posGUIMain = (self.pos().x(),self.pos().y())
        #pass


    def closeEvent(self, event):
        logger.info('closeEvent', self.name)
        #self.saveLogTotalInFile() # It will be saved at closing of GUIMain

        #try    : del cp.guilogger # GUILogger
        #except : pass

        #if cp.guilogger is not None :
        #    del cp.guilogger
        #    cp.guilogger = None


    def onClose(self):
        logger.debug('onClose', self.name)
        self.close()


    def onSave(self):
        logger.debug('onSave:', self.name)
        self.saveLogInFile()


    def onBox(self):
        level_selected = self.box_level.currentText()
        cp.log_level.setValue( level_selected ) 
        logger.info('onBox - selected ' + self.tit_level.text() + ' ' + cp.log_level.value(), self.name)
        logger.setLevel(cp.log_level.value())
        self.box_txt.setText( logger.getLogContent() )


    def saveLogInFile(self):
        logger.info('saveLogInFile ' + self.fname_log, self.name)
        path = str(QtWidgets.QFileDialog.getSaveFileName(self,
                                                     caption   = 'Select the file to save log',
                                                     directory = self.fname_log,
                                                     filter    = '*.txt'
                                                     ))[0]
        if path == '' :
            logger.debug('Saving is cancelled.', self.name)
            return 
        logger.info('Output file: ' + path, self.name)
        logger.saveLogInFile(path)
        self.fname_log = path
        cp.log_file.setValue(path)


    def saveLogTotalInFile(self):
        logger.info('saveLogTotalInFile' + self.fname_log_total, self.name)
        logger.saveLogTotalInFile(self.fname_log_total)


    def getConfirmation(self):
        """Pop-up box for confirmation"""
        msg = QtWidgets.QMessageBox(self, windowTitle='Confirm closing!',
            text='You are about to close GUI Logger...\nIf the log-file is not saved it will be lost.',
            standardButtons=QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard | QtWidgets.QMessageBox.Cancel)
        msg.setDefaultButton(msg.Save)

        clicked = msg.exec_()

        if   clicked == QtWidgets.QMessageBox.Save :
            logger.info('Saving is requested', self.name)
        elif clicked == QtWidgets.QMessageBox.Discard :
            logger.info('Discard is requested', self.name)
        else :
            logger.info('Cancel is requested', self.name)
        return clicked


    def onShow(self):
        logger.info('onShow - is not implemented yet...', self.name)


    def startGUILog(self) :
        self.fname_log       = cp.log_file.value()
        #self.fname_log_total = cp.log_file_total.value()
        self.setStatus(0, 'Log-file: ' + os.path.basename(self.fname_log))

        logger.setLevel(cp.log_level.value())
        self.box_txt.setText(logger.getLogContent())
        
        logger.setGUILogger(self)
        logger.debug('GUILogger is open', self.name)
        self.box_txt.moveCursor(QtGui.QTextCursor.End)


    def appendGUILog(self, msg='...'):
        self.box_txt.append(msg)
        self.scrollDown()


    def scrollDown(self):
        #print 'scrollDown'
        #scrol_bar_v = self.box_txt.verticalScrollBar() # QScrollBar
        #scrol_bar_v.setValue(scrol_bar_v.maximum()) 
        self.box_txt.moveCursor(QtGui.QTextCursor.End)
        self.box_txt.repaint()
        #self.raise_()
        #self.box_txt.update()

        
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
    widget = GUILogger ()
    widget.show()
    app.exec_()
    sys.exit (0)

#------------------------------
