#!/usr/bin/env python
#--------------------------------------------------------------------------
"""Renders the main GUI for the :py:class:`CalibManager`

This software was developed for the SIT project.  
If you use all or part of it, please give an appropriate acknowledgment.

Author Mikhail Dubrovin
"""
from __future__ import print_function
from __future__ import absolute_import

#------------------------------

import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
import time   # for sleep(sec)

from CalibManager.ConfigParametersForApp import cp
from CalibManager.Logger                 import logger
from CalibManager.GUILogger              import GUILogger
from CalibManager.GUIMainTabs            import GUIMainTabs
from CalibManager.GUIInsExpDirDet        import *
from CalibManager.PackageVersions        import PackageVersions

#------------------------------

class GUIMain(QtWidgets.QWidget) :
    """Main GUI for calibration management project.
    """
    def __init__(self, parent=None, app=None, **dict_opts) :

        self.name = 'GUIMain'
        self.myapp = app
        QtWidgets.QWidget.__init__(self, parent)

        self.log_rec_on_start()

        cp.setIcons()

        cp.package_versions = PackageVersions()

        self.main_win_width  = cp.main_win_width 
        self.main_win_height = cp.main_win_height
        self.main_win_pos_x  = cp.main_win_pos_x 
        self.main_win_pos_y  = cp.main_win_pos_y   

        self.setGeometry(self.main_win_pos_x .value(), \
                         self.main_win_pos_y .value(), \
                         self.main_win_width .value(), \
                         self.main_win_height.value())

        self.setWindowTitle('Calibration Manager')
        self.setWindowIcon(cp.icon_monitor)
        self.palette = QtGui.QPalette()
        self.resetColorIsSet = False

        self.setOptionalPars(dict_opts)

        #self.guitree  = GUICalibDirTree()
        self.guitabs   = GUIMainTabs(self) # QtWidgets.QTextEdit()
        self.guilogger = GUILogger(show_buttons=False)
        self.guiinsexpdirdet = GUIInsExpDirDet(self)

        self.vsplit = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.vsplit.addWidget(self.guitabs)
        self.vsplit.addWidget(self.guilogger)
        #self.vsplit.moveSplitter(0,200)

        self.vbox = QtWidgets.QVBoxLayout() 
        #self.vbox.addWidget(self.guibuttonbar)
        self.vbox.addWidget(self.guiinsexpdirdet)
        #self.vbox.addLayout(self.hboxB) 
        #self.vbox.addStretch(1)
        self.vbox.addWidget(self.vsplit) 

        self.setLayout(self.vbox)

        self.showToolTips()
        self.setStyle()

        gu.create_directory(cp.dir_work.value())

        #self.move(10,25)
        self.move(self.main_win_pos_x.value(), self.main_win_pos_y.value())
        cp.guimain = self

        # Saves the 1st version of the log file right on start
        # in order to track down what is going on with open app.
        self.save_log_file(verb=False)

        #print 'End of init'


    def setOptionalPars(self, opts):

        is_default = True

        if opts['runnum'] is not None :
            rnum = opts['runnum']
            str_run_number = '%04d' % rnum
            cp.str_run_number.setValue(str_run_number)
            cp.dark_list_run_min.setValue(rnum)
            cp.dark_list_run_max.setValue(rnum+10)
            is_default = False
    
        if opts['exp'] is not None :
            cp.exp_name.setValue(opts['exp'])
            instr_name  = opts['exp'][:3]
            cp.instr_name.setValue(instr_name)
            cp.calib_dir.setValue(fnm.path_to_calib_dir_default())
            is_default = False
    
        if opts['detector'] is not None :
            det_name = opts['detector'].replace(","," ")

            list_of_dets_sel = det_name.split()
            list_of_dets_sel_lower = [det.lower() for det in list_of_dets_sel]

            #msg = self.sep + 'List of detectors:'
            for det, par in zip(cp.list_of_dets_lower, cp.det_cbx_states_list) :
                par.setValue(det in list_of_dets_sel_lower)
                #msg += '\n%s %s' % (det.ljust(10), par.value())
            #self.log(msg,1)
            is_default = False

        if opts['calibdir'] is not None :
            cdir = opts['calibdir']
            if os.path.exists(cdir) : cp.calib_dir.setValue(cdir)
            is_default = False


        if not is_default :
   	    #print 'dict_opts', opts
            print('Optional parameters',\
                  '\n  instr_name : %s' % cp.instr_name.value(),\
                  '\n  exp_name   : %s' % cp.exp_name.value(),\
                  '\n  calib_dir  : %s' % cp.calib_dir.value(),\
                  '\n  run_number : %s' % cp.str_run_number.value(),\
                  '\n  detectors  : %s' % opts['detector'])

 
    def printStyleInfo(self):
        qstyle     = self.style()
        qpalette   = qstyle.standardPalette()
        qcolor_bkg = qpalette.color(1)
        #r,g,b,alp  = qcolor_bkg.getRgb()
        msg = 'Background color: r,g,b,alpha = %d,%d,%d,%d' % ( qcolor_bkg.getRgb() )
        logger.debug(msg)


    def showToolTips(self):
        pass
        #self.butStop.setToolTip('Not implemented yet...')


    def setStyle(self):
        self.setMinimumSize(800,700)
        self.layout().setContentsMargins(0,0,0,0)

        #self.vsplit.setMinimumHeight(700)
        
        #self.        setStyleSheet(cp.styleBkgd)
        #self.butSave.setStyleSheet(cp.styleButton)
        #self.butExit.setStyleSheet(cp.styleButton)
        #self.butELog.setStyleSheet(cp.styleButton)
        #self.butFile.setStyleSheet(cp.styleButton)

        #self.butELog    .setVisible(False)
        #self.butFBrowser.setVisible(False)

        #self.butSave.setText('')
        #self.butExit.setText('')
        #self.butExit.setFlat(True)

        #self.vsplit.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Ignored)


    #def resizeEvent(self, e):
         #logger.debug('resizeEvent', self.name) 
         #print 'GUIMain resizeEvent: %s' % str(self.size())
         #pass


    #def moveEvent(self, e):
        #logger.debug('moveEvent', self.name) 
        #self.position = self.mapToGlobal(self.pos())
        #self.position = self.pos()
        #logger.debug('moveEvent - pos:' + str(self.position), __name__)       
        #print 'Move window to x,y: ', str(self.mapToGlobal(QtCore.QPoint(0,0)))
        #pass


    def closeEvent(self, event):
        logger.info('closeEvent', self.name)

        try    : self.guiinsexpdirdet.close() 
        except : pass
        
        try    : self.guitabs.close()
        except : pass
        
        try    : cp.guilogger.close()
        except : pass

        try    : cp.plotimgspe.close()
        except : pass

        try    : cp.guifilebrowser.close()
        except : pass

        self.onSave()


    def onSave(self):

        point, size = self.mapToGlobal(QtCore.QPoint(-5,-22)), self.size() # Offset (-5,-22) for frame size.
        x,y,w,h = point.x(), point.y(), size.width(), size.height()
        msg = 'Save main window x,y,w,h : %d, %d, %d, %d' % (x,y,w,h)
        logger.info(msg, self.name)
        #print msg

        #Save main window position and size
        self.main_win_pos_x .setValue(x)
        self.main_win_pos_y .setValue(y)
        self.main_win_width .setValue(w)
        self.main_win_height.setValue(h)

        #self.add_record_in_db()

        cp.close()

        if cp.save_log_at_exit.value() :
            logger.saveLogInFile(fnm.log_file())

            self.save_log_file(verb=True)

            #logger.saveLogTotalInFile( fnm.log_file_total() )


    def save_log_file(self, verb=True):
        path = fnm.log_file_cpo()
        if gu.create_path(path) :
            logger.saveLogInFile(path)
            if verb : print('Log file: %s' % path)
        else : logger.warning('onSave: path for log file %s was not created.' % path, self.name)


    def log_rec_on_start(self) :
        import CalibManager.GlobalUtils as gu
        msg = 'user: %s@%s  cwd: %s\n    command: %s'%\
              (gu.get_login(), gu.get_hostname(), gu.get_cwd(), ' '.join(sys.argv))
        logger.info(msg, self.name)


    def add_record_in_db(self):
        from .NotificationDB import NotificationDB
        try :
            ndb = NotificationDB()
            ndb.add_record()
        except :
            pass

#------------------------------
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
    app = QtWidgets.QApplication(sys.argv)
    ex  = GUIMain()
    ex.show()
    app.exec_()

#------------------------------
