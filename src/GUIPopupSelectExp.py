#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module GUIPopupSelectExp...
#------------------------------------------------------------------------

"""Popup GUI for experiment selection"""

#--------------------------------
__version__ = "$Revision$"
#--------------------------------

import os

from PyQt4 import QtGui, QtCore
from Logger import logger
from ConfigParametersForApp import cp
from GlobalUtils import selectFromListInPopupMenu

#------------------------------

def years(lst_exp) :
    years = []
    for exp in lst_exp :
        year = exp[-2:]
        if year in years : continue
        if not year.isdigit() : continue
        years.append(year)
    return ['20%s'%y for y in sorted(years)]

#------------------------------

def lst_exp_for_year(lst_exp, year) :
    str_year = year if isinstance(year,str) else '%4d'%year
    pattern = str_year[-2:] # two last digits if the year
    return [exp for exp in lst_exp if exp[-2:]==pattern]

#------------------------------  

class GUIPopupList(QtGui.QDialog) :
#class GUIPopupList(QtGui.QWidget) :
#    """
#    """
    def __init__(self, parent=None, lst_exp=[]):

        QtGui.QDialog.__init__(self, parent)

        self.name_sel = None
        self.list = QtGui.QListWidget(parent)

        self.fill_list(lst_exp)

        # Confirmation buttons
        #self.but_cancel = QtGui.QPushButton('&Cancel') 
        #self.but_apply  = QtGui.QPushButton('&Apply') 
        #cp.setIcons()
        #self.but_cancel.setIcon(cp.icon_button_cancel)
        #self.but_apply .setIcon(cp.icon_button_ok)
        #self.connect(self.but_cancel, QtCore.SIGNAL('clicked()'), self.onCancel)
        #self.connect(self.but_apply,  QtCore.SIGNAL('clicked()'), self.onApply)

        #self.hbox = QtGui.QVBoxLayout()
        #self.hbox.addWidget(self.but_cancel)
        #self.hbox.addWidget(self.but_apply)
        ##self.hbox.addStretch(1)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.list)
        #vbox.addLayout(self.hbox)
        self.setLayout(vbox)

        self.list.itemClicked.connect(self.onItemClick)

        self.showToolTips()
        self.setStyle()


    def fill_list_v0(self, lst_exp) :
        for exp in sorted(lst_exp) :
            item = QtGui.QListWidgetItem(exp, self.list)
        self.list.sortItems(QtCore.Qt.AscendingOrder)


    def fill_list(self, lst_exp) :
        for year in sorted(years(lst_exp)) :
            item = QtGui.QListWidgetItem(year, self.list)
            item.setFont(QtGui.QFont('Courier', 14, QtGui.QFont.Bold))
            item.setFlags(QtCore.Qt.NoItemFlags)
            for exp in sorted(lst_exp_for_year(lst_exp, year)) :
                item = QtGui.QListWidgetItem(exp, self.list)
                item.setFont(QtGui.QFont('Monospace', 11, QtGui.QFont.Normal)) # Bold))

        #self.list.scrollToItem(item)

        #self.list.setItemWidget(item, widg)
        #self.list.setItemHidden(item, False)
        #self.list.sortItems(QtCore.Qt.AscendingOrder)
        #widg = self.list.itemWidget(item)


    def setStyle(self):
        self.setWindowTitle('Select experiment')
        self.setFixedWidth(120)
        self.setMinimumHeight(600)
        #self.setMaximumWidth(600)
        self.setStyleSheet(cp.styleBkgd)
        self.setContentsMargins(QtCore.QMargins(-9,-9,-9,-9))
        self.setStyleSheet(cp.styleBkgd)
        #self.but_cancel.setStyleSheet(cp.styleButton)
        #self.but_apply.setStyleSheet(cp.styleButton)
        self.move(QtGui.QCursor.pos().__add__(QtCore.QPoint(-110,-50)))


    def showToolTips(self):
        #self.but_apply.setToolTip('Apply selection')
        #self.but_cancel.setToolTip('Cancel selection')
        self.setToolTip('Select experiment')


    def onItemClick(self, item):
        #if item.isSelected(): item.setSelected(False)
        #widg = self.list.itemWidget(item)
        #item.checkState()
        self.name_sel = item.text()
        #print self.name_sel
        logger.debug('Selected experiment %s' % self.name_sel, __name__)  
        self.accept()


    def closeEvent(self, event):
        logger.info('closeEvent', __name__)
        self.reject()


    def selectedName(self):
        return self.name_sel

 
    def onCancel(self):
        logger.debug('onCancel', __name__)
        self.reject()


    def onApply(self):
        logger.debug('onApply', __name__)  
        self.accept()

#------------------------------  

class GUIPopupSelectExp(QtGui.QDialog) :
    """
    """

    def __init__(self, parent=None, lst_exp=[], orient='H'):
        QtGui.QDialog.__init__(self,parent)
        self.orient = orient
        self.lst_exp = lst_exp
        self.exp_name = None

        #self.setGeometry(20, 40, 500, 200)
        self.setWindowTitle('Select experiment')

        self.makeTabBar()
        self.guiSelector()
 
        self.setStyle()
        self.showToolTips()

        #self.hboxW = QtGui.QHBoxLayout()
        self.box = QtGui.QVBoxLayout(self) if self.orient=='H' else QtGui.QHBoxLayout(self) 

        self.box.addWidget(self.tab_bar)
        #self.box.addLayout(self.hboxW)
        #self.box.addStretch(1)

        self.setLayout(self.box)

        self.showToolTips()
        self.setStyle()
        #gu.printStyleInfo(self)

        cp.guitabs = self
        #self.move(10,25)

        #self.onTabBar()
     
#-----------------------------  

    def makeTabBar(self) :

        self.tab_bar = QtGui.QTabBar()
        tab_names = years(lst_exp)

        for tab_name in tab_names :
            tab_ind = self.tab_bar.addTab(tab_name)
            self.tab_bar.setTabTextColor(tab_ind, QtGui.QColor('blue')) #gray, red, grayblue

        self.tab_bar.setShape(QtGui.QTabBar.RoundedNorth if self.orient=='H' else QtGui.QTabBar.RoundedWest)

        tab_name = tab_names[-1]
        tab_index = tab_names.index(tab_name)
        self.tab_bar.setCurrentIndex(tab_index)

        self.connect(self.tab_bar, QtCore.SIGNAL('currentChanged(int)'), self.onTabBar)


    def guiSelector(self):

        #try    : self.gui_win.close()
        #except : pass

        ##try    : del self.gui_win
        ##except : pass

        #self.gui_win = self.dict_tab_obj[self.tab_name]
        #self.hboxW.addWidget(self.gui_win)
        #self.gui_win.setVisible(True)
        pass


    def onTabBar(self):
        tab_ind = self.tab_bar.currentIndex()
        tab_name = str(self.tab_bar.tabText(tab_ind))
        print 'Tab index: %d, name: %s' % (tab_ind, tab_name)
        self.guiSelector()

        year = tab_name
        lst_expts = lst_exp_for_year(self.lst_exp, year)
        self.exp_name = selectFromListInPopupMenu(lst_expts)
        print 'Selection:', self.exp_name
        if self.exp_name is not None : self.close()


    def showToolTips(self):
        #self.but_apply.setToolTip('Apply changes to the list')
        #self.but_cancel.setToolTip('Use default list')
        pass


    def setStyle(self):
        #self.setFixedWidth(200)
        self.setMinimumWidth(200)
        self.setMaximumWidth(500)
        self.setStyleSheet(cp.styleBkgd)
        self.setContentsMargins(QtCore.QMargins(-9,-9,-9,-9))
        self.move(QtGui.QCursor.pos())

        #self.setMouseTracking(1)

 
    #def resizeEvent(self, e):
        #logger.debug('resizeEvent', __name__) 
        #pass


    #def moveEvent(self, e):
        #pass


    def closeEvent(self, event):
        logger.debug('closeEvent', __name__)
        #print 'closeEvent'
        #try    : self.widg_pars.close()
        #except : pass


    #def event(self, event):
        #print 'Event happens...:', event


    #def mouseMoveEvent(self, e):
    #    print "on Hover", e.pos().x(), e.pos().y()


    def onCancel(self):
        logger.debug('onCancel', __name__)
        self.reject()


    def onApply(self):
        logger.debug('onApply', __name__)  
        self.accept()

#------------------------------
#------------------------------
#----------- TESTS ------------
#------------------------------
#------------------------------

def select_experiment_v1(lst_exp) :
    w = GUIPopupSelectExp(None, lst_exp)
    ##w.show()
    resp=w.exec_()
    return w.exp_name

#------------------------------

def select_experiment_v2(lst_exp) :
    lst_years = years(lst_exp)
    year = selectFromListInPopupMenu(lst_years)
    if year is None : return None
    exp_for_year = lst_exp_for_year(lst_exp, year)

    return selectFromListInPopupMenu(exp_for_year)

#------------------------------

def select_experiment_v3(parent, lst_exp) :
    w = GUIPopupList(parent, lst_exp)
    ##w.show()
    resp=w.exec_()
    if   resp == QtGui.QDialog.Accepted : return w.selectedName()
    elif resp == QtGui.QDialog.Rejected : return None
    else : return None

#------------------------------

def test(lst_exp) :
    #exp_name = select_experiment_v1(lst_exp)
    #exp_name = select_experiment_v2(lst_exp)
    exp_name = select_experiment_v3(None, lst_exp)
    print 'exp_name = %s' % exp_name 

#------------------------------

if __name__ == "__main__" :

    import sys

    lst_exp = sorted(os.listdir('/reg/d/psdm/CXI/'))
    #print 'lst_exps:', lst_exp    
    print 'years form the list of experiments', years(lst_exp)
    print 'experiments for 2016:', lst_exp_for_year(lst_exp, '2016')

    app = QtGui.QApplication(sys.argv)

    test(lst_exp)

#------------------------------