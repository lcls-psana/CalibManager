from __future__ import absolute_import
#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#------------------------------------------------------------------------

#--------------------------------
__version__ = "$Revision$"
#--------------------------------
#import os

from PyQt5 import QtCore, QtGui, QtWidgets

from .ConfigParametersForApp import cp
from .GUIConfigPars          import GUIConfigPars
from .GUIConfigFile          import GUIConfigFile
from CalibManager.Logger                 import logger

#------------------------------

class GUIConfig(QtWidgets.QWidget) :
    """GUI with tabs for configuration management"""

    def __init__(self, parent=None) :
        QtWidgets.QWidget.__init__(self, parent)
        self.setGeometry(1, 1, 600, 200)
        self.setWindowTitle('Files')

        self.lab_title  = QtWidgets.QLabel     ('Configuration settings')
        self.lab_status = QtWidgets.QLabel     ('Status: ')
        self.but_close  = QtWidgets.QPushButton('&Close') 
        self.but_save   = QtWidgets.QPushButton('&Save') 
        self.but_show   = QtWidgets.QPushButton('Show &Image') 

        self.hboxW = QtWidgets.QHBoxLayout()
        self.hboxB = QtWidgets.QHBoxLayout()
        self.hboxB.addWidget(self.lab_status)
        self.hboxB.addStretch(1)     
        self.hboxB.addWidget(self.but_close)
        self.hboxB.addWidget(self.but_save)
        self.hboxB.addWidget(self.but_show )

        self.list_file_types = [ 'Parameters'
                                ,'Configuration File'
                               ]
        self.makeTabBar()
        self.guiSelector()

        self.vbox = QtWidgets.QVBoxLayout()   
        #cp.guiworkresdirs = GUIWorkResDirs()
        #self.vbox.addWidget(cp.guiworkresdirs)
        self.vbox.addWidget(self.lab_title)
        self.vbox.addWidget(self.tab_bar)
        self.vbox.addLayout(self.hboxW)
        self.vbox.addStretch(1)     
        self.vbox.addLayout(self.hboxB)
        self.setLayout(self.vbox)

        self.but_close.clicked.connect(self.onClose)
        self.but_save.clicked.connect(self.onSave)
        self.but_show.clicked.connect(self.onShow)

        self.showToolTips()
        self.setStyle()


    def showToolTips(self):
        #msg = 'Edit field'
        self.but_close .setToolTip('Close this window.')
        self.but_save  .setToolTip('Save all current configuration parameters.')
        self.but_show  .setToolTip('Show ...')


    def setStyle(self):
        self.          setStyleSheet (cp.styleBkgd)
        self.but_close.setStyleSheet (cp.styleButton)
        self.but_save .setStyleSheet (cp.styleButton)
        self.but_show .setStyleSheet (cp.styleButton)

        self.lab_title.setStyleSheet (cp.styleTitleBold)
        self.lab_title.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_title.setVisible(False)

        self.setMinimumSize(600,360)

        #self.lab_status.setVisible(False)
        self.but_close .setVisible(False)
        self.but_save  .setVisible(False)
        self.but_show  .setVisible(False)


    def makeTabBar(self,mode=None) :
        #if mode is not None : self.tab_bar.close()
        self.tab_bar = QtWidgets.QTabBar()

        #Uses self.list_file_types
        self.ind_tab_0 = self.tab_bar.addTab( self.list_file_types[0] )
        self.ind_tab_1 = self.tab_bar.addTab( self.list_file_types[1] )

        self.tab_bar.setTabTextColor(self.ind_tab_0, QtGui.QColor('magenta'))
        self.tab_bar.setTabTextColor(self.ind_tab_1, QtGui.QColor('magenta'))
        self.tab_bar.setShape(QtWidgets.QTabBar.RoundedNorth)

        #self.tab_bar.setTabEnabled(1, False)
        #self.tab_bar.setTabEnabled(2, False)
        #self.tab_bar.setTabEnabled(3, False)
        #self.tab_bar.setTabEnabled(4, False)
        
        try    :
            tab_index = self.list_file_types.index(cp.current_config_tab.value())
        except :
            tab_index = 3
            cp.current_config_tab.setValue(self.list_file_types[tab_index])
        self.tab_bar.setCurrentIndex(tab_index)

        logger.debug(' make_tab_bar - set mode: ' + cp.current_config_tab.value(), __name__)

        self.tab_bar.currentChanged[int].connect(self.onTabBar)


    def guiSelector(self):

        try    : self.gui_win.close()
        except : pass

        try    : del self.gui_win
        except : pass

        if cp.current_config_tab.value() == self.list_file_types[0] :
            self.gui_win = GUIConfigPars(self)
            self.setStatus(0, 'Status: setting of configuration parameters')
            self.gui_win.setFixedHeight(280)
            
        if cp.current_config_tab.value() == self.list_file_types[1] :
            self.gui_win = GUIConfigFile(self)
            self.setStatus(0, 'Status: operations with configuration file')
            self.gui_win.setFixedHeight(170)

        #self.gui_win.setFixedHeight(180)
        #self.gui_win.setFixedHeight(600)
        self.hboxW.addWidget(self.gui_win)
        self.gui_win.setVisible(True)


    def onTabBar(self):
        tab_ind  = self.tab_bar.currentIndex()
        tab_name = str(self.tab_bar.tabText(tab_ind))
        cp.current_config_tab.setValue( tab_name )
        logger.info(' ---> selected tab: ' + str(tab_ind) + ' - open GUI to work with: ' + tab_name, __name__)
        self.guiSelector()


    def setParent(self,parent) :
        self.parent = parent


    #def resizeEvent(self, e):
        #logger.debug('resizeEvent', __name__) 
        #print __name__ + ' config: self.size():', self.size()
        #self.setMinimumSize( self.size().width(), self.size().height()-40 )
        #pass


    #def moveEvent(self, e):
        #logger.debug('moveEvent', __name__) 
        #self.position = self.mapToGlobal(self.pos())
        #self.position = self.pos()
        #logger.debug('moveEvent: new pos:' + str(self.position), __name__)
        #pass


    def closeEvent(self, event):
        logger.debug('closeEvent', __name__)

        try    : cp.guimain.butFiles.setStyleSheet(cp.styleButton)
        except : pass

        try    : self.gui_win.close()
        except : pass

        try    : self.tab_bar.close()
        except : pass
        
        try    : del cp.guifiles # GUIConfig
        except : pass # silently ignore


    def onClose(self):
        logger.debug('onClose', __name__)
        self.close()


    def onSave(self):
        logger.debug('onSave', __name__)
        cp.saveParametersInFile( cp.fname_cp.value() )


    def onShow(self):
        logger.debug('onShow - is not implemented yet...', __name__)


    def setStatus(self, status_index=0, msg=''):
        list_of_states = ['Good','Warning','Alarm']
        if status_index == 0 : self.lab_status.setStyleSheet(cp.styleStatusGood)
        if status_index == 1 : self.lab_status.setStyleSheet(cp.styleStatusWarning)
        if status_index == 2 : self.lab_status.setStyleSheet(cp.styleStatusAlarm)

        #self.lab_status.setText('Status: ' + list_of_states[status_index] + msg)
        self.lab_status.setText(msg)

#-----------------------------

if __name__ == "__main__" :
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = GUIConfig ()
    widget.show()
    app.exec_()

#-----------------------------
