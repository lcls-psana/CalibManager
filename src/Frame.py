#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#   Frame...
#------------------------------------------------------------------------

"""Frame derived from QFrame
Created on Dec 3, 2014

@author: Mikhail
"""
#--------------------------------
__version__ = "$Revision$"
#--------------------------------

#from PyQt4.Qt import QFrame
from PyQt5 import QtCore, QtGui, QtWidgets

class Frame(QtWidgets.QFrame):
    """ class Frame inherits from QFrame and sets its parameters.

    QFrame inherits from QWidget and hence Frame can be used in stead of QWidget
    """
    def __init__(self, parent=None, lw=0, mlw=1, vis=True, style=QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken):
        QtWidgets.QFrame.__init__(self, parent)
        self.parent = parent
        self.setFrame(lw, mlw, vis, style)


    def setFrame(self, lw=0, mlw=1, vis=False, style=QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken):
        self.setFrameStyle(style) #Box, Panel | Sunken, Raised 
        self.setLineWidth(lw)
        self.setMidLineWidth(mlw)
        self.setBoarderVisible(vis) 
        #self.setGeometry(self.parent.rect())
        #self.layout().setContentsMargins(0,0,0,0)

    def setBoarderVisible(self, vis=True) :
        if vis : self.setFrameShape(QtWidgets.QFrame.Box)
        else   : self.setFrameShape(QtWidgets.QFrame.NoFrame)
    
#    def resizeEvent(self, e):
#        print 'resizeEvent'
#        #self.setGeometry(self.parent.rect())

#---------------------------
# TEST AND EXAMPLE OF USAGE
#---------------------------

class GUILabel(QtWidgets.QLabel, Frame):
    def __init__(self, parent=None):
        Frame       .__init__(self, parent, mlw=5)
        #QtGui.QLabel.__init__(self, QtCore.QString('label'), parent)
        self.setText('GUILabel set')

  
class GUIWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        #super(GUIWidget, self).__init__(parent)
        but = QtWidgets.QPushButton('Button', self)
        but.move(30,20)


class GUIWidgetFrame(Frame, QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        Frame        .__init__(self, parent, mlw=5)
        but = QtWidgets.QPushButton('Button', self)
        but.move(20,10)


# Use Frame in stead of QWidget
class GUIFrame(Frame):
    def __init__(self, parent=None):
        #Frame.__init__(self, parent, mlw=5)
        Frame.__init__(self, mlw=30)
        but = QtWidgets.QPushButton('Button', self)
        but.move(30,20)

#-----------------------------

if __name__ == "__main__" :
    import sys
    
    app = QtWidgets.QApplication(sys.argv)

    ##w = QtGui.QTextEdit()
    #w = QtGui.QLabel('QLabel')
    #fb = Frame(w, lw=0, mlw=3, vis=True)
    #w = GUILabel()
    #w = GUIWidgetFrame()
    #w = GUIWidget()
    w = GUIFrame()
    w.setWindowTitle('GUIWidget')
    w.setGeometry(200, 500, 200, 100)
    w.show()
    app.exec_()

#-----------------------------
