#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#   GUIFileBrowser ...
#------------------------------------------------------------------------

"""GUI for File Browser"""
from __future__ import absolute_import

#--------------------------------
__version__ = "$Revision$"
#--------------------------------

import os

from PyQt5 import QtCore, QtGui, QtWidgets

from CalibManager.ConfigParametersForApp import cp
from CalibManager.Logger                 import logger
from CalibManager.FileNameManager        import fnm
import CalibManager.GlobalUtils as gu

#------------------------------

class GUIFileBrowser(QtWidgets.QWidget) :
    """GUI for File Browser"""

    def __init__(self, parent=None, list_of_files=['Empty list'], selected_file=None, is_editable=True) :

        QtWidgets.QWidget.__init__(self, parent)

        self.setGeometry(200, 400, 900, 500)
        self.setWindowTitle('GUI File Browser')
        try : self.setWindowIcon(cp.icon_browser)
        except : pass

        self.box_txt    = QtWidgets.QTextEdit()
 
        self.tit_status = QtWidgets.QLabel('Status:')
        self.tit_file   = QtWidgets.QLabel('File:')
        self.but_brow   = QtWidgets.QPushButton('Browse') 
        self.but_close  = QtWidgets.QPushButton('Close') 
        self.but_save   = QtWidgets.QPushButton('Save As') 

        self.is_editable = is_editable

        self.box_file      = QtWidgets.QComboBox(self) 
        self.setListOfFiles(list_of_files)

        self.hboxM = QtWidgets.QHBoxLayout()
        self.hboxM.addWidget(self.box_txt)

        self.hboxF = QtWidgets.QHBoxLayout()
        self.hboxF.addWidget(self.tit_file)
        self.hboxF.addWidget(self.box_file)
        self.hboxF.addWidget(self.but_brow)

        self.hboxB = QtWidgets.QHBoxLayout()
        self.hboxB.addWidget(self.tit_status)
        self.hboxB.addStretch(4)     
        self.hboxB.addWidget(self.but_save)
        self.hboxB.addWidget(self.but_close)

        self.vbox  = QtWidgets.QVBoxLayout()
        #self.vbox.addWidget(self.tit_title)
        self.vbox.addLayout(self.hboxF)
        self.vbox.addLayout(self.hboxM)
        self.vbox.addLayout(self.hboxB)
        self.setLayout(self.vbox)
        
        self.but_brow.clicked.connect(self.onBrow)
        self.but_save.clicked.connect(self.onSave)
        self.but_close.clicked.connect(self.onClose)
        self.box_file.currentIndexChanged[int].connect(self.onBox)
 
        self.startFileBrowser(selected_file)

        self.showToolTips()
        self.setStyle()

        #self.guifilebrowser = self


    def showToolTips(self):
        #self           .setToolTip('This GUI is intended for run control and monitoring.')
        self.but_close .setToolTip('Close this window.')


    def setStyle(self):
        self.           setStyleSheet(cp.styleBkgd)
        self.tit_status.setStyleSheet(cp.styleTitle)
        self.tit_file  .setStyleSheet(cp.styleTitle)
        self.tit_file  .setFixedWidth(25)
        self.tit_file  .setAlignment (QtCore.Qt.AlignRight)
        self.box_file  .setStyleSheet(cp.styleButton) 
        self.but_brow  .setStyleSheet(cp.styleButton)
        self.but_brow  .setFixedWidth(60)
        self.but_save  .setStyleSheet(cp.styleButton)
        self.but_close .setStyleSheet(cp.styleButton)
        self.box_txt   .setReadOnly  (not self.is_editable)
        self.box_txt   .setStyleSheet(cp.styleWhiteFixed) 
        self.layout().setContentsMargins(0,0,0,0)


    def setListOfFiles(self, list):
        self.list_of_files  = ['Click on this box and select file from pop-up-list']
        self.list_of_files += list
        self.box_file.clear()
        self.box_file.addItems(self.list_of_files)
        #self.box_file.setCurrentIndex( 0 )


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
        #self.saveLogTotalInFile() # It will be saved at closing of GUIMain

        try    : cp.guimain.butFBrowser.setStyleSheet(cp.styleButtonBad)
        except : pass

        try    : cp.guidark.but_browse.setStyleSheet(cp.styleButtonBad)
        except : pass

        self.box_txt.close()

        cp.guifilebrowser = None

        #try    : del cp.guifilebrowser # GUIFileBrowser
        #except : pass


    def onClose(self):
        logger.debug('onClose', __name__)
        self.close()


    def onSave(self):
        logger.debug('onSave', __name__)
        path = gu.get_save_fname_through_dialog_box(self, self.fname, 'Select file to save', filter='*.txt')
        if path is None or path == '' : return
        text = str(self.box_txt.toPlainText())
        logger.info('Save in file:\n'+text, __name__)
        f=open(path,'w')
        f.write( text )
        f.close() 


    def onBrow(self):
        logger.debug('onBrow - select file', __name__)

        path0 ='./'
        if len(self.list_of_files) > 1 : path0 = self.list_of_files[1]

        path = gu.get_open_fname_through_dialog_box(self, path0, 'Select text file for browser', filter='Text files (*.txt *.dat *.data *.cfg *.npy)\nAll files (*)')
        if path is None or path == '' or path == path0 :
            logger.debug('Loading is cancelled...', __name__ )
            return

        logger.info('File selected for browser: %s' % path, __name__)        

        if not path in self.list_of_files :
            self.list_of_files.append(path)
            self.box_txt.setText(gu.load_textfile(path))

            self.setListOfFiles(self.list_of_files[1:])
            self.box_file.setCurrentIndex( len(self.list_of_files)-1 )
            self.setStatus(0, 'Status: browsing selected file')

 
    def onBox(self):
        self.fname = str( self.box_file.currentText() )
        logger.info('onBox - selected file: ' + self.fname, __name__)

        if self.fname == '' : return

        #self.list_of_supported = ['cfg', 'log', 'txt', 'txt-tmp', '', 'dat', 'data']
        self.list_of_supported = ['ALL']
        self.str_of_supported = ''
        for ext in self.list_of_supported : self.str_of_supported += ' ' + ext

        #print 'self.fname = ', self.fname
        #print 'self.list_of_files', self.list_of_files

        if self.list_of_files.index(self.fname) == 0 :
            self.setStatus(0, 'Waiting for file selection...')
            self.box_txt.setText('Click on file-box and select the file from pop-up list...')

        elif os.path.lexists(self.fname) :
            ext = os.path.splitext(self.fname)[1].lstrip('.')

            if ext in self.list_of_supported or self.list_of_supported[0] == 'ALL' :
                self.box_txt.setText(gu.load_textfile(self.fname))
                self.setStatus(0, 'Status: enjoy browsing the selected file...')

            else :
                self.box_txt.setText('Sorry, but this browser supports text files with extensions:' +
                                     self.str_of_supported + '\nTry to select another file...')
                self.setStatus(1, 'Status: ' + ext + '-file is not supported...')

        else :
            self.box_txt.setText( 'Selected file is not avaliable...\nTry to select another file...')
            self.setStatus(2, 'Status: WARNING: FILE IS NOT AVAILABLE!')


    def startFileBrowser(self, selected_file=None) :
        logger.debug('Start the GUIFileBrowser.',__name__)
        self.setStatus(0, 'Waiting for file selection...')

        if selected_file is not None and selected_file in self.list_of_files :
            index = self.list_of_files.index(selected_file)
            self.box_file.setCurrentIndex( index )

        elif len(self.list_of_files) == 2 :
            self.box_file.setCurrentIndex( 1 )
            #self.onBox()      
        else :
            self.box_file.setCurrentIndex( 0 )
        #self.box_txt.setText('Click on file-box and select the file from pop-up list...')


    def appendGUILog(self, msg='...'):
        self.box_txt.append(msg)
        scrol_bar_v = self.box_txt.verticalScrollBar() # QScrollBar
        scrol_bar_v.setValue(scrol_bar_v.maximum()) 

        
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
    widget = GUIFileBrowser ()
    widget.show()
    app.exec_()

#------------------------------
