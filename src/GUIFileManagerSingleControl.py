
"""GUIFileManagerSingleControl - Sub-GUI for GUIFileManagerSingle.

This software was developed for the SIT project.
If you use all or part of it, please give an appropriate acknowledgment.

@author Mikhail S. Dubrovin
"""
from __future__ import absolute_import

import os

from PyQt5 import QtCore, QtGui, QtWidgets

from .ConfigParametersForApp import cp

from CalibManager.Logger import logger
from .FileNameManager import fnm

from . import GlobalUtils as gu
from . import RegDBUtils as ru
from .GUIFileBrowser import *
from .PlotImgSpe     import *
from .FileDeployer   import fd
from .GUIRange       import *


class GUIFileManagerSingleControl(QtWidgets.QWidget) :
    """Main GUI for main button bar."""
    char_expand = cp.char_expand
    #char_expand = '' # down-head triangle

    def __init__(self, parent=None, app=None) :

        self.name = 'GUIFileManagerSingleControl'
        self.myapp = app
        QtWidgets.QWidget.__init__(self, parent)
        #Frame.__init__(self, parent, mlw=1)

        self.setGeometry(10, 25, 630, 120)
        self.setWindowTitle('File Manager Select & Action GUI')
        #self.setWindowIcon(cp.icon_monitor)
        self.palette = QtGui.QPalette()
        self.resetColorIsSet = False

        #cp.setIcons()

        self.path_fm_selected = cp.path_fm_selected
        self.setParams()

        self.guirange  = GUIRange(None, self.str_run_from, self.str_run_to)

        self.lab_src  = QtWidgets.QLabel('for detector')
        self.lab_type = QtWidgets.QLabel('calib type')
        self.but_src  = QtWidgets.QPushButton(self.source_name + self.char_expand)
        self.but_type = QtWidgets.QPushButton(self.calib_type + self.char_expand)

        self.lab_file = QtWidgets.QLabel('File:')
        self.edi_file = QtWidgets.QLineEdit(self.path_fm_selected.value()) # fnm.path_to_calib_dir()
        self.edi_file.setReadOnly(True)

        self.but_move   = QtWidgets.QPushButton('Move')
        self.but_copy   = QtWidgets.QPushButton('Copy')
        self.but_delete = QtWidgets.QPushButton('Delete')
        self.but_view   = QtWidgets.QPushButton('View')
        self.but_plot   = QtWidgets.QPushButton('Plot')
        #self.but_copy  .setIcon(cp.icon_monitor)

        self.but_browse = QtWidgets.QPushButton('Browse')

        self.hboxB = QtWidgets.QHBoxLayout()
        #self.hboxB.addStretch(1)
        self.hboxB.addWidget(self.lab_file)
        self.hboxB.addWidget(self.edi_file)
        self.hboxB.addWidget(self.but_browse)
        self.hboxB.addStretch(1)

        self.hboxD = QtWidgets.QHBoxLayout()
        #self.hboxD.addSpacing(50)
        self.hboxD.addWidget(self.but_view)
        self.hboxD.addWidget(self.but_plot)
        self.hboxD.addWidget(self.but_delete)
        self.hboxD.addStretch(1)

        self.hboxC = QtWidgets.QHBoxLayout()
        #self.hboxC.addStretch(1)
        self.hboxC.addWidget(self.but_move)
        self.hboxC.addWidget(self.but_copy)
        self.hboxC.addWidget(self.lab_src )
        self.hboxC.addWidget(self.but_src )
        self.hboxC.addWidget(self.lab_type)
        self.hboxC.addWidget(self.but_type)
        self.hboxC.addWidget(self.guirange)
        self.hboxC.addStretch(1)


        self.vboxW = QtWidgets.QVBoxLayout()
        self.vboxW.addStretch(1)
        self.vboxW.addLayout(self.hboxB)
        self.vboxW.addLayout(self.hboxD)
        self.vboxW.addLayout(self.hboxC)
        self.vboxW.addStretch(1)

        self.setLayout(self.vboxW)

        self.but_browse.clicked.connect(self.onButBrowse)
        self.but_move.clicked.connect(self.onButMove)
        self.but_copy.clicked.connect(self.onButCopy)
        self.but_view.clicked.connect(self.onButView)
        self.but_plot.clicked.connect(self.onButPlot)
        self.but_delete.clicked.connect(self.onButDelete)
        self.but_src.clicked.connect(self.onButSrc)
        self.but_type.clicked.connect(self.onButType)

        self.showToolTips()
        self.setStyle()

        cp.guifilemanagersinglecontrol = self
        self.move(10,25)

        #print 'End of init'


    def showToolTips(self):
        #pass
        self.edi_file  .setToolTip('Path to the file with image data')
        self.but_browse.setToolTip('Open file browser dialog\nwindow and select the file')
        self.but_src   .setToolTip('Select name of the detector')
        self.but_type  .setToolTip('Select type of calibration parameters')
        self.but_move  .setToolTip('Move selected file')
        self.but_copy  .setToolTip('Copy selected file')
        self.but_view  .setToolTip('Launch file browser')
        self.but_plot  .setToolTip('Launch plot browser')
        self.but_delete.setToolTip('Delete selected file\nDelete  is allowed for\nWORK or CALIB directories only')


    def setStyle(self):
        self.          setStyleSheet(cp.styleBkgd)
        self.but_move  .setStyleSheet(cp.styleButton)
        self.but_copy  .setStyleSheet(cp.styleButton)
        self.but_delete.setStyleSheet(cp.styleButton)
        self.but_view  .setStyleSheet(cp.styleButton)
        self.but_plot  .setStyleSheet(cp.styleButton)

        self.setMinimumSize(630,100)
        self.setFixedHeight(100)
        self.layout().setContentsMargins(2,0,2,0)

        #self.but_copy.setFixedWidth(100)
        #self.but_delete.setFixedWidth(100)
        #self.but_copy.setMinimumHeight(60)

        self.edi_file.setFixedWidth(490)
        self.edi_file.setStyleSheet(cp.styleEditInfo)
        self.edi_file.setEnabled(False)

        self.lab_file  .setStyleSheet(cp.styleLabel)
        self.lab_src   .setStyleSheet(cp.styleLabel)
        self.lab_type  .setStyleSheet(cp.styleLabel)

        self.but_move.setVisible(False)
        #self.butViewwser.setVisible(False)
        #self.butSave.setText('')
        #self.butExit.setText('')
        #self.butExit.setFlat(True)

        self.setStyleButtons()
        #self.setVisible(True)


    def setStyleButtons(self):
        """Set buttons enabled or disabled depending on status of other fields
        """

        file_is_enable = True
        if self.str_path() == '':
            file_is_enable = False
            self.but_browse.setStyleSheet(cp.styleButtonGood)
        else:
            self.but_browse.setStyleSheet(cp.styleButton)

        self.but_view.setEnabled(file_is_enable)
        self.but_plot.setEnabled(file_is_enable)

        #print '\nself.str_path()', self.str_path()
        #print 'fnm.path_dir_work()', fnm.path_dir_work().lstrip('.')

        is_enable_delete = file_is_enable # \
#                           and (self.str_path().find(fnm.path_to_calib_dir()) != -1
#                                or self.str_path().find(fnm.path_dir_work().lstrip('.')) != -1
#                                )
        self.but_delete.setEnabled(is_enable_delete)

        is_enable_copy = file_is_enable \
                         and self.source_name != 'Select' \
                         and self.calib_type != 'Select'
        self.but_move  .setEnabled(is_enable_copy)
        self.but_copy  .setEnabled(is_enable_copy)

        if self.source_name == 'Select': self.but_src .setStyleSheet(cp.stylePink)
        else                           : self.but_src .setStyleSheet(cp.styleButton)
        if self.calib_type  == 'Select': self.but_type.setStyleSheet(cp.stylePink)
        else                           : self.but_type.setStyleSheet(cp.styleButton)

        self.guirange.setFieldsEnable(True)

        #self.setButtonDelete()
        #self.setButtonCopy()


    #def setButtonDelete(self):

    #def setButtonCopy(self):
        #self.but.setVisible(False)
        #self.but.setEnabled(True)


    def setParams(self):
        #if self.path_fm_selected.value() != self.path_fm_selected.value_def():
        #    self.path_fm_selected.setValue(os.path.dirname(self.path_fm_selected.value()))
        self.str_run_from = '0'
        self.str_run_to   = 'end'
        self.source_name  = 'Select'
        self.calib_type   = 'Select'


    def resetFields(self):
        self.setParams()
        self.edi_file.setText(self.path_fm_selected.value())
        self.but_src .setText(self.source_name + self.char_expand)
        self.but_type.setText(self.calib_type + self.char_expand)
        self.setStyleButtons()
        self.guirange.resetFields()


    def resetFieldsOnDelete(self):
        self.path_fm_selected.setValue(os.path.dirname(self.path_fm_selected)) # ''
        self.edi_file.setText(self.path_fm_selected.value())
        self.setStyleButtons()


    #def resizeEvent(self, e):
        #logger.debug('resizeEvent', self.name)
        #print 'GUIFileManagerSingleControl resizeEvent: %s' % str(self.size())
        #pass


    #def moveEvent(self, e):
        #logger.debug('moveEvent', self.name)
        #self.position = self.mapToGlobal(self.pos())
        #self.position = self.pos()
        #logger.debug('moveEvent - pos:' + str(self.position), __name__)
        #pass


    def closeEvent(self, event):
        logger.debug('closeEvent', self.name)

        try   : cp.guifilebrowser.close()
        except: pass

        try   : cp.plotimgspe.close()
        except: pass


    def onExit(self):
        logger.debug('onExit', self.name)
        self.close()


    def onButMove(self):
        #logger.info('onButMove', __name__)
        cmd = 'mv %s %s' % (self.str_path(), self.get_out_path())
        if self.approveCommand(self.but_copy, cmd):
            #os.system(cmd)
            fd.procDeployCommand(cmd, 'single-file-manager')
            self.resetFieldsOnDelete()
            if cp.guistatus is not None: cp.guistatus.updateStatusInfo()


    def onButCopy(self):
        #logger.info('onButCopy', __name__)
        if os.path.basename(self.str_path()) == 'HISTORY':
            logger.warning('File %s copy is NOT allowed' % self.str_path(), __name__)
            return

        cmd = 'cp %s %s' % (self.str_path(), self.get_out_path())
        if self.approveCommand(self.but_copy, cmd):
            #os.system(cmd)
            fd.procDeployCommand(cmd, 'single-file-manager')
            if cp.guistatus is not None: cp.guistatus.updateStatusInfo()


    def onButDelete(self):
        #logger.info('onButDelete', __name__)
        cmd = 'rm %s' % self.str_path()
        if self.approveCommand(self.but_delete, cmd):
            os.system(cmd)
            fd.addHistoryRecordOnDelete(cmd, comment='single-file-manager')
            self.resetFieldsOnDelete()
            if cp.guistatus is not None: cp.guistatus.updateStatusInfo()


    def approveCommand(self, but, cmd):
        msg = 'Approve command:\n' + cmd
        resp = gu.confirm_or_cancel_dialog_box(parent=but, text=msg, title='Please confirm or cancel!')
        if resp:
            logger.info('Approved command:\n' + cmd, __name__)
        return resp


    def selectDirFromPopupMenu(self, dir_current='.'):

        list_of_opts = [  'Use WORK directory'
                         ,'Use CALIB directory'
                         ,'Use CURRENT FILE directory'
                         ,'Use OTHER EXPERIMENT directory'
                         ,'Use ALIGNMENT ARCHIVE'
                         ,'Use ./'
                         ,'Reset'
                         ,'Cancel'
                        ]

        selected = gu.selectFromListInPopupMenu(list_of_opts)
        logger.info('selected option: %s' % selected, __name__)

        if   selected == list_of_opts[0]: return fnm.path_dir_work()
        elif selected == list_of_opts[1]: return fnm.path_to_calib_dir()
        elif selected == list_of_opts[2]: return dir_current
        elif selected == list_of_opts[3]: return os.path.join(fnm.path_to_calib_dir(),'../../')
        elif selected == list_of_opts[4]: return '/reg/g/psdm/detector/alignment/'
        elif selected == list_of_opts[5]: return './'
        elif selected == list_of_opts[6]: return ''
        elif selected == list_of_opts[7]: return None
        else                            : return None


    def getRunRange(self):
        """Interface method returning run range string, for example '123-end' """
        return self.guirange.getRange()


    def get_out_path(self):
        det = self.get_detector_selected()
        if det is None: return
        calib_dir = fnm.path_to_calib_dir()
        calib_type = cp.dict_of_det_calib_types[det]
        fname = '%s.data' % self.getRunRange()
        path = os.path.join(calib_dir, calib_type, self.source_name, self.calib_type, fname)
        return path


    def str_path(self):
        return str(self.edi_file.displayText())


    def onButBrowse(self):
        logger.debug('onButBrowse', __name__)
        path0 = self.selectDirFromPopupMenu(self.str_path())
        logger.debug('selected directory: %s' % path0)
        if path0 is None: return
        if path0 == '':
            path = path0
        else:
            file_filter = 'Files (*.txt *.data *.dat HISTORY)\nAll files (*)'
            path = gu.get_open_fname_through_dialog_box(self, path0, 'Select file', filter=file_filter)
            logger.debug('selected path: %s' % path)
            if path is None or path == '':
                logger.debug('File selection is cancelled...', __name__)
                return

        self.edi_file.setText(path)
        self.path_fm_selected.setValue(path) # .setValue(path)
        logger.debug('Selected file:\n' + path, __name__)

        self.setStyleButtons()


    def get_detector_selected(self):
        lst = cp.list_of_dets_selected()
        len_lst = len(lst)
        msg = '%d detector(s) selected: %s' % (len_lst, str(lst))
        #logger.info(msg, __name__ )

        if len_lst !=1:
            msg += ' Select THE ONE!'
            logger.warning(msg, __name__)
            return None

        return lst[0]


    def onButType(self):
        logger.debug('onButType', __name__)

        det = self.get_detector_selected()
        if det is None: return

        lst = cp.dict_of_det_const_types[det]
        selected = gu.selectFromListInPopupMenu(lst)
        if selected is None: return            # selection is cancelled

        txt = str(selected)
        self.calib_type = txt
        self.but_type.setText(txt + self.char_expand)
        logger.debug('Type selected: ' + txt, __name__)

        self.setStyleButtons()


    def onButSrc(self):
        logger.debug('onButSrc', __name__)

        det = self.get_detector_selected()
        if det is None: return

        try   :
            lst = ru.list_of_sources_for_det(det)
        except:
            lst = cp.dict_of_det_sources[det]

        selected = gu.selectFromListInPopupMenu(lst)

        if selected is None: return            # selection is cancelled

        txt = str(selected)
        self.source_name = txt
        self.but_src.setText( txt + self.char_expand )
        logger.info('Source selected: ' + txt, __name__)

        self.setStyleButtons()


    def onButView(self):
        #self.exportLocalPars()
        logger.debug('onButView', __name__)
        try   :
            cp.guifilebrowser.close()
        except:
            cp.guifilebrowser = GUIFileBrowser(None, [self.str_path()], self.str_path())
            cp.guifilebrowser.move(self.pos().__add__(QtCore.QPoint(880,40))) # open window with offset w.r.t. parent
            cp.guifilebrowser.show()


    def onButPlot(self):
        logger.debug('onButPlot', __name__)
        try:
            cp.plotimgspe.close()
            try   : del cp.plotimgspe
            except: pass

        except:
            ifname = self.str_path()
            ofname = os.path.join(fnm.path_dir_work(),'image.png')
            tit = 'Plot for %s' % os.path.basename(ifname)
            cp.plotimgspe = PlotImgSpe(None, ifname=ifname, ofname=ofname, title=tit, is_expanded=False)
            cp.plotimgspe.move(cp.guimain.pos().__add__(QtCore.QPoint(720,120)))
            cp.plotimgspe.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ex  = GUIFileManagerSingleControl()
    ex.show()
    app.exec_()

# EOS
