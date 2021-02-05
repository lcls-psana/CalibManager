#--------------------------------------------------------------------------
# File and Version Information:
#  $Id: H5WTree.py 13101 2017-01-29 21:22:43Z dubrovin@SLAC.STANFORD.EDU $
#
# Description:
#  Module H5WTree...
#------------------------------------------------------------------------

"""Shows the HDF5 file tree-structure and allows to select data items

This software was developed for the SIT project.
If you use all or part of it, please give an appropriate acknowledgment.

@version $Id: H5WTree.py 13101 2017-01-29 21:22:43Z dubrovin@SLAC.STANFORD.EDU $

@author Mikhail S. Dubrovin
"""
#------------------------------

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import CalibManager.H5TreeViewModel as h5model
from   CalibManager.QIcons import icon
import CalibManager.H5Print as printh5
from   CalibManager.H5Logger import log

#------------------------------

class H5WTree(QtWidgets.QWidget) :
    """Shows the HDF5 file tree-structure and allows to select data items.
    """
    def __init__(self, parent=None, fname='/reg/g/psdm/detector/calib/epix100a/epix100a-test.h5') :
        QtWidgets.QWidget.__init__(self, parent)

        self.actExpColl = parent.actExpColl if parent is not None else None

        self.fname = fname

        self.list_of_checked_item_names = []
        self.tree_view_is_expanded = False

        icon.set_icons()

        self.icon_folder_open   = icon.icon_folder_open
        self.icon_folder_closed = icon.icon_folder_closed
        self.icon_expand        = icon.icon_expand
        self.icon_collapse      = icon.icon_collapse

        self.model = h5model.H5TreeViewModel(parent, fname)


        #self.view = QtGui.QListView()
        #self.view = QtGui.QTableView()
        self.view = QtWidgets.QTreeView()
        self.view.setModel(self.model)
        #print 'Root is decorated ? ', self.view.rootIsDecorated() # Returns True
        #self.view.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        #self.view.setExpanded(self.indExpandedItem,True)
        self.view.setAnimated(True)
        #self.setCentralWidget(self.view)


        self.vbox = QtWidgets.QVBoxLayout(self) 
        self.vbox.addWidget(self.view)
 
        self.setLayout(self.vbox)

        self.view.selectionModel().currentChanged[QModelIndex, QModelIndex].connect(self.cellSelected)

        #self.view.clicked.connect(self.someMethod1)       # This works
        #self.view.doubleClicked.connect(self.someMethod2) # This works
        self.connect_item_changed()

        self.view.expanded.connect(self.itemExpanded)
        self.view.collapsed.connect(self.itemCollapsed)

        self.processRetreve() # Set all check box states for current configuration
        if self.tree_view_is_expanded :
            #self.processExpand()  # Expand the tree 
            self.processExpCheck() # Expand the tree for checked data items 

        self.tree_window_is_open = True

        self.set_style()


    def connect_item_changed(self):
        self.model.itemChanged.connect(self.itemChanged)


    def disconnect_item_changed(self):
        self.model.itemChanged.disconnect(self.itemChanged)
    

    def set_style(self):
        self.setGeometry(10, 10, 350, 700)
        self.setWindowTitle('HDF5 tree, select items')
        self.layout().setContentsMargins(0,0,0,0)


    def closeEvent(self, event): # if the 'x' (in the top-right corner of the window) is clicked
        #print 'closeEvent'
        #self.parent.processDisplay() # in order to close this window as from GUIMain
        #self.disconnect()
        self.view.close()
        #self.model.close()
        self.menubar.close()
        self.toolbar.close()
        self.tree_window_is_open = False
        #self.display.setText('Open')


    def processExit(self):
        #print 'Exit button is clicked'
        self.close()


    def processApply(self):
        #print 'Apply button is clicked, use all checked items in the tree model for display'
        log.info('Apply button is clicked, use all checked items in the tree model for display')
        self.list_of_checked_item_names = self.model.get_list_of_checked_item_names_for_model()
        #if self.wtdWindowIsOpen :
        #    self.guiwhat.processRefresh()


    def processReset(self):
        #print 'Reset button is clicked, uncheck all items'
        log.info('Reset button is clicked, uncheck all items')
        self.model.reset_checked_items()


    def processRetreve(self):
        msg = '%s' % ('Retreve button is clicked,'\
              'retreve the list of checked items from config. pars. and use them in the tree model.')
        log.info(msg)
        self.model.retreve_checked_items(self.list_of_checked_item_names)


    def processExpCheck(self):
        msg = 'ExpandChecked button is clicked, expand the tree for checked items only.'
        log.info(msg)
        self.processCollapse() # first, collapse the tree
        self.model.expand_checked_items(self.view)
        self.tree_view_is_expanded = True       # Change status for expand/collapse button

        if self.actExpColl is not None :
           self.actExpColl.setIcon(self.icon_collapse)
           self.actExpColl.setText('Collapse tree')


    def processExpand(self):
        log.info('Expand button is clicked')
        self.model.set_all_group_icons(self.icon_expand)
        self.view.expandAll()
        self.tree_view_is_expanded = True


    def processCollapse(self):
        log.info('Collapse button is clicked')
        self.model.set_all_group_icons(self.icon_collapse)
        self.view.collapseAll()
        self.tree_view_is_expanded = False


    def processExpColl(self): # Flip/flop between Expand and Collaple the HDF5 tree
        log.info('Expand/Collapse button is clicked :')
        if self.tree_view_is_expanded == True :
            if self.actExpColl is not None :
               self.actExpColl.setIcon(self.icon_expand)
               self.actExpColl.setText('Expand tree')
            self.processCollapse()
        else :
            if self.actExpColl is not None :
               self.actExpColl.setIcon(self.icon_collapse)
               self.actExpColl.setText('Collapse tree')
            self.processExpand()

 
    def processPrint(self):
        log.info('Print button is clicked')
        fname = self.fname
        log.info('Print structure of the HDF5 file:\n %s' % fname)
        printh5.print_hdf5_file_structure(fname)


    def someMethod1(self):
        log.info('1-clicked!')


    def someMethod2(self):
        log.info('2-clicked!')


    def itemExpanded(self, ind): 
        item = self.model.itemFromIndex(ind)
        item.setIcon(self.icon_folder_open)
        log.info('Item expanded: %s' % item.text())


    def itemCollapsed(self, ind):
        item = self.model.itemFromIndex(ind)
        item.setIcon(self.icon_folder_closed)
        log.info('Item collapsed: %s' % item.text())


    def itemSelected(self, selected, deselected):
        log.info('  %d items selected\n  %d items deselected' % (len(selected), len(deselected)))


    def cellSelected(self, ind_sel, ind_desel):
        dsfullname = str(self.model.get_full_name_from_index(ind_sel))
        log.info('Selected item "%s"' % dsfullname)
        printh5.print_dataset_metadata_from_file(self.fname, dsfullname)

        #print "ind   selected row, col = ", ind_sel.row(),  ind_sel.column()
        #print "ind deselected row, col = ", ind_desel.row(),ind_desel.column() 
        #item       = self.model.itemFromIndex(ind_sel)
        #dsfullname = str(self.model.get_full_name_from_item(item))
        #print ' isEnabled=',item.isEnabled() 
        #print ' isCheckable=',item.isCheckable() 
        #print ' checkState=',item.checkState()
        #print ' isSelectable=',item.isSelectable() 
        #print ' isTristate=',item.isTristate() 
        #print ' isEditable=',item.isEditable() 
        #print ' isExpanded=',self.view.isExpanded(ind_sel)


    def itemChanged(self, item):
        state = ['UNCHECKED', 'TRISTATE', 'CHECKED'][item.checkState()]
        msg = "Item with full name %s, is at state %s" % (self.model.get_full_name_from_item(item), state)
        log.info(msg)

        #print 'level from top:', self.model.distance_from_top(item)

        self.disconnect_item_changed()
        ###self.model.check_parents(item)
        self.model.check_children(item)
        self.connect_item_changed()
    
#------------------
#   -- test --
#------------------

if __name__ == "__main__" :
    #l /reg/d/psdm/xpp/*/calib/epix100a/
    #fname='/reg/g/psdm/detector/calib/epix100a/epix100a-test.h5'
    fname0='/reg/d/psdm/xpp/xppl7416/calib/epix100a/'\
           'epix100a-3925999620-0996513537-2080374794-1794135040-0940361739-2398406657-0419430424.h5'
    fname = sys.argv[1] if len(sys.argv)==2 else fname0    
    log.setPrintBits(0o377)

    app = QtWidgets.QApplication(sys.argv)
    ex  = H5WTree(None, fname)
    ex.show()
    app.exec_()
    sys.exit('End of test')

#------------------
