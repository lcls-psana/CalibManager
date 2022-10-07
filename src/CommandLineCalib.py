
"""CommandLineCalib is intended for command line calibration of dark runs

This software was developed for the LCLS project.
If you use all or part of it, please give an appropriate acknowledgment.

@author Mikhail Dubrovin
"""
#from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import logging
logger = logging.getLogger(__name__)

import os
import sys
import CalibManager.GlobalUtils as gu
import CalibManager.FileDeployer as fdmets
from CalibManager.FileNameManager import fnm
from CalibManager.ConfigParametersForApp import cp
from CalibManager.BatchLogScanParser import blsp # Just in order to instatiate it


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


def pattern_in_sources(ptrn='rayonix'):
    lst_of_srcs = cp.blsp.list_of_sources_for_selected_detectors() # ['MfxEndstation.0:Rayonix.0']
    lst_bool = [(ptrn.lower() in s.lower()) for s in lst_of_srcs]
    logger.debug('pattern_in_sources - all sources: %s conditions: %s' % (str(lst_of_srcs),str(lst_bool)))
    return any(lst_bool)


def print_list_of_detectors(sep='--'):
    msg = sep + 'List of detectors:'
    for det, par in zip(cp.list_of_dets_lower, cp.det_cbx_states_list):
        msg += '\n%s %s' % (det.ljust(10), par.value())
    logger.info(msg)


def print_list_of_xtc_files(title='List of xtc files'):
    pattern = '-r%s' % cp.str_run_number.value()
    lst = fnm.get_list_of_xtc_files()
    lst_for_run = [path for path in lst if pattern in os.path.basename(path)]
    logger.info(title + '\n'.join(lst_for_run))


def print_list_of_sources_from_regdb(sep='--'):
    txt = sep + 'Sources from DB:'
    try: txt += cp.blsp.txt_of_sources_in_run()
    except: txt += 'N/A'
    logger.info(txt)


def get_list_of_files_dark_in_work_dir():
    path_prexix = fnm.path_prefix_dark()
    dir, prefix = os.path.split(path_prexix)
    return gu.get_list_of_files_in_dir_for_part_fname(dir, pattern=prefix)


#def get_list_of_files_dark_expected():
#    lst_of_srcs = cp.blsp.list_of_sources_for_selected_detectors()
#    return fnm.get_list_of_files_peds() \
#         + gu.get_list_of_files_for_list_of_insets(fnm.path_peds_ave(),    lst_of_srcs) \
#         + gu.get_list_of_files_for_list_of_insets(fnm.path_peds_rms(),    lst_of_srcs) \
#         + gu.get_list_of_files_for_list_of_insets(fnm.path_hotpix_mask(), lst_of_srcs) \
#         + gu.get_list_of_files_for_list_of_insets(fnm.path_peds_cmod(),   lst_of_srcs)


def print_list_of_files_dark_in_work_dir(sep='--'):
    lst = get_list_of_files_dark_in_work_dir()
    msg = sep + 'List of files in work directory for command "ls %s*"' % fnm.path_prefix_dark()
    if lst == []: msg += ' is empty'
    else        : msg += ':\n' + '\n'.join(lst)
    logger.info(msg)


def print_dark_ave_log(sep='--'):
    path = fnm.path_peds_aver_log()
    if not os.path.exists(path):
        msg = 'File: %s does not exist' % path
        logger.warning(msg)
        return
    txt = sep + 'psana log file %s:\n\n' % path \
        + gu.load_textfile(path) \
        + 'End of psana log file %s' % path
    logger.info(txt)


def str_command_for_peds_scan():
    """Returns str command for scan, for example:
       event_keys -d exp=mecj5515:run=102:stream=0-79:smd -n 1000 -s 0 -m 1 -p EventKey
    """
    dsname = fnm.path_to_data_files()       # exp=mecj5515:run=102:stream=0-79:smd
    evskip = cp.bat_dark_start.value() - 1
    events = cp.bat_dark_scan.value()
    logscn = fnm.path_peds_scan_log() # log file name for scan

    command = 'event_keys -d %s -n %s -s %s -m 1 -p EventKey' % (dsname, str(events), str(evskip))

    msg = 'Scan xtc file(s) using command:\n%s' % command \
        + '\nand save results in the log-file: %s' % logscn
    logger.info(msg)
    return command


def command_for_peds_scan():
    str_run_number = cp.str_run_number.value()
    command = str_command_for_peds_scan()
    logname = fnm.path_peds_scan_log() # log file name for scan
    err = gu.subproc_in_log(command.split(), logname) # , shell=True)

    err = str(err) # convert byte to str for py3
    if err != '':
        if 'ERR' in err:
            logger.error('\nERROR message from scan:\n%s' % (err))
            #self.stop_auto_processing(is_stop_on_button_click=False)
            logger.warning('Autoprocessing for run %s is stopped due to error at execution of the scan command'\
                           % str_run_number)
            return False
        else:
            logger.debug('Message from scan: %s' % (err))

    logger.info('Scan for run %s is completed' % str_run_number)
    return True


def str_of_sources():
    """Returns comma separated sources. For example
       'CxiDg2.0:Cspad2x2.0,CxiEndstation.0:Opal4000.1'
    """
    list_of_all_srcs = []
    for det_name in cp.list_of_dets_selected():
        lst_types, lst_srcs, lst_ctypes = cp.blsp.list_of_types_and_sources_for_detector(det_name)
        #list_path_peds_ave    = gu.get_list_of_files_for_list_of_insets(fnm.path_peds_ave(),    lst_srcs)
        #list_path_peds_rms    = gu.get_list_of_files_for_list_of_insets(fnm.path_peds_rms(),    lst_srcs)
        #list_path_hotpix_mask = gu.get_list_of_files_for_list_of_insets(fnm.path_hotpix_mask(), lst_srcs)
        list_of_all_srcs += lst_srcs
    return ','.join(list_of_all_srcs)


def str_command_for_peds_aver():
    """Returns str command for dark run average, for example:
       det_ndarr_raw_proc -d exp=mecj5515:run=102:stream=0-79:smd -s MecTargetChamber.0:Cspad.0\
                          -n 6 -m 0 -f ./work/clb-#exp-#run-peds-#type-#src.txt
    """

    dsname = fnm.path_to_data_files()       # 'exp=mecj5515:run=102:stream=0-79:smd'
    evskip = cp.bat_dark_start.value() - 1
    events = cp.bat_dark_end.value()
    fntmpl = fnm.path_peds_template()       # './work/clb-#exp-#run-peds-#type-#src.txt'
    srcs   = str_of_sources()               # 'MecTargetChamber.0:Cspad.0,MecTargetChamber.0:Cspad.1'
    logave = fnm.path_peds_aver_log() # log file name for averaging
    int_lo = cp.mask_min_thr.value()
    int_hi = cp.mask_max_thr.value()
    rms_lo = cp.mask_rms_thr_min.value()
    rms_hi = cp.mask_rms_thr_max.value()
    rmsnlo = cp.mask_rmsnlo.value()
    rmsnhi = cp.mask_rmsnhi.value()
    intnlo = cp.mask_intnlo.value()
    intnhi = cp.mask_intnhi.value()
    evcode = cp.bat_dark_sele.value()

    if srcs == '':
        str_sel_dets = ' '.join(cp.list_of_dets_selected())
        logger.warning('Requested detector(s): "%s" is(are) are not found in data' % str_sel_dets)
        return None

    command = 'det_ndarr_raw_proc'\
            + ' -d %s'   % dsname\
            + ' -s %s'   % srcs\
            + ' -n %d'   % events\
            + ' -m %d'   % evskip\
            + ' -f %s'   % fntmpl\
            + ' -b %.3f' % int_lo\
            + ' -t %.3f' % int_hi\
            + ' -B %.3f' % rms_lo\
            + ' -T %.3f' % rms_hi\
            + ' -F 0.1'\
            + ' -p 0'\
            + ' -S 0377'\
            + ' -v 511'\
            + ' -L %.3f' % rmsnlo\
            + ' -H %.3f' % rmsnhi\
            + ' -D %.3f' % intnlo\
            + ' -U %.3f' % intnhi

    if evcode != 'None': command += ' -c %s'   % evcode

#  -d DSNAME, --dsname=DSNAME  dataset name, default = None
#  -s SOURCE, --source=SOURCE  input ndarray file name, default = None
#  -f OFNAME, --ofname=OFNAME  output file name template, default = nda-#exp-#run-#src-#evts-#type-#date-#time-#fid-#sec-#nsec.txt
#  -n EVENTS, --events=EVENTS  number of events to collect, default = 10000000
#  -m EVSKIP, --evskip=EVSKIP  number of events to skip, default = 0
#  -b INTLOW, --intlow=INTLOW  intensity low limit, default = None
#  -t INTHIG, --inthig=INTHIG  intensity high limit, default = None
#  -B RMSLOW, --rmslow=RMSLOW  rms low limit, default = None
#  -T RMSHIG, --rmshig=RMSHIG  rms high limit, default = None
#  -F FRACLM, --fraclm=FRACLM  allowed fraction limit, default = 0.1
#  -p PLOTIM, --plotim=PLOTIM  control bit-word to plot images, default = 0
#  -v VERBOS, --verbos=VERBOS  control bit-word for verbosity, default = 7
#  -S SAVEBW, --savebw=SAVEBW  control bit-word to save arrays, default = 255
#  -D INTNLO, --intnlo=INTNLO  number of sigma from mean for low  limit on INTENSITY, default = 6.0
#  -U INTNHI, --intnhi=INTNHI  number of sigma from mean for high limit on INTENSITY, default = 6.0
#  -L RMSNLO, --nsiglo=RMSNLO  number of sigma from mean for low limit on RMS, default = 6.0
#  -H RMSNHI, --nsighi=RMSNHI  number of sigma from mean for high limit on RMS, default = 6.0
#  -c EVCODE, --evcode=EVCODE  comma separated event codes for selection as OR ..., default = None

    msg = 'Avereging xtc file(s) using command:\n%s' % command \
        + '\nand save results in the log-file: %s' % logave
    logger.info(msg)

    return command


def command_for_peds_aver():

    command = str_command_for_peds_aver()
    if command is None: return False

    logname = fnm.path_peds_aver_log() # log file name for averaging

    err = gu.subproc_in_log(command.split(), logname) # , shell=True)
    if err != '':
        logger.warning('Warning/error message from subprocess:\n%s' % (err))
        return False
    else:
        logger.info('Avereging for run %s is completed' % cp.str_run_number.value())
        return True


def proc_dark_run_interactively(sep='--'):

    command_for_peds_scan()

    logger.info(sep + 'Data Types and Sources from xtc scan of the\n' + cp.blsp.txt_list_of_types_and_sources())

    if not command_for_peds_aver():
        msg = sep + 'Subprocess for averaging is completed with warning/error message(s);'\
              +'\nsee details in the logfile(s).'
        logger.critical(msg)

    print_dark_ave_log(sep)


def remove_subprocess_logs():
    for fname in (fnm.path_peds_aver_log(), fnm.path_peds_scan_log()):
        logger.debug('remove subprocess log file %s' % fname)
        os.remove(fname)
    logger.info('See log file: %s' % cp.logname.value())


class CommandLineCalib():
    """module for dark run processing CLI
    """
    sep = '\n' + 60*'-' + '\n'

    def __init__(self, **kwargs):

        if not self.set_pars(**kwargs): return

        self.print_local_pars()
        print_list_of_detectors(self.sep)
        print_list_of_xtc_files(title=self.sep+'List of xtc files for %s\n' % self.dsname)
        print_list_of_sources_from_regdb(self.sep)

        gu.create_directory(fnm.dir_results(), mode=self.dirmode)

        if self.process:
            proc_dark_run_interactively(self.sep)
        else:
            logger.critical(self.sep + '\nDARK PROCESSING OPTION IS TURNED OFF...'\
                            + '\nAdd option "-P" in the command line to process files\n')
            return

        if pattern_in_sources(ptrn='rayonix'): # rayonix_is_in_list
            self.add_files_for_rayonix()

        self.deploy_calib_files()
        remove_subprocess_logs()


    def set_pars(self, **kwa):

        #self.print_bits = kwa['print_bits']
        #logger.setPrintBits(self.print_bits)

        cp.commandlinecalib = self
        self.count_msg = 0

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
            logger.critical('EXPERIMENT NAME IS NOT DEFINED...'\
                     + '\nAdd optional parameter -e <exp-name>')
            return False

        self.dsname = 'exp=%s:run=%s:\n' % (self.exp_name, self.str_run_number)

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
            logger.critical('DETECTOR NAMES ARE NOT DEFINED...'\
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
        self.queue       = kwa['queue']
        self.process     = kwa['process']
        self.deploy      = kwa['deploy']
        self.deploygeo   = kwa['deploygeo']
        self.zeropeds    = kwa['zeropeds']
        self.instr_name  = self.exp_name[:3]
        self.dirmode     = kwa['dirmode']
        self.filemode    = kwa['filemode']
        self.loglev      = kwa['loglev']  # str
        self.logname     = kwa['logname']  # str

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
        cp.logname         .setValue(self.logname)

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
        + '\n     dirmode       : %s' % oct(self.dirmode)\
        + '\n     filemode      : %s' % oct(self.filemode)\
        + '\n     loglev        : %s' % self.loglev\
        + '\n     logname       : %s' % self.logname\

        logger.info(msg)


    def deploy_calib_files(self):

        print_list_of_files_dark_in_work_dir(self.sep)

        if self.deploy:
            logger.info(self.sep + 'Begin deployment of calibration files')
            s = fdmets.deploy_calib_files(self.str_run_number, self.str_run_range, mode='calibrun-dark', ask_confirm=False,\
                                          zeropeds=self.zeropeds, deploygeo=self.deploygeo, dirmode=self.dirmode, filemode=self.filemode)
            if s:
                logger.warning('Problem with deployment of calibration files...')
            else:
                logger.info('Deployment of calibration files is completed')
        else:
            logger.critical(self.sep + 'FILE DEPLOYMENT OPTION IS TURNED OFF...'\
                     +'\nAdd option "-D" in the command line to deploy files\n')


    def add_files_for_rayonix(self):
        """ Using shape of array for evaluated pedestals, add in the work directory additional files for Rayonix
            with zero peds and geometry
        """
        from PSCalib.NDArrIO import load_txt, save_txt #, list_of_comments
        from . import AppDataPath as apputils
        fname_geo  = str(apputils.AppDataPath('CalibManager/scripts/geometry-rayonix.template').path())
        logger.info('\n%s\nfname_geo: %s' % (100*'_', fname_geo))

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
                os.chmod(fname_peds_zero, self.filemode)

            # make/save default geometry
            if self.deploygeo:
                geo_segment = str_geo_segment_rayonix_v2(shape=ave.shape)
                str_geo = load_text_with_insets(fname_geo, insets={'SEGMENT_V2':geo_segment})
                logger.debug('str_geo:\n%s' % str_geo)
                fname_geometry  = str_filename_with_source(fnm.path_geometry(), s)
                logger.info('fname_geometry  :%s' % fname_geometry)
                gu.save_textfile(str_geo, fname_geometry, mode='w', accmode=self.filemode)

# EOF
