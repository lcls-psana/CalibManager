
#------------------------------
"""
Usage ::
    from CalibManager.QIcons import icon
    # then get QtGui.QIcon objects

    app = QtGui.QApplication(sys.argv)

    icon.set_icons()
    icon1 = icon.icon_exit
    icon2 = icon.icon_home

@see class :py:class:`graphqt.QIcons`

@see project modules
    * :py:class:`CalibManager.AppDataPath`
    * :py:class:`CalibManager.ConfigParameters`

This software was developed for the SIT project.
If you use all or part of it, please give an appropriate acknowledgment.

@version $Id:QIcons.py 11923 2016-11-22 14:28:00Z dubrovin@SLAC.STANFORD.EDU $

@author Mikhail S. Dubrovin
"""
from __future__ import print_function
#------------------------------

import os
from PyQt5 import QtCore, QtGui#, QtWidgets
import CalibManager.AppDataPath as apputils # for icons

#------------------------------

class QIcons(object) :
    """A singleton storage of icons with caching.
    """
    def __init__(self) :
        self._name = self.__class__.__name__
        self.icons_are_loaded = False

#------------------------------

    def set_icons(self) :
        """SHOULD BE CALLED AFTER QtGui.QApplication"""

        if self.icons_are_loaded : return
        self.icons_are_loaded = True

        path_icon = 'CalibManager/icons'
        #path_icon = 'expmon/icons'

        self.path_icon_contents      = apputils.AppDataPath('%s/contents.png' % path_icon     ).path()
        self.path_icon_mail_forward  = apputils.AppDataPath('%s/mail-forward.png' % path_icon ).path()
        self.path_icon_button_ok     = apputils.AppDataPath('%s/button_ok.png' % path_icon    ).path()
        self.path_icon_button_cancel = apputils.AppDataPath('%s/button_cancel.png' % path_icon).path()
        self.path_icon_exit          = apputils.AppDataPath('%s/exit.png' % path_icon         ).path()
        self.path_icon_home          = apputils.AppDataPath('%s/home.png' % path_icon         ).path()
        self.path_icon_redo          = apputils.AppDataPath('%s/redo.png' % path_icon         ).path()
        self.path_icon_undo          = apputils.AppDataPath('%s/undo.png' % path_icon         ).path()
        self.path_icon_reload        = apputils.AppDataPath('%s/reload.png' % path_icon       ).path()
        self.path_icon_save          = apputils.AppDataPath('%s/save.png' % path_icon         ).path()
        self.path_icon_save_cfg      = apputils.AppDataPath('%s/fileexport.png' % path_icon   ).path()
        self.path_icon_edit          = apputils.AppDataPath('%s/edit.png' % path_icon         ).path()
        self.path_icon_browser       = apputils.AppDataPath('%s/fileopen.png' % path_icon     ).path()
        self.path_icon_monitor       = apputils.AppDataPath('%s/icon-monitor.png' % path_icon ).path()
        self.path_icon_unknown       = apputils.AppDataPath('%s/icon-unknown.png' % path_icon ).path()
        self.path_icon_plus          = apputils.AppDataPath('%s/icon-plus.png' % path_icon    ).path()
        self.path_icon_minus         = apputils.AppDataPath('%s/icon-minus.png' % path_icon   ).path()
        self.path_icon_logviewer     = apputils.AppDataPath('%s/logviewer.png' % path_icon    ).path()
        self.path_icon_lock          = apputils.AppDataPath('%s/locked-icon.png' % path_icon  ).path()
        self.path_icon_unlock        = apputils.AppDataPath('%s/unlocked-icon.png' % path_icon).path()
        self.path_icon_convert       = apputils.AppDataPath('%s/icon-convert.png' % path_icon ).path()
        self.path_icon_table         = apputils.AppDataPath('%s/table.gif' % path_icon        ).path()
        self.path_icon_folder_open   = apputils.AppDataPath('%s/folder_open.gif' % path_icon  ).path()
        self.path_icon_folder_closed = apputils.AppDataPath('%s/folder_closed.gif' % path_icon).path()
        self.path_icon_expcheck      = apputils.AppDataPath('%s/folder_open_checked.png' % path_icon).path()
 
        self.icon_contents      = QtGui.QIcon(self.path_icon_contents     )
        self.icon_mail_forward  = QtGui.QIcon(self.path_icon_mail_forward )
        self.icon_button_ok     = QtGui.QIcon(self.path_icon_button_ok    )
        self.icon_button_cancel = QtGui.QIcon(self.path_icon_button_cancel)
        self.icon_exit          = QtGui.QIcon(self.path_icon_exit         )
        self.icon_home          = QtGui.QIcon(self.path_icon_home         )
        self.icon_redo          = QtGui.QIcon(self.path_icon_redo         )
        self.icon_undo          = QtGui.QIcon(self.path_icon_undo         )
        self.icon_reload        = QtGui.QIcon(self.path_icon_reload       )
        self.icon_save          = QtGui.QIcon(self.path_icon_save         )
        self.icon_save_cfg      = QtGui.QIcon(self.path_icon_save_cfg     )
        self.icon_edit          = QtGui.QIcon(self.path_icon_edit         )
        self.icon_browser       = QtGui.QIcon(self.path_icon_browser      )
        self.icon_monitor       = QtGui.QIcon(self.path_icon_monitor      )
        self.icon_unknown       = QtGui.QIcon(self.path_icon_unknown      )
        self.icon_plus          = QtGui.QIcon(self.path_icon_plus         )
        self.icon_minus         = QtGui.QIcon(self.path_icon_minus        )
        self.icon_logviewer     = QtGui.QIcon(self.path_icon_logviewer    )
        self.icon_lock          = QtGui.QIcon(self.path_icon_lock         )
        self.icon_unlock        = QtGui.QIcon(self.path_icon_unlock       )
        self.icon_convert       = QtGui.QIcon(self.path_icon_convert      )
        self.icon_table         = QtGui.QIcon(self.path_icon_table        )
        self.icon_folder_open   = QtGui.QIcon(self.path_icon_folder_open  )
        self.icon_folder_closed = QtGui.QIcon(self.path_icon_folder_closed)
        self.icon_expcheck      = QtGui.QIcon(self.path_icon_expcheck     )

        self.icon_data          = self.icon_table
        self.icon_apply         = self.icon_button_ok
        self.icon_reset         = self.icon_undo
        self.icon_retreve       = self.icon_redo
        self.icon_expand        = self.icon_folder_open
        self.icon_collapse      = self.icon_folder_closed
        self.icon_print         = self.icon_contents
 
#------------------------------
        
icon = QIcons()

#------------------------------

def test_QIcons() :
    print('Icon pathes:')
    print(icon.path_icon_contents)
    print(icon.path_icon_mail_forward)
    print(icon.path_icon_button_ok)
    print(icon.path_icon_button_cancel)
    print(icon.path_icon_exit)
    print(icon.path_icon_home)
    print(icon.path_icon_redo)
    print(icon.path_icon_undo)  
    print(icon.path_icon_reload)
    print(icon.path_icon_save)
    print(icon.path_icon_save_cfg)
    print(icon.path_icon_edit)
    print(icon.path_icon_browser)
    print(icon.path_icon_monitor)
    print(icon.path_icon_unknown)
    print(icon.path_icon_plus)
    print(icon.path_icon_minus)
    print(icon.path_icon_logviewer)
    print(icon.path_icon_lock)
    print(icon.path_icon_unlock)
    print(icon.path_icon_convert)
    print(icon.path_icon_table)
    print(icon.path_icon_folder_open)
    print(icon.path_icon_folder_closed)
    print(icon.path_icon_data)

#------------------------------

if __name__ == "__main__" :
    import sys
    app = QtWidgets.QApplication(sys.argv)
    icon.set_icons()
    test_QIcons()
    sys.exit(0)

#------------------------------
