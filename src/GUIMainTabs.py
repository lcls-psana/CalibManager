#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#------------------------------------------------------------------------

"""GUI for tabs.

This software was developed for the SIT project.  If you use all or 
part of it, please give an appropriate acknowledgment.

@version $Id$

@author Mikhail S. Dubrovin
"""
from __future__ import absolute_import

#--------------------------------
__version__ = "$Revision$"
#--------------------------------

#import os

from PyQt5 import QtCore, QtGui, QtWidgets

from .ConfigParametersForApp import cp

#from GUILogger            import *
#from FileNameManager      import fnm
from CalibManager.Logger               import logger
from .GUIConfig            import * # GUIConfig
from .GUIDark              import GUIDark
from .GUIData              import GUIData
from .GUIROIMask           import GUIROIMask
from .GUIFileManager       import GUIFileManager
from .GUIGeometry          import GUIGeometry
from . import GlobalUtils        as     gu

#---------------------
class GUIMainTabs(QtWidgets.QWidget) :
    """GUI for tabs support in GUIMain.
    """
    list_of_tabs = [ 'Dark'
                    ,'ROI'
                    ,'Geometry'
                    ,'File Manager'
                    ,'Configuration'
                    ]
                    #,'Data'
                    #,'Gain'

    orientation = 'H'
    #orientation = 'V'

    def __init__(self, parent=None, app=None) :

        self.name = 'GUIMainTabs'
        self.myapp = app
        QtWidgets.QWidget.__init__(self, parent)

        cp.setIcons()
 
        self.setGeometry(10, 25, 400, 600)
        self.setWindowTitle('Calibration Manager')
        self.setWindowIcon(cp.icon_monitor)
        self.palette = QtGui.QPalette()
        self.resetColorIsSet = False

        self.gui_win = None

        self.hboxW = QtWidgets.QHBoxLayout()

        self.makeTabBar()
        self.guiSelector()

        if self.orientation == 'H' : self.box = QtWidgets.QVBoxLayout(self) 
        else :                       self.box = QtWidgets.QHBoxLayout(self) 

        self.box.addWidget(self.tab_bar)
        self.box.addLayout(self.hboxW)
        #self.box.addStretch(1)

        self.setLayout(self.box)

        self.showToolTips()
        self.setStyle()
        gu.printStyleInfo(self)

        cp.guitabs = self
        self.move(10,25)
        
        #print 'End of init'
        
    #-------------------

    def showToolTips(self):
        pass
        #self.butExit.setToolTip('Close all windows and \nexit this program') 


    def setStyle(self):
        self.setMinimumHeight(250)
        #self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.layout().setContentsMargins(0,0,0,0)
 

    def makeTabBar(self,mode=None) :
        #if mode is not None : self.tab_bar.close()
        self.tab_bar = QtWidgets.QTabBar()

        #len(self.list_of_tabs)
        for tab_name in self.list_of_tabs :
            #===============================
            #if tab_name == 'Data' : continue # DO NOT ADD THIS TAB
            #===============================
            tab_ind = self.tab_bar.addTab(tab_name)
            self.tab_bar.setTabTextColor(tab_ind, QtGui.QColor('blue')) #gray, red, grayblue

        if self.orientation == 'H' :
            self.tab_bar.setShape(QtWidgets.QTabBar.RoundedNorth)
        else :
            self.tab_bar.setShape(QtWidgets.QTabBar.RoundedWest)

        self.setTabByName(cp.current_tab.value())
            
        self.tab_bar.currentChanged[int].connect(self.onTabBar)


    def setTabByName(self, tab_name) :
        try    :
            tab_index = self.list_of_tabs.index(tab_name)
        except :
            tab_index = 0
            cp.current_tab.setValue(self.list_of_tabs[tab_index])
        logger.info(' makeTabBarr - set tab: %s' % tab_name, __name__)
        self.tab_bar.setCurrentIndex(tab_index)


    def guiSelector(self):

        try    : self.gui_win.close()
        except : pass

        try    : del self.gui_win
        except : pass

        self.gui_win = None

        if   cp.current_tab.value() == self.list_of_tabs[0] :
            self.gui_win = GUIDark(self)
            #self.gui_win = GUIFiles(self)
            #self.setStatus(0, 'Status: processing for pedestals')
            
        elif cp.current_tab.value() == self.list_of_tabs[1] :
            self.gui_win = GUIROIMask(self)

        elif cp.current_tab.value() == self.list_of_tabs[2] :
            self.gui_win = GUIGeometry(self)

        elif cp.current_tab.value() == self.list_of_tabs[3] :
            self.gui_win = GUIFileManager(self)

        elif cp.current_tab.value() == self.list_of_tabs[4] :
            self.gui_win = GUIConfig(self)

        elif cp.current_tab.value() == self.list_of_tabs[5] :
            self.gui_win = GUIData(self)
            #self.setStatus(0, 'Status: processing for data')

        #elif cp.current_tab.value() == self.list_of_tabs[6] :
        #    self.gui_win = QtGui.QTextEdit('is not implemented yet...') # Gain is not implemented.'

        self.hboxW.addWidget(self.gui_win)
        self.gui_win.setVisible(True)


    def onTabBar(self):
        tab_ind  = self.tab_bar.currentIndex()
        tab_name = str(self.tab_bar.tabText(tab_ind))
        cp.current_tab.setValue(tab_name)
        msg = 'Selected tab: %i - %s' % (tab_ind, tab_name)
        logger.info(msg, __name__)
        self.guiSelector()


    #def resizeEvent(self, e):
        #self.frame.setGeometry(self.rect())
        #logger.debug('resizeEvent', self.name) 


    #def moveEvent(self, e):
        #logger.debug('moveEvent', self.name) 
        #self.position = self.mapToGlobal(self.pos())
        #self.position = self.pos()
        #logger.debug('moveEvent - pos:' + str(self.position), __name__)       
        #pass


    def closeEvent(self, event):
        logger.info('closeEvent', self.name)

        try    : self.gui_win.close()
        except : pass

        #try    : del self.gui_win
        #except : pass


    def onExit(self):
        logger.debug('onExit', self.name)
        self.close()

#-----------------------------

if __name__ == "__main__" :
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ex  = GUIMainTabs()
    ex.move(QtCore.QPoint(50,50))
    ex.show()
    app.exec_()

#-----------------------------
