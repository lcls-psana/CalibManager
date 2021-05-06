#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#   AppDataPath...
#------------------------------------------------------------------------

"""AppDataPath class represents a path to a file that can be found in
one of the $SIT_DATA locations.

@version $Id$

@author Andy Salnikov
"""

import os

#-----------------------------

class AppDataPath(object) :
    """
    AppDataPath class represents a path to a file that can be found in one of the $SIT_DATA locations.
    """

    def __init__(self, relPath) :
        """Constructor takes relative file path."""
        self.m_path = ""
        
        dataPath = './data:../../data:' + os.getenv("SIT_DATA")
        if not dataPath: return
            
        for dir in dataPath.split(':'):
            path = os.path.join(dir, relPath)
            if os.path.exists(path):
                self.m_path = path
                break
            

    def path(self) :
        """Returns path of the existing file or empty string"""
        return self.m_path

#------------------------------

if __name__ == "__main__" :
    import sys
    sys.exit("Module is not supposed to be run as main module")

#------------------------------
