

"""CommandLineCalib is intended for command line calibration of dark runs

This software was developed for the SIT project.  If you use all or
part of it, please give an appropriate acknowledgment.

@author Mikhail S. Dubrovin
"""
#from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import logging
logger = logging.getLogger(__name__)
#from CalibManager.Logger import logger

import sys
import os
from . import GlobalUtils as gu
from .FileNameManager import fnm
from .ConfigParametersForApp import cp
from . import FileDeployer as fdmets
from .BatchLogScanParser import blsp # Just in order to instatiate it


def str_replace_fields(s, insets={}):
    """1. splits string fields separated by spaces.
       2. each field can be replaced by insets from dictionary.
       3. return (str) of joined fields separated by spaces.
    """
    return ' '.join([insets.get(f,f) for f in s.split(' ')])


def load_text_with_insets(fname, insets={}):
    """
    """
    logger.debug('load_text_with_insets - load_text_file: %s\n  insets: %s' % (fname, str(insets)))
    txt = ''
    fin = open(fname, 'r')
    for s in fin:
        txt += str_replace_fields(s, insets)
    fin.close()
    return txt


def str_filename_with_source(fname, src):
    """
    combines fname like ./work/clb-mfxp16318-r0009-peds-ave.txt and source like MfxEndstation.0:Rayonix.0
    and returns ./work/clb-mfxp16318-r0009-peds-ave-MfxEndstation.0:Rayonix.0.txt
    """
    flds = fname.rsplit('.',1)
    if len(flds)!=2:
       logger.info('str_filename_with_source - no extension found in file name: %s' % str(fname))
       return None
    return '%s-%s.%s' % (flds[0], src, flds[1])


def str_geo_segment_rayonix_v2(shape=(3840,3840), nbins_max=3840, pixsize_um=44.5):
    """In highest resolution mode Rayonix has 3840x3840 pixels of 44.5 um size.
       MTRX:3840:3840:44.5:44.5
       MTRX:1920:1920:89:89
       MTRX:1280:1280:133.5:133.5
       MTRX:960:960:178:178
       MTRX:384:384:445:445
    """
    nrows, ncols = shape
    npix_in_row = nbins_max/nrows
    npix_in_col = nbins_max/ncols
    fmt = 'MTRX:V2:%d:%d'
    fmt += ':%.0f' if npix_in_row%2==0 else ':%.1f'
    fmt += ':%.0f' if npix_in_col%2==0 else ':%.1f'
    return fmt % (nrows, ncols, pixsize_um*npix_in_row, pixsize_um*npix_in_col)


class CommandLineCalib(object):
    """module for dark run processing CLI
    """
    sep = '\n' + 60*'-' + '\n'

    def __init__(self, **kwargs):

        self.name = 'CommandLineCalib'
        cp.commandlinecalib = self

        logging.basicConfig(format='[%(levelname).1s] L%(lineno)04d: %(message)s', level=logging.INFO)

        self.count_msg = 0

        if not self.set_pars(**kwargs): return

        self.print_command_line()
        self.log_rec_on_start()
        self.print_local_pars()
        self.print_list_of_detectors()
        self.print_list_of_xtc_files()
        try: self.print_list_of_sources_from_regdb()
        except: pass

        gu.create_directory(cp.dir_work.value())

        if self.queue is None:
            self.proc_dark_run_interactively()
#        else:
#            if not self.get_print_lsf_status(): return
#            logger.info('process dark in batch queue: %s' % self.queue)
#            self.proc_dark_run_in_batch()
#            self.print_list_of_types_and_sources_from_xtc()

        rayonix_is_in_list = self.pattern_in_sources(ptrn='rayonix')
        if rayonix_is_in_list:
            self.add_files_for_rayonix()
        self.print_list_of_files_dark_in_work_dir()
        self.deploy_calib_files()

        self.save_log_file()
        #self.add_record_in_db()


    def set_pars(self, **kwa):

        #self.print_bits = kwa['print_bits']
        #logger.setPrintBits(self.print_bits)

        docfg = self.loadcfg = kwa['loadcfg']

        self.runnum = kwa.get('runnum', None)
        if self.runnum is None: sys.exit('MISSING PARAMETER "--runnum" or "-r" NEEDS TO BE SPECIFIED')

        self.str_run_number = '%04d' % self.runnum

        if kwa['runrange'] is None:
            self.str_run_range = '%s-end' % self.runnum
        else:
            self.str_run_range = kwa['runrange']

        self.exp_name = cp.exp_name.value_def()
        self.exp_name = cp.exp_name.value() if docfg and kwa['exp'] is None else kwa['exp']
        if self.exp_name is None or self.exp_name == cp.exp_name.value_def():
            logger.critical('\nWARNING: EXPERIMENT NAME IS NOT DEFINED...'\
                     + '\nAdd optional parameter -e <exp-name>')
            return False

        if kwa['detector'] is None:
            self.det_name = cp.det_name.value() if docfg else cp.det_name.value_def()
        else:
            self.det_name = kwa['detector'].replace(","," ")

        list_of_dets_sel = self.det_name.split()
        list_of_dets_sel_lower = [det.lower() for det in list_of_dets_sel]

        #msg = self.sep + 'List of detectors:'
        for det, par in zip(cp.list_of_dets_lower, cp.det_cbx_states_list):
            par.setValue(det in list_of_dets_sel_lower)
            #msg += '\n%s %s' % (det.ljust(10), par.value())
        #logger.info(msg)

        if self.det_name == cp.det_name.value_def():
            logger.critical('\nWARNING: DETECTOR NAMES ARE NOT DEFINED...'\
                     + '\nAdd optional parameter -d <det-names>, ex.: -d CSPAD,CSPAD2x2 etc')
            return False

        self.event_code  = cp.bat_dark_sele.value()  if kwa['event_code']  is None else kwa['event_code']
        self.scan_events = cp.bat_dark_scan.value()  if kwa['scan_events'] is None else kwa['scan_events']
        self.skip_events = cp.bat_dark_start.value() if kwa['skip_events'] is None else kwa['skip_events']
        self.num_events  = cp.bat_dark_end.value() - cp.bat_dark_start.value() if kwa['num_events'] is None else kwa['num_events']
        self.thr_int_min = cp.mask_min_thr.value() if kwa['thr_int_min'] is None else kwa['thr_int_min']
        self.thr_int_max = cp.mask_max_thr.value() if kwa['thr_int_max'] is None else kwa['thr_int_max']
        self.thr_rms_min = cp.mask_rms_thr_min.value() if kwa['thr_rms_min'] is None else kwa['thr_rms_min']
        self.thr_rms_max = cp.mask_rms_thr_max.value() if kwa['thr_rms_max'] is None else kwa['thr_rms_max']
        self.intnlo      = cp.mask_intnlo.value() if kwa['intnlo'] is None else kwa['intnlo']
        self.intnhi      = cp.mask_intnhi.value() if kwa['intnhi'] is None else kwa['intnhi']
        self.rmsnlo      = cp.mask_rmsnlo.value() if kwa['rmsnlo'] is None else kwa['rmsnlo']
        self.rmsnhi      = cp.mask_rmsnhi.value() if kwa['rmsnhi'] is None else kwa['rmsnhi']

        self.workdir     = cp.dir_work.value()  if kwa['workdir'] is None else kwa['workdir']
        #self.queue       = cp.bat_queue.value() if kwa['queue'] is None else kwa['queue']
        self.queue       = kwa['queue']
        #self.logfile     = cp.log_file.value()  if kwa['logfile']  is None else kwa['logfile']

        self.process     = kwa['process']
        self.deploy      = kwa['deploy']
        self.deploygeo   = kwa['deploygeo']
        self.zeropeds    = kwa['zeropeds']
        self.instr_name  = self.exp_name[:3]

        self.timeout_sec = cp.job_timeout_sec.value()

        cp.str_run_number.setValue(self.str_run_number)
        cp.exp_name      .setValue(self.exp_name)
        cp.instr_name    .setValue(self.instr_name)

        self.calibdir     = cp.calib_dir.value() if docfg and kwa['calibdir'] is None else kwa['calibdir']
        if self.calibdir == cp.calib_dir.value_def() or self.calibdir is None:
            self.calibdir = fnm.path_to_calib_dir_default()

        self.xtcdir       = cp.xtc_dir_non_std.value_def() if kwa['xtcdir'] is None else kwa['xtcdir']

        cp.xtc_dir_non_std .setValue(self.xtcdir)
        cp.calib_dir       .setValue(self.calibdir)
        cp.dir_work        .setValue(self.workdir)
        cp.bat_queue       .setValue(self.queue)
        cp.bat_dark_sele   .setValue(self.event_code)
        cp.bat_dark_scan   .setValue(self.scan_events)
        cp.bat_dark_start  .setValue(self.skip_events)
        cp.bat_dark_end    .setValue(self.num_events+self.skip_events)
        cp.mask_min_thr    .setValue(self.thr_int_min)
        cp.mask_max_thr    .setValue(self.thr_int_max)
        cp.mask_rms_thr_min.setValue(self.thr_rms_min)
        cp.mask_rms_thr_max.setValue(self.thr_rms_max)
        cp.det_name        .setValue(self.det_name)
        cp.mask_intnlo     .setValue(self.intnlo)
        cp.mask_intnhi     .setValue(self.intnhi)
        cp.mask_rmsnlo     .setValue(self.rmsnlo)
        cp.mask_rmsnhi     .setValue(self.rmsnhi)

        #cp.log_file      .setValue(self.logfile)

        return True


    def print_local_pars(self):
        msg = self.sep \
        + 'print_local_pars(): Combination of command line parameters and' \
        + '\nconfiguration parameters from file %s (if available after "calibman")' % cp.getParsFileName() \
        + '\n     str_run_number: %s' % self.str_run_number\
        + '\n     runrange      : %s' % self.str_run_range\
        + '\n     exp_name      : %s' % self.exp_name\
        + '\n     instr_name    : %s' % self.instr_name\
        + '\n     workdir       : %s' % self.workdir\
        + '\n     calibdir      : %s' % self.calibdir\
        + '\n     xtcdir        : %s' % self.xtcdir\
        + '\n     det_name      : %s' % self.det_name\
        + '\n     queue         : %s' % self.queue\
        + '\n     num_events    : %d' % self.num_events\
        + '\n     skip_events   : %d' % self.skip_events\
        + '\n     scan_events   : %d' % self.scan_events\
        + '\n     timeout_sec   : %d' % self.timeout_sec\
        + '\n     thr_int_min   : %f' % self.thr_int_min\
        + '\n     thr_int_max   : %f' % self.thr_int_max\
        + '\n     thr_rms_min   : %f' % self.thr_rms_min\
        + '\n     thr_rms_max   : %f' % self.thr_rms_max\
        + '\n     intnlo        : %f' % self.intnlo\
        + '\n     intnhi        : %f' % self.intnhi\
        + '\n     rmsnlo        : %f' % self.rmsnlo\
        + '\n     rmsnhi        : %f' % self.rmsnhi\
        + '\n     process       : %s' % self.process\
        + '\n     deploy        : %s' % self.deploy\
        + '\n     deploygeo     : %s' % self.deploygeo\
        + '\n     zeropeds      : %s' % self.zeropeds\
        + '\n     loadcfg       : %s' % self.loadcfg\
#        + '\n     print_bits    : %s' % self.print_bits
        #+ '\nself.logfile      : ' % self.logfile

        logger.info(msg)


    def print_list_of_detectors(self):
        msg = self.sep + 'List of detectors:'
        for det, par in zip(cp.list_of_dets_lower, cp.det_cbx_states_list):
            msg += '\n%s %s' % (det.ljust(10), par.value())
        logger.info(msg)


    def print_command_line(self):
        msg = 'Command line: %s' % (' '.join(sys.argv))
        logger.info(msg)


    def proc_dark_run_interactively(self):
        from .BatchJobPedestals import BatchJobPedestals

        if self.process:
            logger.info(self.sep + 'Begin dark run data processing interactively')
        else:
            logger.critical(self.sep + '\nWARNING: FILE PROCESSING OPTION IS TURNED OFF...'\
                            + '\nAdd "-P" option in the command line to process files\n')
            return

        self.bjpeds = BatchJobPedestals(self.runnum)
        self.bjpeds.command_for_peds_scan()

        self.print_list_of_types_and_sources_from_xtc()

        if not self.bjpeds.command_for_peds_aver():
            msg = self.sep + 'Subprocess for averaging is completed with warning/error message(s);'\
                  +'\nsee details in the logfile(s).'
            logger.critical(msg)
            #return

        self.print_dark_ave_batch_log()
        return


#    def proc_dark_run_in_batch(self):
#        from .BatchJobPedestals import BatchJobPedestals
#        from time import sleep
#
#        if self.process:
#            self.log(self.sep + 'Begin dark run data processing in batch queue %s' % self.queue,1)
#        else:
#            self.log(self.sep + '\nWARNING: FILE PROCESSING OPTION IS TURNED OFF...'\
#                  + '\nAdd "-P" option in the command line to process files\n',4)
#            return
#
#        self.bjpeds = BatchJobPedestals(self.runnum)
#        self.bjpeds.start_auto_processing()
#
#        sum_dt=0
#        dt = 10 # sec
#        nloops = self.timeout_sec / dt
#        for i in range(nloops):
#            sleep(dt)
#            sum_dt += dt
#            status = self.bjpeds.status_for_peds_files_essential()
#            str_bj_stat, msg_bj_stat = self.bjpeds.status_batch_job_for_peds_aver()
#
#            self.log('%3d sec: Files %s available. %s' % (sum_dt, {False:'ARE NOT', True:'ARE'}[status], msg_bj_stat), 1)
#
#            if status:
#                self.print_dark_ave_batch_log()
#                return
#
#        sys.stdout.write('WARNING: Too many check cycles. Probably LSF is dead...\n')
#
#        #if self.bjpeds.autoRunStage:
#        #self.bjpeds.stop_auto_processing()


    def deploy_calib_files(self):
        #list_of_deploy_commands, list_of_sources = fdmets.get_list_of_deploy_commands_and_sources_dark(self.str_run_number, self.str_run_range)
        #msg = self.sep + 'Tentative deployment commands:\n' + '\n'.join(list_of_deploy_commands)
        #self.log(msg,1)

        if self.deploy:
            logger.info(self.sep + 'Begin deployment of calibration files')
            s = fdmets.deploy_calib_files(self.str_run_number, self.str_run_range, mode='calibrun-dark', ask_confirm=False,\
                                          zeropeds=self.zeropeds, deploygeo=self.deploygeo)
            if s:
                logger.warning('\nProblem with deployment of calibration files...')
            else:
                logger.info('\nDeployment of calibration files is completed',1)
        else:
            logger.critical(self.sep + '\nWARNING: FILE DEPLOYMENT OPTION IS TURNED OFF...'\
                     +'\nAdd "-D" option in the command line to deploy files\n')


    def save_log_file(self, verb=True):
        # save log in local file
        logfname = fnm.log_file()
        msg = 'See details in log-file: %s' % logfname
        #self.log(msg,4) # set it 4-warning - always print
        logger.critical(msg) # warning - always print



        ###### logger.saveLogInFile(logfname)

        # save log in /reg/g/psdm/logs/calibman/<year>/<month>/<log-file-name>.txt
        path = fnm.log_file_cpo()
        if gu.create_path(path):
            ###### logger.saveLogInFile(path)
            if verb: sys.stdout.write('Log file: %s\n' % path)
        else: logger.warning('onSave: path for log file %s was not created.' % path)


    def log_rec_on_start(self):
        #import CalibManager.GlobalUtils as gu
        msg = 'user: %s@%s  cwd: %s\n    command: %s'%\
              (gu.get_login(), gu.get_hostname(), gu.get_cwd(), ' '.join(sys.argv))
        logger.info(msg)


    def pattern_in_sources(self, ptrn='rayonix'):
        lst_of_srcs = cp.blsp.list_of_sources_for_selected_detectors() # ['MfxEndstation.0:Rayonix.0']
        lst_bool = [(ptrn.lower() in s.lower()) for s in lst_of_srcs]
        logger.debug('pattern_in_sources - all sources: %s conditions: %s' % (str(lst_of_srcs),str(lst_bool)))
        return any(lst_bool)


    def add_files_for_rayonix(self):
        """ Using shape of array for evaluated pedestals, add in the work directory additional files for Rayonix
            with zero peds and geometry
        """
        from PSCalib.NDArrIO import load_txt, save_txt #, list_of_comments
        from . import AppDataPath as apputils
        fname_geo  = str(apputils.AppDataPath('CalibManager/scripts/geometry-rayonix.template').path())
        logger.info('%s\nfname_geo: %s' % (100*'_', fname_geo))

        lst_of_srcs = cp.blsp.list_of_sources_for_selected_detectors() # ['MfxEndstation.0:Rayonix.0']
        logger.debug('all sources: %s' % str(lst_of_srcs))

        for s in lst_of_srcs:
            if not('rayonix' in s.lower()):
                logger.info('skip - rayonix is not found in: %s' % s)
                continue

            lst_peds_ave = gu.get_list_of_files_for_list_of_insets(fnm.path_peds_ave(), [s,])
            if not isinstance(lst_peds_ave, list):
                logger.warning('lst_peds_ave is not a list: %s' % str(lst_peds_ave))
                continue

            if len(lst_peds_ave)<1:
                logger.warning('add_files_for_rayonix - lst_peds_ave is empty')
                continue

            # load array with pedestals
            fname_peds_ave = lst_peds_ave[0]
            ave = load_txt(str(fname_peds_ave))
            logger.info('pedestals.shape:%s dtype:%s' % (ave.shape, ave.dtype))

            if self.zeropeds:
                # make/save zero-pedestals
                fname_peds_zero = str_filename_with_source(fnm.path_peds_zero(), s)
                logger.info('fname_peds_zeros:%s' % fname_peds_zero)
                save_txt(fname_peds_zero, gu.np.zeros_like(ave), cmts=(), fmt='%.0f')
                os.chmod(fname_peds_zero, 0o664)

            # make/save default geometry
            if self.deploygeo:
                geo_segment = str_geo_segment_rayonix_v2(shape=ave.shape)
                str_geo = load_text_with_insets(fname_geo, insets={'SEGMENT_V2':geo_segment})
                logger.debug('str_geo:\n%s' % str_geo)
                fname_geometry  = str_filename_with_source(fnm.path_geometry(), s)
                logger.info('fname_geometry  :%s' % fname_geometry)
                gu.save_textfile(str_geo, fname_geometry, mode='w', accmode=0o664)


    def print_list_of_files_dark_in_work_dir(self):
        lst = self.get_list_of_files_dark_in_work_dir()
        msg = self.sep + 'List of files in work directory for command "ls %s*"' % fnm.path_prefix_dark()
        if lst == []: msg += ' is empty'
        else        : msg += ':\n' + '\n'.join(lst)
        logger.info(msg)


    def get_list_of_files_dark_in_work_dir(self):
        path_prexix = fnm.path_prefix_dark()
        dir, prefix = os.path.split(path_prexix)
        return gu.get_list_of_files_in_dir_for_part_fname(dir, pattern=prefix)


    def get_list_of_files_dark_expected(self):
        lst_of_srcs = cp.blsp.list_of_sources_for_selected_detectors()
        return fnm.get_list_of_files_peds() \
             + gu.get_list_of_files_for_list_of_insets(fnm.path_peds_ave(),    lst_of_srcs) \
             + gu.get_list_of_files_for_list_of_insets(fnm.path_peds_rms(),    lst_of_srcs) \
             + gu.get_list_of_files_for_list_of_insets(fnm.path_hotpix_mask(), lst_of_srcs) \
             + gu.get_list_of_files_for_list_of_insets(fnm.path_peds_cmod(),   lst_of_srcs)


    def print_list_of_types_and_sources_from_xtc(self):
        txt = self.sep + 'Data Types and Sources from xtc scan of the\n' \
            + cp.blsp.txt_list_of_types_and_sources()
        logger.info(txt)


    def print_list_of_sources_from_regdb(self):
        txt = self.sep + 'Sources from DB:' \
            + cp.blsp.txt_of_sources_in_run()
        logger.info(txt)


    def print_dark_ave_batch_log(self):
        path = fnm.path_peds_aver_batch_log()
        if not os.path.exists(path):
            msg = 'File: %s does not exist' % path
            logger.warning(msg)
            return

        txt = self.sep + 'psana log file %s:\n\n' % path \
            + gu.load_textfile(path) \
            + 'End of psana log file %s' % path
        logger.info(txt)


#    def get_print_lsf_status(self):
#        queue = cp.bat_queue.value()
#        farm = cp.dict_of_queue_farm[queue]
#        msg, status = gu.msg_and_status_of_lsf(farm, print_bits=0)
#        msgi = self.sep + 'LSF status for queue %s on farm %s: \n%s\nLSF status for %s is %s'\
#               % (queue, farm, msg, queue, {False:'bad',True:'good'}[status])
#        self.log(msgi,1)
#
#        msg, status = gu.msg_and_status_of_queue(queue)
#        self.log('\nBatch queue status, %s'%msg, 1)
#
#        return status


    def print_list_of_xtc_files(self):
        pattern = '-r%s' % self.str_run_number
        lst = fnm.get_list_of_xtc_files()
        lst_for_run = [path for path in lst if pattern in os.path.basename(path)]
        txt = self.sep + 'List of xtc files for exp=%s:run=%s:\n' % (self.exp_name, self.str_run_number)
        txt += '\n'.join(lst_for_run)
        logger.info(txt)


#    def log(self, msg, level=1):
#        """Internal logger - re-direct all messages to the project logger, critical messages"""
#        #logger.levels = ['debug','info','warning','error','critical']
#        self.count_msg += 1
#        #print 'Received msg: %d' % self.count_msg
#        #if self.print_bits & 1 or level==4: print msg
#
#        if   level==1: logger.info    (msg, __name__)
#        elif level==4: logger.critical(msg, __name__)
#        elif level==0: logger.debug   (msg, __name__)
#        elif level==2: logger.warning (msg, __name__)
#        elif level==3: logger.error   (msg, __name__)
#        else         : logger.info    (msg, __name__)

# EOF
