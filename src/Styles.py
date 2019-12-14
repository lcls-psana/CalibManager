#------------------------------
"""
Usage ::
    from CalibManager.Styles import style
    # then get (str) styles
    style1 = style.styleEditBad
    style2 = style.styleButtonGood

@see class :py:class:`CalibManager.Styles`

@see project modules
    * :py:class:`CalibManager.ConfigParameters`

This software was developed for the SIT project.
If you use all or part of it, please give an appropriate acknowledgment.

@version $Id:Styles.py 11923 2016-11-22 14:28:00Z dubrovin@SLAC.STANFORD.EDU $

@author Mikhail S. Dubrovin
"""
#------------------------------

class Styles(object) :
    """Storage of CalibManager styles.
    """
    def __init__(self) :
        self._name = self.__class__.__name__
        self.set_styles()

#------------------------------
    def set_styles(self) :

        self.styleYellowish = "background-color: rgb(255, 255, 220); color: rgb(0, 0, 0);" # Yellowish
        self.stylePink      = "background-color: rgb(255, 200, 220); color: rgb(0, 0, 0);" # Pinkish
        self.styleYellowBkg = "background-color: rgb(240, 240, 100); color: rgb(0, 0, 0);" # YellowBkg
        self.styleGreenMy   = "background-color: rgb(150, 250, 230); color: rgb(0, 0, 0);" # My
        self.styleGray      = "background-color: rgb(230, 240, 230); color: rgb(0, 0, 0);" # Gray
        self.styleGreenish  = "background-color: rgb(100, 240, 200); color: rgb(0, 0, 0);" # Greenish
        self.styleGreenPure = "background-color: rgb(150, 255, 150); color: rgb(0, 0, 0);" # Green
        self.styleBluish    = "background-color: rgb(220, 220, 250); color: rgb(0, 0, 0);" # Bluish
        self.styleWhite     = "background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);"
        self.styleRedBkgd   = "background-color: rgb(255,   0,   0); color: rgb(0, 0, 0);" # Red background
        self.styleReddish   = "background-color: rgb(220,   0,   0); color: rgb(0, 0, 0);" # Reddish background
        self.styleTransp    = "background-color: rgb(255,   0,   0, 100);"
        self.styleDefault   = "" # "background-color: rgb(239, 235, 231, 255); color: rgb(0, 0, 0);" # Gray bkgd
        self.styleStat      = "color: rgb(0, 0, 256); background-color: rgb(230, 240, 230);" # Gray
        self.styleBkgdGray  = "background-color: rgb(50, 50, 50);" # Gray

        self.styleBlue      = "color: rgb(100, 0, 150);"
        self.styleBlueM     = "color: rgb(200, 0, 150);"
        self.styleBuriy     = "color: rgb(150, 100, 50);"
        self.styleRed       = "color: rgb(255, 0, 0);"
        self.styleGreen     = "color: rgb(0, 150, 0);"
        self.styleYellow    = "color: rgb(0, 150, 150);"

        self.styleBkgd         = self.styleDefault # self.styleGreenMy # styleYellowish
        self.styleTitle        = self.styleBlueM
        self.styleLabel        = self.styleBlue
        self.styleEdit         = self.styleWhite
        self.styleEditInfo     = self.styleBkgd # self.styleGreenish # Bluish
        self.styleEditBad      = self.styleRedBkgd
        self.styleButton       = self.styleGray
        self.styleButtonLeft   = self.styleButton + 'text-align: left;'
        self.styleButtonOn     = self.styleBluish
        self.styleButtonClose  = self.stylePink
        self.styleButtonWarning= self.styleYellowBkg
        self.styleButtonGood   = self.styleGreenPure
        self.styleButtonBad    = self.styleReddish # self.stylePink
        self.styleBox          = self.styleGray
        self.styleCBox         = self.styleYellowish
        self.styleStatusGood   = self.styleGreen
        self.styleStatusWarning= self.styleYellow
        self.styleStatusAlarm  = self.styleRed
        self.styleTitleBold    = self.styleTitle + 'font-size: 18pt; font-family: Courier; font-weight: bold;'
        self.styleWhiteFixed   = self.styleWhite + 'font-family: Fixed;'
        self.styleTitleInFrame = self.styleWhite # self.styleDefault # self.styleWhite # self.styleGray

        self.styleStat         = self.styleBkgdGray + "color: white;"

        #self.colorEditInfo     = QtGui.QColor(100, 255, 200)
        #self.colorEditBad      = QtGui.QColor(255,   0,   0)
        #self.colorEdit         = QtGui.QColor('white')
        #self.colorTabItem      = QtGui.QColor('white')

#------------------------------
style = Styles()
#------------------------------
