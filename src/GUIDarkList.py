#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module GUIDarkList ...
#
#------------------------------------------------------------------------

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
from Logger                 import logger
from FileNameManager        import fnm
from GUIDarkListItem         import *
#import GlobalUtils          as     gu

#---------------------
#  Class definition --
#---------------------
#class GUIDarkList ( QtGui.QGroupBox ) :
class GUIDarkList ( QtGui.QWidget ) :
    """GUI for the list of widgers"""

    def __init__ ( self, parent=None ) :

        self.parent = parent

        #self.calib_dir      = cp.calib_dir
        #self.det_name       = cp.det_name

        #QtGui.QGroupBox.__init__(self, 'Runs', parent)
        QtGui.QWidget.__init__(self, parent)

        self.setGeometry(100, 100, 730, 400)
        self.setWindowTitle('List of dark runs')
        #self.setTitle('My status')
        #try : self.setWindowIcon(cp.icon_help)
        #except : pass
        self.setFrame()

        self.list = QtGui.QListWidget(parent=self)

        self.widg_width = 500

        self.size     = QtCore.QSize(self.widg_width,35)
        self.size_ext = QtCore.QSize(self.widg_width,200)

        self.updateList()

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.list)
        self.setLayout(vbox)

        self.list.itemClicked.connect(self.onItemClick)
        self.list.itemDoubleClicked.connect(self.onItemDoubleClick)

        #self.connect(self.list.horizontalHeader(),
        #             QtCore.SIGNAL('sectionClicked (int)'),
        #             self.random_function)
 
        self.showToolTips()
        self.setStyle()

        cp.guidarklist = self

    #-------------------
    #  Public methods --
    #-------------------

    def updateList(self):

        self.list.clear()

        self.list_of_records = []
        self.list_of_runs = fnm.get_list_of_xtc_runs()

        for run in self.list_of_runs :
            #print run
            widg = GUIDarkListItem ( self, str(run) ) # QtGui.QLabel(str(run), self)
            item = QtGui.QListWidgetItem('', self.list)
            #self.list.addItem(item)
            #item.setFlags (  QtCore.Qt.ItemIsEnabled ) #| QtCore.Qt.ItemIsSelectable  | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsTristate)
            #print 'item.flags(): %o' % item.flags()
            #item.setCheckState(0)
            item.setFlags (  QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable  | QtCore.Qt.ItemIsUserCheckable )
            #item.setFlags ( QtCore.Qt.ItemIsEnabled )

            item.setSizeHint(self.size)
            self.list.setItemWidget(item, widg)
            #self.list.setItemSelected(item, True)

            record = run, item, widg
            self.list_of_records.append(record)


    def setFieldsEnabled(self, is_enabled=False):
        for (run, item, widg) in self.list_of_records :
            #print '  run:', run          
            widg.setFieldsEnabled(is_enabled)


    def getRunAndItemForWidget(self, widg_active):
        for (run, item, widg) in self.list_of_records :
            if widg == widg_active :
                return run, item
        return None, None


    def showToolTips(self):
        #self           .setToolTip('This GUI is intended for run control and monitoring.')
        #self.but_close .setToolTip('Close this window.')
        pass

    def setFrame(self):
        self.frame = QtGui.QFrame(self)
        self.frame.setFrameStyle( QtGui.QFrame.Box | QtGui.QFrame.Sunken ) #Box, Panel | Sunken, Raised 
        self.frame.setLineWidth(1)
        self.frame.setMidLineWidth(0)
        self.frame.setGeometry(self.rect())
        self.frame.setVisible(False)


    def setStyle(self):
        self.setMinimumWidth(self.widg_width)
        #self.setFixedHeight(400)
        self.setMinimumHeight(200)
        #self.setBaseSize(600, 400)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        #self.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.           setStyleSheet (cp.styleBkgd)

        #self.list.adjustSize()
        #print 'self.list.size():',  self.list.size()
        #self.setMinimumSize(self.list.size())

        #self.tit_status.setStyleSheet (cp.styleTitle)
        #self.tit_status.setStyleSheet (cp.styleDefault)
        #self.tit_status.setStyleSheet (cp.styleTitleInFrame)
        #self.lab_txt   .setReadOnly   (True)
        #self.lab_txt   .setStyleSheet (cp.styleWhiteFixed) 
        #self.lab_txt   .setStyleSheet (cp.styleBkgd)
        
        self.setContentsMargins (QtCore.QMargins(-9,-9,-9,-9))
        #self.setContentsMargins (QtCore.QMargins(1,10,1,1))


    def resizeEvent(self, e):
        #logger.debug('resizeEvent', __name__) 
        self.frame.setGeometry(self.rect())
        #self.lab_txt.setGeometry(self.contentsRect())
        
    def moveEvent(self, e):
        #logger.debug('moveEvent', __name__) 
        #cp.posGUIMain = (self.pos().x(),self.pos().y())
        pass


    def closeEvent(self, event):
        logger.debug('closeEvent', __name__)
        #self.saveLogTotalInFile() # It will be saved at closing of GUIMain

        #try    : cp.guimain.butLogger.setStyleSheet(cp.styleButtonBad)
        #except : pass

        #self.lab_txt.close()

        #try    : del cp.guidarklist # GUIDarkList
        #except : pass

        for (run, item, widg) in self.list_of_records :
            widg.close()


    def onClose(self):
        logger.debug('onClose', __name__)
        self.close()

        
    def onItemExpand(self, widg):
        run, item = self.getRunAndItemForWidget(widg)
        logger.info('Expand widget for run %s' % run, __name__)
        self.size_ext = QtCore.QSize(self.widg_width, widg.getHeight())
        item.setSizeHint(self.size_ext)


    def onItemShrink(self, widg):
        logger.info('onItemExpand', __name__)
        run, item = self.getRunAndItemForWidget(widg)
        logger.info('Shrink widget for run %s' % run, __name__)
        item.setSizeHint(self.size)


    def onItemClick(self, item):
        logger.info('onItemClick - do nothing...', __name__)
        #print 'onItemClick' # , isChecked: ', str(item.checkState())

        widg = self.list.itemWidget(item)

        if item.sizeHint() == self.size_ext :
            pass
            #widg.onClickShrink()
            #print 'widg.size:', widg.size()
            #item.setSizeHint(self.size)
        else :
            pass
            #widg.onClickExpand()
            #print 'widg.size:', widg.size()

            #self.size_ext = QtCore.QSize(self.widg_width, widg.getHeight())
            #item.setSizeHint(self.size_ext)


    def onItemDoubleClick(self, item):
        logger.info('onItemDoubleClick', __name__)
        #print 'onItemDoubleClick' #, isChecked: ', str(item.checkState())

    
#-----------------------------

if __name__ == "__main__" :

    app = QtGui.QApplication(sys.argv)
    w = GUIDarkList()
    #w.setStatusMessage('Test of GUIDarkList...')
    #w.statusOfDir('./')
    w.show()
    app.exec_()

#-----------------------------
