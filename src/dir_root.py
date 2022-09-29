"""define DIR_ROOT for repositories and logfiles through the environment variable:
   #source /reg/g/psdm/sw/conda1/manage/bin/psconda.sh # old releases
   #source /cds/sw/ds/ana/conda1/manage/bin/psconda.sh # ana-4.0.46-py3
      export SIT_ROOT=/reg/g/psdm/
      export SIT_DATA=/cds/group/psdm/data/
      export SIT_PSDM_DATA=/cds/data/psdm/

   #source /sdf/group/lcls/ds/ana/sw/conda1/manage/bin/psconda.sh
      export SIT_ROOT=/sdf/group/lcls/ds/ana/
      export SIT_DATA=/sdf/group/lcls/ds/ana/data/
      export SIT_PSDM_DATA=/sdf/data/lcls/ds/

   /sdf/data/lcls/ds/xpp/xpptut15/xtc/e665-r0240-s00-c00.xtc

   from CalibManager.dir_root import DIR_REPO, DIR_PSDM_DATA
"""

from Detector.dir_root import *  # os, DIR_ROOT, DIR_REPO, DIR_LOG_AT_START

DIR_PSDM_DATA = os.getenv('SIT_PSDM_DATA').rstrip('/')  # /sdf/data/lcls/ds

# EOF
