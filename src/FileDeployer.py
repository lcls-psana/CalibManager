from __future__ import absolute_import
#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#   FileDeployer ...
#------------------------------------------------------------------------

#--------------------------------
__version__ = "$Revision$"
#--------------------------------
#import sys
import os
import stat
#import socket

from .ConfigParametersForApp import cp
from   .Logger               import logger
from . import GlobalUtils          as     gu
from .FileNameManager        import fnm

#------------------------------

def get_list_of_deploy_commands_and_sources_dark(str_run_number, str_run_range):
    """Get list of deploy commands for all detectors of the same type"""

    cp.str_run_number.setValue(str_run_number)
    #cp.blsp.print_list_of_types_and_sources()
    list_of_dtypes, list_of_sources, list_of_ctypes = cp.blsp.list_of_types_and_sources_for_selected_detectors()
    # list_of_dtypes  : ['CsPad::DataV1',    'CsPad::DataV1']
    # list_of_sources : ['CxiDs1.0:Cspad.0', 'CxiDsd.0:Cspad.0']
    # list_of_ctypes  : ['CsPad::CalibV1',   'CsPad::CalibV1']

    #print 'list_of_dtypes  :', list_of_dtypes
    #print 'list_of_sources:',  list_of_sources
    #print 'list_of_ctypes :',  list_of_ctypes

    list_of_deploy_commands  = get_list_of_deploy_commands_for_calibtype(list_of_ctypes, list_of_dtypes, list_of_sources, fnm.path_peds_ave(), 'pedestals', str_run_range)
    list_of_deploy_commands += get_list_of_deploy_commands_for_calibtype(list_of_ctypes, list_of_dtypes, list_of_sources, fnm.path_peds_rms(), 'pixel_rms', str_run_range)

    if cp.dark_deploy_hotpix.value() :
      list_of_deploy_commands += get_list_of_deploy_commands_for_calibtype(list_of_ctypes, list_of_dtypes, list_of_sources, fnm.path_hotpix_mask(), 'pixel_status', str_run_range)

    if cp.dark_deploy_cmod.value() :
      list_of_deploy_commands += get_list_of_deploy_commands_for_calibtype(list_of_ctypes, list_of_dtypes, list_of_sources, fnm.path_peds_cmod(), 'common_mode', str_run_range)

    return list_of_deploy_commands, list_of_sources
    
#------------------------------

def get_list_of_deploy_commands_and_sources_dark_dcs(str_run_number, str_run_range, mode='dark'):
    """Get list of deploy commands for all detectors of the same type"""

    cp.str_run_number.setValue(str_run_number)
    #cp.blsp.print_list_of_types_and_sources()
    list_of_dtypes, list_of_sources, list_of_ctypes = cp.blsp.list_of_types_and_sources_for_selected_detectors()

    list_of_deploy_commands  = get_list_of_deploy_commands_for_calibtype_dcs(list_of_sources, fnm.path_peds_ave(), 'pedestals', str_run_range, mode)
    list_of_deploy_commands += get_list_of_deploy_commands_for_calibtype_dcs(list_of_sources, fnm.path_peds_rms(), 'pixel_rms', str_run_range, mode)

    if cp.dark_deploy_hotpix.value() :
      list_of_deploy_commands += get_list_of_deploy_commands_for_calibtype_dcs(list_of_sources, fnm.path_hotpix_mask(), 'pixel_status', str_run_range, mode)

    if cp.dark_deploy_cmod.value() :
      list_of_deploy_commands += get_list_of_deploy_commands_for_calibtype_dcs(list_of_sources, fnm.path_peds_cmod(), 'common_mode', str_run_range, mode)

    return list_of_deploy_commands, list_of_sources
    
#-----------------------------

def get_list_of_deploy_commands_and_sources(str_run_number, str_run_range, mode='dark'):
    if mode=='calibman-dark' or \
       mode=='calibrun-dark' : return get_list_of_deploy_commands_and_sources_dark(str_run_number, str_run_range)
    else                     : return [], []

#-----------------------------

def get_list_of_deploy_commands_and_sources_dcs(str_run_number, str_run_range, mode='dark'):
    if mode=='calibman-dark' or \
       mode=='calibrun-dark' : return get_list_of_deploy_commands_and_sources_dark_dcs(str_run_number, str_run_range, mode)
    else                     : return [], []

#-----------------------------
#-----------------------------
#-----------------------------

def deploy_calib_files(str_run_number, str_run_range, mode='calibrun-dark', ask_confirm=True):
    """Deploys the calibration file(s)"""

    list_of_deploy_commands, list_of_sources = get_list_of_deploy_commands_and_sources(str_run_number, str_run_range, mode)
    msg = 'Deploy calibration file(s):'

    if list_of_deploy_commands == [] :
        msg += 'List of commands IS EMPTY !!!'  
        logger.info(msg, __name__)
        return 1
    
    msg =  '\nTentative deployment commands:\n' + '\n'.join(list_of_deploy_commands)
    logger.info(msg, __name__)

    list_src_cbx = [[src,True] for src in list_of_sources]
    if ask_confirm :
        resp = gu.changeCheckBoxListInPopupMenu(list_src_cbx, win_title='Confirm depl. for:')
        if resp != 1 :
            logger.info('Deployment is cancelled!', __name__)
            return 2

    for cmd in list_of_deploy_commands :
        #print 'cmd: ', cmd
        if is_allowed_command(cmd, list_src_cbx) : fd.procDeployCommand(cmd, mode)

    #---->>> DCS hdf5 file deployment
    return deploy_calib_files_dcs(str_run_number, str_run_range, mode, list_src_cbx)

#-----------------------------

def deploy_calib_files_dcs(str_run_number, str_run_range, mode, list_src_cbx):
    """Deploys the calibration file(s) in the Detector Calibration Store
       e.g.: dcs add -e mfxn8316 -r 11 -d Epix100a -t pixel_status -v 4 -f my-nda.txt -m "my comment" -c ./calib
    """
    
    list_of_deploy_commands, list_of_sources = get_list_of_deploy_commands_and_sources_dcs(str_run_number, str_run_range, mode)

    if list_of_deploy_commands == [] :
        msg += 'List of DCS deploy commands IS EMPTY !!!'  
        logger.info(msg, __name__)
        return 3
    
    msg =  '\nTentative DCS deployment commands:\n' + '\n'.join(list_of_deploy_commands)
    logger.info(msg, __name__)

    if False: # 2020-10-15
      for cmd in list_of_deploy_commands :
        #print 'cmd: ', cmd
        if is_allowed_command_dcs(cmd, list_src_cbx) : procDeployCommandDCS(cmd, mode)
    else:
        logger.warning('automatic deployment to DCS/HDF5 is turned off', __name__)

    return 0

#-----------------------------

def procDeployCommandDCS(cmd, mode) :
    #os.system(cmd_cat)
    stream = os.popen(cmd)
    resp = stream.read()
    msg = '%s\n%s' % (cmd, resp) if resp else cmd
    logger.info(msg, 'procDeployCommandDCS')

#-----------------------------

def is_allowed_command_dcs(cmd, list_src_cbx):
    """Check the deployment command is for selected src"""

    fields  = cmd.split()
    infname = fields[11] # for example:  ./work/clb-cxib2313-r0010-mask-hot-thr-0.00ADU-CxiDs1.0:Cspad.0.txt 
    if not os.path.exists(infname) :
        msg = '\nWARNING: INPUT FILE %s DOES NOT EXIST... Is not deployed.\n' % infname
        logger.warning(msg, __name__)
        return False

    for src,cbx in list_src_cbx :
        if cbx : return True
        #if src in destination : return True

    return False

#-----------------------------
#-----------------------------
#-----------------------------
#-----------------------------

def is_allowed_command(cmd, list_src_cbx):
    """Check the deployment command is for selected src"""

    fields  = cmd.split()
    infname = fields[1] # for example:  ./work/clb-cxib2313-r0010-mask-hot-thr-0.00ADU-CxiDs1.0:Cspad.0.txt 
    if not os.path.exists(infname) :
        msg = '\nWARNING: INPUT FILE %s DOES NOT EXIST... Is not deployed.\n' % infname
        logger.warning(msg, __name__)
        return False

    destination = fields[2] # for example: /reg/d/psdm/CXI/cxib2313/calib/CsPad::CalibV1/CxiDsd.0:Cspad.0/pedestals/1-1.data
    for src,cbx in list_src_cbx :
        if not cbx : continue
        if src in destination : return True
    return False


def get_list_of_deploy_commands_for_calibtype(list_of_ctypes, list_of_types, list_of_sources, base_path, calibtype='pedestals', str_run_range='0-end'):
    """Get list of deploy commands for lists of type and sources for calibtype"""
    
    list_of_files = gu.get_list_of_files_for_list_of_insets(base_path, list_of_sources)

    list_of_deploy_commands = []

    for file, ctype, type, source in zip(list_of_files, list_of_ctypes, list_of_types, list_of_sources) :
        # Ex.: ctype='Epix100a::CalibV1',  type='Epix::ElementV2',  source='NoDetector.0:Epix100a.0'

        #pos1 = source.find(':')
        #pos2 = source.find('.',pos1)
        #typ  = source[pos1+1:pos2] + '::CalibV1' # Ex.: typ='Epix100a::CalibV1'

        if calibtype == 'common_mode' and gu.cgu.det_type_from_source(source) not in cp.list_of_depl_cmod : continue

        fname = '%s.data' % str_run_range
        
        calib_path = os.path.join(cp.calib_dir.value(), ctype, source, calibtype, fname)
        cmd = 'cp %s %s' % (file, calib_path)

        list_of_deploy_commands.append(cmd)

    return list_of_deploy_commands

#-----------------------------
#-----------------------------
#-----------------------------
#-----------------------------

def get_list_of_deploy_commands_for_calibtype_dcs(list_of_sources, base_path, calibtype='pedestals', str_run_range='0-end', mode='dark'):
    """Get list of deploy commands for lists of type and sources for calibtype"""
    
    list_of_files = gu.get_list_of_files_for_list_of_insets(base_path, list_of_sources)

    list_of_deploy_commands = []

    for file, source in zip(list_of_files, list_of_sources) :
        # Ex. source: 'NoDetector.0:Epix100a.0'
        # Ex. file  : './work/clb-mfxn8316-r0014-peds-sta-MfxEndstation.0:Epix100a.0.txt'
        if calibtype == 'common_mode' and gu.cgu.det_type_from_source(source) not in cp.list_of_depl_cmod : continue

        #fname = '%s.data' % str_run_range        
        #calib_path = os.path.join(cp.calib_dir.value(), ctype, source, calibtype, fname)

        # ex.: dcs add -e mfxn8316 -r 11 -d Epix100a -t pixel_status -v 4 -f my-nda.txt -m "my comment" -c ./calib
        cmd = 'dcs add -e %s' % cp.exp_name.value()\
            +  ' -r %s' % cp.str_run_number.value().lstrip('0')\
            +  ' -d %s' % source\
            +  ' -t %s' % calibtype\
            +  ' -f %s' % file\
            +  ' -m %s' % mode\
            +  ' -c %s' % cp.calib_dir.value()\
            +  ' -i'

        list_of_deploy_commands.append(cmd)

    return list_of_deploy_commands

#-----------------------------

class FileDeployer(object) :
    """Collection of methods for file deployment in calibration directory tree"""

    def __init__ ( self ) :
        pass

    
    def procDeployCommand(self, cmd, comment='dark'):
        """Accepts command like 'cp path_inp path_out' and replace it by command 'cat path_inp > path_out'"""
        
        cmd_seq = cmd.split()
        action, path_inp, path_out = cmd_seq
        #------------------------------------------------------------------------------------
        # USE cat in stead of cp and move in order to create output file with ACL permissions
        #------------------------------------------------------------------------------------
        cmd_cat = 'cat %s > %s' % (path_inp, path_out)

        dir_ctype, fname      = path_out  .rsplit('/',1)
        dir_src,   calib_type = dir_ctype .rsplit('/',1)
        dir_dtype, src        = dir_src   .rsplit('/',1)
        dir_calib, dtype      = dir_dtype .rsplit('/',1)

        #print 'path_out : ', path_out
        #print 'fname    : ', fname
        #print 'dir_ctype: ', dir_ctype
        #print 'dir_src  : ', dir_src
        #print 'dir_dtype: ', dir_dtype
        #print 'dir_calib: ', dir_calib

        # Create output directory tree if it does not exist
        list_of_dirs = [dir_calib, dir_dtype, dir_src, dir_ctype]

        for dir in list_of_dirs :
            dir_exists = os.path.exists(dir) 
            #print dir, dir_exists
            if not dir_exists :
                gu.create_directory(dir)

        #out, err = gu.subproc(cmd_cat.split())
        #if err != '' : msg += '\nERROR: ' + err
        #if out != '' : msg += '\nRESPONCE: ' + out

        #os.system(cmd_cat)
        stream = os.popen(cmd_cat)
        resp = stream.read()
        msg = 'Command: %s\n%s' % (cmd_cat,resp)
        logger.info(msg, __name__)

        if action == 'mv' and resp == '' : os.system('rm %s'%(path_inp))
        #self.changeFilePermissions(path_out)
        self.addHistoryRecord(cmd, comment)


    def changeFilePermissions(self, path, mode=660):
        cmd = 'chmod %d %s' % (mode,path)
        msg = 'Change permissions for file: %s' % cmd
        logger.info(msg, __name__)
        os.system(cmd)


    def addHistoryRecord(self, cmd, comment='dark'):
        #print 'cmd  = ', cmd
        fname_history  = cp.fname_history.value()
        if fname_history == '' : return

        exp_name       = cp.exp_name.value()
        str_run_number = cp.str_run_number.value()

        user   = gu.get_login()
        login  = gu.get_login()
        host   = gu.get_hostname()
        tstamp = gu.get_current_local_time_stamp(fmt='%Y-%m-%dT%H:%M:%S  zone:%Z')

        cmd_cp, path_inp, path_out = cmd.split() 
        dir_inp, fname_inp = path_inp.rsplit('/',1)
        dir_out, fname_out = path_out.rsplit('/',1) 
        path_history = os.path.join(dir_out,fname_history)

        rec = 'file:%s  copy_of:%s  exp:%s  run:%s  comment:%s  user:%s  host:%s  cptime:%s\n' % \
              (fname_out.ljust(14),
               path_inp,
               #fname_inp,
               exp_name.ljust(8),
               str_run_number.ljust(4),
               comment.ljust(10),
               user,
               host,
               tstamp.ljust(29))

        #print 'user           = ', user
        #print 'login          = ', login
        #print 'host           = ', host
        #print 'fname_inp      = ', fname_inp
        #print 'fname_out      = ', fname_out
        #print 'dir_out        = ', dir_out
        #print 'tstamp         = ', tstamp
        #print 'exp_name       = ', exp_name
        #print 'str_run_number = ', str_run_number
        #print 'path_history   = ', path_history
        #print 'rec            = ', rec

        msg = 'Add record: \n%s to history file: %s' % (rec,path_history)
        logger.info(msg, __name__)

        gu.save_textfile(rec, path_history, mode='a')

        #self.changeFilePermissions(path_history)


    def addHistoryRecordOnDelete(self, cmd, comment='file-manager'):
        """Add record in the hystory file on delete command if the hystory file exists
        """
        #print 'cmd  = ', cmd
        fname_history  = cp.fname_history.value()
        if fname_history == '' : return

        user   = gu.get_login()
        login  = gu.get_login()
        host   = gu.get_hostname()
        tstamp = gu.get_current_local_time_stamp(fmt='%Y-%m-%dT%H:%M:%S  zone:%Z')

        cmd_rm, path = cmd.split() 
        dir, fname = path.rsplit('/',1)
        path_history = os.path.join(dir,fname_history)

        if not os.path.exists(path_history) : return

        rec = 'file:%s  cmd:%s  comment:%s  user:%s  host:%s  cptime:%s\n' % \
              (fname.ljust(14),
               cmd_rm.ljust(4),
               comment.ljust(10),
               user,
               host,
               tstamp.ljust(29))

        msg = 'Add record: \n%s to history file: %s' % (rec, path_history)
        logger.info(msg, __name__)

        gu.save_textfile(rec, path_history, mode='a')

        #self.changeFilePermissions(path_history)

#-----------------------------

fd = FileDeployer()

#-----------------------------


        
