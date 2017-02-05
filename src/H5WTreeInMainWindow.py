
#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module H5WTreeInMainWindow...
#------------------------------------------------------------------------

"""Shows the HDF5 file tree-structure and allows to select data items

This software was developed for the SIT project.
If you use all or part of it, please give an appropriate acknowledgment.

@version $Id$

@author Mikhail S. Dubrovin
"""
#------------------------------

from CalibManager.H5WTree import *

#------------------------------

class H5WTreeInMainWindow(QtGui.QMainWindow) :
    """Shows the HDF5 file tree-structure and allows to select data items.
    """

    def __init__(self, parent=None, fname='/reg/g/psdm/detector/calib/epix100a/epix100a-test.h5'):
        QtGui.QMainWindow.__init__(self, parent)

        self.fname = fname

        self.list_of_checked_item_names = []
        self.tree_view_is_expanded = False

        icon.set_icons()

        self.icon_folder_open   = icon.icon_folder_open
        self.icon_folder_closed = icon.icon_folder_closed
        self.icon_data          = icon.icon_data
        self.icon_apply         = icon.icon_apply
        self.icon_reset         = icon.icon_reset
        self.icon_retreve       = icon.icon_retreve
        self.icon_exit          = icon.icon_exit
        self.icon_expand        = icon.icon_expand
        self.icon_collapse      = icon.icon_collapse
        self.icon_expcheck      = icon.icon_expcheck
        self.icon_print         = icon.icon_print
        self.icon_expcoll       = icon.icon_expand

        self.actExit         = QtGui.QAction(self.icon_exit,     'Exit',           self)
        self.actApply        = QtGui.QAction(self.icon_apply,    'Apply',          self)
        self.actReset        = QtGui.QAction(self.icon_reset,    'Reset',          self)
        self.actRetreve      = QtGui.QAction(self.icon_retreve,  'Retreve',        self)
        self.actExpand       = QtGui.QAction(self.icon_expand,   'Expand',         self)
        self.actCollapse     = QtGui.QAction(self.icon_collapse, 'Collapse',       self)
        self.actExpColl = QtGui.QAction(self.icon_expcoll,  'Expand tree',    self)
        self.actExpCheck     = QtGui.QAction(self.icon_expcheck, 'Expand checked', self)
        self.actPrint        = QtGui.QAction(self.icon_print,    'Print tree',     self)

        self.h5wtree = H5WTree(self, fname)

        self.connect(self.actExit,     QtCore.SIGNAL('triggered()'), self.h5wtree.processExit)
        self.connect(self.actApply,    QtCore.SIGNAL('triggered()'), self.h5wtree.processApply)
        self.connect(self.actReset,    QtCore.SIGNAL('triggered()'), self.h5wtree.processReset)
        self.connect(self.actRetreve,  QtCore.SIGNAL('triggered()'), self.h5wtree.processRetreve)
        self.connect(self.actExpand,   QtCore.SIGNAL('triggered()'), self.h5wtree.processExpand)
        self.connect(self.actCollapse, QtCore.SIGNAL('triggered()'), self.h5wtree.processCollapse)
        self.connect(self.actExpColl,  QtCore.SIGNAL('triggered()'), self.h5wtree.processExpColl)
        self.connect(self.actExpCheck, QtCore.SIGNAL('triggered()'), self.h5wtree.processExpCheck)
        self.connect(self.actPrint,    QtCore.SIGNAL('triggered()'), self.h5wtree.processPrint)
        #self.connect(self.actExit,     QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        self.menubar = self.menuBar()
        optAct = self.menubar.addMenu('&Actions')
        optAct.addAction(self.actApply)
        optAct.addAction(self.actReset)
        optAct.addAction(self.actRetreve)
        optAct.addAction(self.actExit)

        optView = self.menubar.addMenu('&View')
        optView.addAction(self.actExpand)
        optView.addAction(self.actCollapse)
        optView.addAction(self.actExpCheck)
        optView.addAction(self.actPrint)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.setMovable(True)
        self.toolbar.addAction(self.actExit)
        #self.toolbar.insertSeparator(....)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.actApply)
        self.toolbar.addAction(self.actReset)
        self.toolbar.addAction(self.actRetreve)
        self.toolbar.addSeparator()
        #self.toolbar.addAction(self.actExpand)
        #self.toolbar.addAction(self.actCollapse)
        self.toolbar.addAction(self.actExpColl)
        self.toolbar.addAction(self.actExpCheck)
        self.toolbar.addAction(self.actPrint)

        self.setCentralWidget(self.h5wtree.view)

        self.set_style()


    def set_style(self):
        self.setGeometry(10, 10, 350, 500)
        self.setWindowTitle('HDF5 tree, select items')

#------------------

if __name__ == "__main__" :
    app = QtGui.QApplication(sys.argv)
    ex  = H5WTreeInMainWindow(parent=None, fname='/reg/g/psdm/detector/calib/epix100a/epix100a-test.h5')
    ex.show()
    app.exec_()
    sys.exit('End of test')

#------------------