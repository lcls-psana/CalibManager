
#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#   GUIButtonBar...
#
#------------------------------------------------------------------------

"""GUIButtonBar.

This software was developed for the SIT project.  If you use all or 
part of it, please give an appropriate acknowledgment.

@version $Id$

@author Mikhail S. Dubrovin
"""
from __future__ import absolute_import

#--------------------------------
__version__ = "$Revision$"
#--------------------------------

import os

from PyQt5 import QtCore, QtGui, QtWidgets

from .ConfigParametersForApp import cp

from .GUILogger            import *
from CalibManager.Logger               import logger
from .FileNameManager      import fnm

#------------------------------

class GUIButtonBar(QtWidgets.QWidget) :
    """Main GUI for main button bar.
    """
    def __init__(self, parent=None, app=None) :

        self.name = 'GUIButtonBar'
        self.myapp = app
        QtWidgets.QWidget.__init__(self, parent)

        cp.setIcons()

        self.setGeometry(10, 25, 650, 30)
        self.setWindowTitle('Calibration Manager')
        self.setWindowIcon(cp.icon_monitor)
        self.palette = QtGui.QPalette()
        self.resetColorIsSet = False
 
        self.butSave     = QtWidgets.QPushButton('Save')
        self.butExit     = QtWidgets.QPushButton('Exit')
        self.butFile     = QtWidgets.QPushButton(u'GUI \u2192 &File')
        self.butELog     = QtWidgets.QPushButton(u'GUI \u2192 &ELog')
        self.butLogger   = QtWidgets.QPushButton('Logger')
        self.butFBrowser = QtWidgets.QPushButton('File Browser')

        self.butELog    .setIcon(cp.icon_mail_forward)
        self.butFile    .setIcon(cp.icon_save)
        self.butExit    .setIcon(cp.icon_exit)
        self.butLogger  .setIcon(cp.icon_logger)
        self.butFBrowser.setIcon(cp.icon_browser)
        self.butSave    .setIcon(cp.icon_save_cfg)
        #self.butStop    .setIcon(cp.icon_stop)

        self.hboxB = QtWidgets.QHBoxLayout() 
        self.hboxB.addWidget(self.butLogger  )
        self.hboxB.addWidget(self.butFBrowser)
        self.hboxB.addWidget(self.butFile    )
        self.hboxB.addWidget(self.butELog    )
        self.hboxB.addStretch(1)     
        self.hboxB.addWidget(self.butSave    )
        self.hboxB.addWidget(self.butExit    )

        self.setLayout(self.hboxB)

        self.butExit.clicked.connect(self.onExit)
        self.butLogger.clicked.connect(self.onLogger)
        self.butSave.clicked.connect(self.onSave)
        self.butFile.clicked.connect(self.onFile)
        #self.connect(self.butELog    ,  QtCore.SIGNAL('clicked()'), self.onELog    )
        #self.connect(self.butFBrowser,  QtCore.SIGNAL('clicked()'), self.onFBrowser)

        self.showToolTips()
        self.setStyle()
        self.printStyleInfo()

        #self.onLogger()
        self.butFBrowser.setStyleSheet(cp.styleButtonBad)

        cp.guibuttonbar = self
        self.move(10,25)
        
        #print 'End of init'
        

    def printStyleInfo(self):
        qstyle     = self.style()
        qpalette   = qstyle.standardPalette()
        qcolor_bkg = qpalette.color(1)
        #r,g,b,alp  = qcolor_bkg.getRgb()
        msg = 'Background color: r,g,b,alpha = %d,%d,%d,%d' % (qcolor_bkg.getRgb())
        logger.debug(msg)


    def showToolTips(self):
        self.butSave.setToolTip('Save all current settings in the \nfile with configuration parameters') 
        self.butExit.setToolTip('Close all windows and \nexit this program') 
        self.butFile.setToolTip('Save current GUI image in PNG file')
        self.butELog.setToolTip('1. Save current GUI image in PNG file\n'\
                                '2. Submit PNG file with msg in ELog')
        self.butLogger.setToolTip('On/Off logger widow')
        self.butFBrowser.setToolTip('On/Off file browser')
        #self.butStop.setToolTip('Not implemented yet...')
        

    def setStyle(self):
        self.        setStyleSheet(cp.styleBkgd)
        self.butSave.setStyleSheet(cp.styleButton)
        self.butExit.setStyleSheet(cp.styleButton)
        self.butELog.setStyleSheet(cp.styleButton)
        self.butFile.setStyleSheet(cp.styleButton)

        self.butELog    .setVisible(False)
        self.butFBrowser.setVisible(False)

        #self.butSave.setText('')
        #self.butExit.setText('')
        #self.butExit.setFlat(True)


    #def resizeEvent(self, e):
        #logger.debug('resizeEvent', self.name) 
        #pass


    #def moveEvent(self, e):
        #logger.debug('moveEvent', self.name) 
        #self.position = self.mapToGlobal(self.pos())
        #self.position = self.pos()
        #logger.debug('moveEvent - pos:' + str(self.position), __name__)       
        #pass


    def closeEvent(self, event):
        logger.debug('closeEvent', self.name)

        try    : cp.guimain.close()
        except : pass

        #try    : del cp.guimain
        #except : pass


    def onExit(self):
        logger.debug('onExit', self.name)
        self.close()

        
    def onPrint(self):
        logger.debug('onPrint', self.name)
        

    def onFile(self):
        logger.debug('onFile', self.name)
        path  = fnm.path_gui_image()
        #dir, fname = os.path.split(path)
        path  = str(QtWidgets.QFileDialog.getSaveFileName(self,
                                                      caption='Select file to save the GUI',
                                                      directory = path,
                                                      filter = '*.png'
                                                      ))[0]
        if path == '' :
            logger.debug('Saving is cancelled.', self.name)
            return
        logger.info('Save GUI image in file: ' + path, self.name)
        pixmap = QtGui.QPixmap.grabWidget(self)
        status = pixmap.save(path, 'PNG')
        #logger.info('Save status: '+str(status), self.name)


    def onELog(self):
        logger.debug('onELog', self.name)
        pixmap = QtGui.QPixmap.grabWidget(self)
        fname  = fnm.path_gui_image()
        status = pixmap.save(fname, 'PNG')
        logger.info('1. Save GUI image in file: ' + fname + ' status: '+str(status), self.name)
        if not status : return
        logger.info('2. Send GUI image in ELog: ', fname)
        wdialog = GUIELogPostingDialog (self, fname=fname)
        resp=wdialog.exec_()
  

    def onSave(self):
        logger.debug('onSave', self.name)
        cp.saveParametersInFile( cp.fname_cp )
        #cp.saveParametersInFile( cp.fname_cp.value() )


    def onLogger(self):       
        logger.debug('onLogger', self.name)
        try    :
            cp.guilogger.close()
            del cp.guilogger
        except :
            self.butLogger.setStyleSheet(cp.styleButtonGood)
            cp.guilogger = GUILogger()
            cp.guilogger.move(self.pos().__add__(QtCore.QPoint(860,00))) # open window with offset w.r.t. parent
            cp.guilogger.show()


    def onFBrowser(self):       
        logger.debug('onFBrowser', self.name)
        try    :
            cp.guifilebrowser.close()
        except :
            self.butFBrowser.setStyleSheet(cp.styleButtonGood)
            cp.guifilebrowser = GUIFileBrowser(None, fnm.get_list_of_files_total())
            cp.guifilebrowser.move(self.pos().__add__(QtCore.QPoint(880,40))) # open window with offset w.r.t. parent
            cp.guifilebrowser.show()

    def onStop(self):       
        logger.debug('onStop - not implemented yet...', self.name)

#------------------------------

    #def mousePressEvent(self, event):
    #    print 'event.x, event.y, event.button =', str(event.x()), str(event.y()), str(event.button())         

    #def mouseReleaseEvent(self, event):
    #    print 'event.x, event.y, event.button =', str(event.x()), str(event.y()), str(event.button())                

#http://doc.qt.nokia.com/4.6/qt.html#Key-enum
    def keyPressEvent(self, event):
        #print 'event.key() = %s' % (event.key())
        if event.key() == QtCore.Qt.Key_Escape:
            #self.close()
            self.SHowIsOn = False    
            pass

        if event.key() == QtCore.Qt.Key_B:
            #print 'event.key() = %s' % (QtCore.Qt.Key_B)
            pass

        if event.key() == QtCore.Qt.Key_Return:
            #print 'event.key() = Return'
            pass

        if event.key() == QtCore.Qt.Key_Home:
            #print 'event.key() = Home'
            pass

#------------------------------

if __name__ == "__main__" :
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ex  = GUIButtonBar()
    ex.show()
    app.exec_()

#------------------------------
