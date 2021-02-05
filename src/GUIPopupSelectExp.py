#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module GUIPopupSelectExp...
#------------------------------------------------------------------------

"""Popup GUI for experiment selection"""
from __future__ import print_function

import os

from PyQt5 import QtCore, QtGui, QtWidgets
#from CalibManager.Logger import logger
#from CalibManager.ConfigParametersForApp import cp

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

def years_and_runs(lst_exp) :
    years = []
    runs  = []
    for exp in lst_exp :
        if len(exp) != 8 : continue
        year = exp[-2:]
        if year in years : continue
        if not year.isdigit() : continue
        years.append(year)

    for exp in lst_exp :
        if len(exp) != 9 : continue
        run = exp[-2:]
        if run in runs : continue
        if not run.isdigit() : continue
        runs.append(run)

    return ['20%s'%y for y in sorted(years)], ['Run:%s'%r for r in sorted(runs)]

#------------------------------

def lst_exp_for_year(lst_exp, year) :
    str_year = year if isinstance(year,str) else '%4d'%year
    pattern = str_year[-2:] # two last digits if the year
    return [exp for exp in lst_exp if exp[-2:]==pattern]

#------------------------------  

class GUIPopupList(QtWidgets.QDialog) :
    """
    """
    def __init__(self, parent=None, lst_exp=[]):

        QtWidgets.QDialog.__init__(self, parent)

        self.name_sel = None
        self.list = QtWidgets.QListWidget(parent)

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

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.list)
        #vbox.addLayout(self.hbox)
        self.setLayout(vbox)

        self.list.itemClicked.connect(self.onItemClick)

        self.showToolTips()
        self.setStyle()


    def fill_list_v0(self, lst_exp) :
        for exp in sorted(lst_exp) :
            item = QtWidgets.QListWidgetItem(exp, self.list)
        self.list.sortItems(QtCore.Qt.AscendingOrder)


    def fill_list_v1(self, lst_exp) :
        self.years = sorted(years(lst_exp))
        for year in self.years :
            item = QtWidgets.QListWidgetItem(year, self.list)
            item.setFont(QtGui.QFont('Courier', 14, QtGui.QFont.Bold))
            item.setFlags(QtCore.Qt.NoItemFlags)
            #item.setFlags(QtCore.Qt.NoItemFlags ^ QtCore.Qt.ItemIsEnabled ^ QtCore.Qt.ItemIsSelectable)
            for exp in sorted(lst_exp_for_year(lst_exp, year)) :
                item = QtWidgets.QListWidgetItem(exp, self.list)
                item.setFont(QtGui.QFont('Monospace', 11, QtGui.QFont.Normal)) # Bold))

    def fill_list(self, lst_exp) :
        self.years, self.runs = years_and_runs(lst_exp)

        for year in self.years :
            item = QtWidgets.QListWidgetItem(year, self.list)
            item.setFont(QtGui.QFont('Courier', 14, QtGui.QFont.Bold))
            item.setFlags(QtCore.Qt.NoItemFlags)
            #item.setFlags(QtCore.Qt.NoItemFlags ^ QtCore.Qt.ItemIsEnabled ^ QtCore.Qt.ItemIsSelectable)
            for exp in sorted(lst_exp_for_year(lst_exp, year)) :
                if len(exp) != 8 : continue
                item = QtWidgets.QListWidgetItem(exp, self.list)
                item.setFont(QtGui.QFont('Monospace', 11, QtGui.QFont.Normal)) # Bold))

        for run in self.runs :
            item = QtWidgets.QListWidgetItem(run, self.list)
            item.setFont(QtGui.QFont('Courier', 14, QtGui.QFont.Bold))
            item.setFlags(QtCore.Qt.NoItemFlags)
            #item.setFlags(QtCore.Qt.NoItemFlags ^ QtCore.Qt.ItemIsEnabled ^ QtCore.Qt.ItemIsSelectable)
            for exp in sorted(lst_exp_for_year(lst_exp, run)) :
                if len(exp) != 9 : continue
                item = QtWidgets.QListWidgetItem(exp, self.list)
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
        #self.setStyleSheet(cp.styleBkgd)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        self.layout().setContentsMargins(0,0,0,0)
        #self.setStyleSheet(cp.styleBkgd)
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
        if self.name_sel in self.years : return # ignore selection of year
        if self.name_sel in self.runs  : return # ignore selection of run
        #print('XXX self.name_sel:', self.name_sel)
        #logger.debug('Selected experiment %s' % self.name_sel, __name__)  
        self.accept()
        #print('XXX done:')
        self.done(QtWidgets.QDialog.Accepted)


    def event(self, e):
        """Intercepts mouse clicks outside popup window"""
        #print 'event.type', e.type()
        if e.type() == QtCore.QEvent.WindowDeactivate :
            self.reject()
            self.done(QtWidgets.QDialog.Rejected)
        return QtWidgets.QDialog.event(self, e)
    

    def closeEvent(self, event):
        #logger.info('closeEvent', __name__)
        self.reject()
        self.done(QtWidgets.QDialog.Rejected)


    def selectedName(self):
        return self.name_sel

 
    def onCancel(self):
        #logger.debug('onCancel', __name__)
        self.reject()
        self.done(QtWidgets.QDialog.Rejected)


    def onApply(self):
        #logger.debug('onApply', __name__)  
        self.accept()
        self.done(QtWidgets.QDialog.Accepted)

#------------------------------  

class GUIPopupSelectExp(QtWidgets.QDialog) :
    """
    """

    def __init__(self, parent=None, lst_exp=[], orient='H'):
        QtWidgets.QDialog.__init__(self,parent)
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
        self.box = QtWidgets.QVBoxLayout(self) if self.orient=='H' else QtWidgets.QHBoxLayout(self) 

        self.box.addWidget(self.tab_bar)
        #self.box.addLayout(self.hboxW)
        #self.box.addStretch(1)

        self.setLayout(self.box)

        self.showToolTips()
        self.setStyle()
        #gu.printStyleInfo(self)

        #cp.guitabs = self
        #self.move(10,25)

        #self.onTabBar()
     
#-----------------------------  

    def makeTabBar(self) :

        self.tab_bar = QtWidgets.QTabBar()
        tab_names = years(self.lst_exp)

        for tab_name in tab_names :
            tab_ind = self.tab_bar.addTab(tab_name)
            self.tab_bar.setTabTextColor(tab_ind, QtGui.QColor('blue')) #gray, red, grayblue

        self.tab_bar.setShape(QtWidgets.QTabBar.RoundedNorth if self.orient=='H' else QtWidgets.QTabBar.RoundedWest)

        tab_name = tab_names[-1]
        tab_index = tab_names.index(tab_name)
        self.tab_bar.setCurrentIndex(tab_index)

        self.tab_bar.currentChanged[int].connect(self.onTabBar)


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
        from CalibManager.GlobalUtils import selectFromListInPopupMenu

        tab_ind = self.tab_bar.currentIndex()
        tab_name = str(self.tab_bar.tabText(tab_ind))
        print('Tab index: %d, name: %s' % (tab_ind, tab_name))
        self.guiSelector()

        year = tab_name
        lst_expts = lst_exp_for_year(self.lst_exp, year)
        self.exp_name = selectFromListInPopupMenu(lst_expts)
        print('Selection:', self.exp_name)
        if self.exp_name is not None : self.close()


    def showToolTips(self):
        #self.but_apply.setToolTip('Apply changes to the list')
        #self.but_cancel.setToolTip('Use default list')
        pass


    def setStyle(self):
        #self.setFixedWidth(200)
        self.setMinimumWidth(200)
        self.setMaximumWidth(500)
        #self.setStyleSheet(cp.styleBkgd)
        self.layout().setContentsMargins(0,0,0,0)
        self.move(QtGui.QCursor.pos())

        #self.setMouseTracking(1)

 
    #def resizeEvent(self, e):
        #logger.debug('resizeEvent', __name__) 
        #pass


    #def moveEvent(self, e):
        #pass


    def closeEvent(self, event):
        pass
        #logger.debug('closeEvent', __name__)
        #print 'closeEvent'
        #try    : self.widg_pars.close()
        #except : pass


    #def event(self, event):
        #print 'Event happens...:', event


    #def mouseMoveEvent(self, e):
    #    print "on Hover", e.pos().x(), e.pos().y()


    def onCancel(self):
        #logger.debug('onCancel', __name__)
        self.reject()


    def onApply(self):
        #logger.debug('onApply', __name__)  
        self.accept()

#------------------------------

def select_experiment_v1(lst_exp) :
    w = GUIPopupSelectExp(None, lst_exp)
    ##w.show()
    resp=w.exec_()
    return w.exp_name

#------------------------------

def select_experiment_v2(lst_exp) :
    from CalibManager.GlobalUtils import selectFromListInPopupMenu

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
    #print('XXX resp:', resp, w.selectedName())
    #QtWidgets.QDialog.Accepted is 1
    #QtWidgets.QDialog.Rejected is 0

    #if   resp == QtWidgets.QDialog.Accepted : return w.selectedName()
    #elif resp == QtWidgets.QDialog.Rejected : return None
    #else : return None

    return w.selectedName()

#------------------------------
#------------------------------
#----------- TESTS ------------
#------------------------------
#------------------------------
 
def test_all(tname) :
    lst_exp = sorted(os.listdir('/reg/d/psdm/SXR/'))
    #lst_exp = sorted(os.listdir('/reg/d/psdm/CXI/'))
    #print 'lst_exps:', lst_exp    
    print('years form the list of experiments', years(lst_exp))
    print('years and runs form the list of experiments', str(years_and_runs(lst_exp)))
    print('experiments for 2016:', lst_exp_for_year(lst_exp, '2016'))

    app = QtWidgets.QApplication(sys.argv)

    exp_name = 'N/A'
    if tname == '1': exp_name = select_experiment_v1(lst_exp)
    if tname == '2': exp_name = select_experiment_v2(lst_exp)
    if tname == '3': exp_name = select_experiment_v3(None, lst_exp)

    print('exp_name = %s' % exp_name) 

#------------------------------

if __name__ == "__main__" :
    import sys; global sys
    tname = sys.argv[1] if len(sys.argv) > 1 else '3'
    print(50*'_', '\nTest %s' % tname)
    test_all(tname)
    sys.exit('End of Test %s' % tname)

#------------------------------
