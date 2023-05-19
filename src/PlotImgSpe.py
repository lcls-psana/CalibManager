
"""Module PlotImgSpe  - Plots image and spectrum for 2d array.

This software was developed for the SIT project.
If you use all or part of it, please give an appropriate acknowledgment.

@author Mikhail Dubrovin
"""

import os
import sys
import matplotlib
matplotlib.use('QtAgg') # forse Agg rendering to a Qt canvas (backend)

#if __name__ == "__main__":
#    import matplotlib
#    matplotlib.use('Qt4Agg') # forse Agg rendering to a Qt4 canvas (backend)

import logging
logger = logging.getLogger(__name__)

from PyQt5 import QtCore, QtGui, QtWidgets

from . import PlotImgSpeWidget  as imgwidg
from . import PlotImgSpeButtons as imgbuts

from .ConfigParametersForApp import cp
from . import GlobalUtils as gu


class PlotImgSpe(QtWidgets.QWidget):
    """Plots image and spectrum for 2d array"""

    def __init__(self, parent=None, arr=None, ifname='', ofname='./fig.png', title='Plot 2d array',\
                 orient=0, y_is_flip=False, is_expanded=False, verb=False, fexmod=False ):
        QtWidgets.QWidget.__init__(self, parent)
        self.setGeometry(20, 40, 700, 800)
        self.setWindowTitle(title)

        logging.basicConfig(format='[%(levelname).1s] %(filename)s L%(lineno)04d: %(message)s', level=logging.INFO)
        logger.info('in PlotImgSpe')

        if arr is not None: self.arr = arr
        elif ifname != '' \
             and os.path.exists(ifname): self.arr = gu.get_image_array_from_file(ifname)
        else                           : self.arr = get_array2d_for_test()

        sys.stdout.write('     image shape : %s\n' % str(self.arr.shape))

        self.ext_ref = None

        self.widgimage = imgwidg.PlotImgSpeWidget(self, self.arr, orient, y_is_flip)
        self.widgbuts  = imgbuts.PlotImgSpeButtons(self, self.widgimage, ifname, ofname, None, is_expanded, fexmod, verb)
        #self.mpl_toolbar = imgtb.ImgSpeNavToolBar(self.widgimage, self)

        vbox = QtWidgets.QVBoxLayout()                  # <=== Begin to combine layout
        #vbox.addWidget(self.widgimage)                 # <=== Add figure as QWidget
        vbox.addWidget(self.widgimage.getCanvas())      # <=== Add figure as FigureCanvas
        #vbox.addWidget(self.mpl_toolbar)               # <=== Add toolbar
        vbox.addWidget(self.widgbuts)                   # <=== Add buttons
        self.setLayout(vbox)
        #self.show()
        self.layout().setContentsMargins(0,0,0,0)
        #cp.plotimgspe = self


    def set_image_array(self,arr,title='Plot 2d array'):
        self.widgimage.set_image_array(arr)
        self.setWindowTitle(title)


    def set_image_array_new(self,arr,title='Plot 2d array', orient=0, y_is_flip=False):
        self.widgimage.set_image_array_new(arr, orient, y_is_flip)
        self.setWindowTitle(title)


    #def resizeEvent(self, e):
    #    #print 'resizeEvent'
    #    pass


    def closeEvent(self, event): # is called for self.close() or when click on "x"

        try   : self.widgimage.close()
        except: pass

        try   : self.widgbuts.close()
        except: pass

        cp.plotimgspe = None


def do_work(parser):
    (opts, args) = parser.parse_args()

    pars = {'parent'          : None,
            'arr'             : None,
            'ifname'          : opts.ifname,
            'ofname'          : opts.ofname,
            'title'           : opts.title,
            'orient'          : opts.rot90,
            'y_is_flip'       : opts.mirror,
            'is_expanded'     : opts.expand,
            'verb'            : opts.verb,
            'fexmod'          : opts.fexmod}

    if args != []:
        if args[0] != '': pars['ifname'] = args[0]

    s = 'Start PlotImgSpe with input parameters:\n'
    for k,v in pars.items(): s += '%16s : %s\n' % (k,v)
    sys.stdout.write(s)

    app = QtWidgets.QApplication(sys.argv)
    w = PlotImgSpe(**pars)
    w.move(QtCore.QPoint(300,10))
    w.show()
    app.exec_()
    sys.exit('End of %s' % sys.argv[0])


def get_array2d_for_test():
    import random
    import numpy as np
    mu, sigma = 200, 25
    rows, cols = 1300, 1340
    arr = mu + sigma*np.random.standard_normal(size=rows*cols)
    #arr = 100*np.random.standard_exponential(size=2400)
    #arr = np.arange(2400)
    arr.shape = (rows,cols)
    return arr


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = PlotImgSpe(None, is_expanded=False)
    w.set_image_array(get_array2d_for_test())
    w.move(QtCore.QPoint(50,50))
    w.show()
    app.exec_()

# EOF
