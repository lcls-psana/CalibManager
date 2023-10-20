
"""CommandLineCalib is intended for command line calibration of dark runs

This software was developed for the LCLS project.
If you use all or part of it, please give an appropriate acknowledgment.

@author Mikhail Dubrovin
"""
import logging
logger = logging.getLogger(__name__)

import os
import sys
import CalibManager.GlobalUtils as gu
import CalibManager.FileDeployer as fdmets
from CalibManager.FileNameManager import fnm
from CalibManager.ConfigParametersForApp import cp
import Detector.UtilsCalib as uc

def dsnamex_is_xtc_file(dsnamex):
    return dsnamex is not None and dsnamex[0] != ':'

def str_replace_fields(s, insets={}):
    """1. splits string fields separated by spaces.
       2. each field can be replaced by insets from dictionary.
       3. return (str) of joined fields separated by spaces.
    """
    return ' '.join([insets.get(f,f) for f in s.split(' ')])

def load_text_with_insets(fname, insets={}):
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

def print_list_of_detectors(sep='--'):
    msg = sep + 'List of detectors:'
    for det, par in zip(cp.list_of_dets_lower, cp.det_cbx_states_list):
        msg += '\n%s %s' % (det.ljust(12), par.value())
    logger.info(msg)

def print_list_of_xtc_files(title='List of xtc files'):
    dsnamex = cp.dsnamex.value()
    if dsnamex_is_xtc_file(dsnamex):
        logger.info('%s    ... xtc file is specified in --dsnamex' % (title))
    else:
        pattern = '-r%s' % cp.str_run_number.value()
        lst = fnm.get_list_of_xtc_files()
        lst_for_run = [path for path in lst if pattern in os.path.basename(path)]
        logger.info(title + '\n'.join(lst_for_run))

def txt_of_sources_in_run(self):
     import CalibManager.RegDBUtils as ru
     return ru.txt_of_sources_in_run(cp.instr_name.value(), cp.exp_name.value(), int(cp.str_run_number.value()))

def print_list_of_sources_from_regdb(sep='--'):
    txt = sep + 'Sources from DB:'
    #try: txt += cp.blsp.txt_of_sources_in_run()
    try: txt += self.txt_of_sources_in_run()
    except: txt += 'N/A'
    logger.info(txt)

def get_list_of_files_dark_in_work_dir():
    path_prexix = fnm.path_prefix_dark()
    dir, prefix = os.path.split(path_prexix)
    return gu.get_list_of_files_in_dir_for_part_fname(dir, pattern=prefix)

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

def scan_event_keys(pattern='EventKey(type=psana.'):
    """scan DataSource(dsname) for evt.key() and create set of (str) EventKey(...
       returns set of (str) evt.keys()
    """
    import psana
    dsnamex = cp.dsnamex.value()
    dsname = dsnamex if dsnamex_is_xtc_file(dsnamex) else cp.dsname.value()  # fnm.path_to_data_files() # exp=mecj5515:run=102:stream=0-79:smd
    logscn = fnm.path_peds_scan_log() # log file name for scan
    SKIP   = cp.bat_dark_start.value() - 1
    EVENTS = cp.bat_dark_scan.value() + SKIP
    ds  = psana.DataSource(dsname)
    sset = set()
    for i, evt in enumerate(ds.events()):
        if i<SKIP: continue
        if not i<EVENTS: break
        if i>1: break
        print('scan event %2d' % i)#, end='\r')
        for k in evt.keys():
            s = str(k)  # EventKey(type=psana.Epix.ElementV3, src='DetInfo(XppGon.0:Epix100a.1)', alias='epix')
            if pattern in s:
                sset.add(s)
    s = 'scan_event_keys'\
      + '\ndsname       : %s' % dsname\
      + '\nfirst event  : %s' % SKIP\
      + '\nlast event   : %s' % EVENTS\
      + '\npattern      : %s' % pattern\
      + '\n' + '\n'.join(sset)
    logger.info(s)
    gu.save_textfile(s, logscn, mode='w') #, accmode=0o664, group='ps-users')
    logger.debug('saved evt.keys() in temporary file: %s' % logscn)
    return sset

def parse_str_event_key(s, pattern='EventKey(type=psana.'):
    """ parse (str) like: EventKey(type=psana.CsPad2x2.ElementV1, src='DetInfo(CxiDg2.0:Cspad2x2.0)', alias='Dg2CsPad2x2')"""
    pos1 = s.find(pattern) + len(pattern)
    pos2 = s.rfind(')')
    s1 = s[pos1:pos2]
    fields = s1.split(',') # splits: CsPad2x2.ElementV1, src='DetInfo(CxiDg2.0:Cspad2x2.0)', alias='Dg2CsPad2x2'
    #print fields

    type = fields[0]                            # CsPad2x2.ElementV1
    if type.find('ConfigV') != -1: return None  # remove ConfigV from lists
    #print 'type: ', type
    tparts = type.split('.')
    type_old = '%s::%s' % (tparts[0],tparts[1]) if len(tparts) == 2 else type # CsPad2x2.ElementV1 -> CsPad2x2::ElementV1

    if len(fields)<2: return None
    patt = 'src='
    pos1 = fields[1].find(patt) + len(patt)
    detinfo_src = fields[1][pos1:].strip('"\'') # DetInfo(CxiDg2.0:Cspad2x2.0)
    #print 'detinfo_src: ', detinfo_src

    pos1 = detinfo_src.find('(') + 1
    pos2 = detinfo_src.rfind(')')
    src  = detinfo_src[pos1:pos2] # if pos2 != -1 elsw detinfo_src[pos1:]  # CxiDg2.0:Cspad2x2.0
    #print 'type:%s  src:%s' % (type, src)
    return type_old, src

def make_list_of_types_and_sources(set_of_str_event_keys):
    list_of_types = []
    list_of_sources = []
    for s in set_of_str_event_keys:
        resp = parse_str_event_key(s)
        if resp is None: continue
        list_of_types.append(resp[0])
        list_of_sources.append(resp[1])
    return list_of_types, list_of_sources

def print_list_of_types_and_sources(list_of_types, list_of_sources, title='Data Types and Sources from xtc file scan:\n'):
    """replacement for cp.blsp.txt_list_of_types_and_sources()"""
    logger.info(title + '\n'+ '\n'.join(['  %30s: %s'%(t, s) for t, s in zip(list_of_types, list_of_sources)]))

def str_command_for_peds_aver(str_sources):
    """Returns str command for dark run average, for example:
       det_ndarr_raw_proc -d exp=mecj5515:run=102:stream=0-79:smd -s MecTargetChamber.0:Cspad.0\
                          -n 6 -m 0 -f ./work/clb-#exp-#run-peds-#type-#src.txt
    """
    dsname = cp.dsname.value()    # fnm.path_to_data_files()       # 'exp=mecj5515:run=102:stream=0-79:smd'
    evskip = cp.bat_dark_start.value() - 1
    events = cp.bat_dark_end.value()
    fntmpl = fnm.path_peds_template()         # './work/clb-#exp-#run-peds-#type-#src.txt'
    srcs   = str_sources  # str_of_sources()  # 'MecTargetChamber.0:Cspad.0,MecTargetChamber.0:Cspad.1'
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
    nrecs  = cp.nrecs
    nrecs1 = cp.nrecs1
    exp_name = cp.exp_name.value() #  needed in case of stand-alone xtc file...

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
            + ' -S 255'\
            + ' -v 511'\
            + ' -L %.3f' % rmsnlo\
            + ' -H %.3f' % rmsnhi\
            + ' -D %.3f' % intnlo\
            + ' -U %.3f' % intnhi\
            + ' --nrecs  %d' % nrecs\
            + ' --nrecs1 %d' % nrecs1\
            + ' --expname %s' % exp_name

    if evcode != 'None': command += ' -c %s'   % evcode

    msg = 'Avereging xtc file(s) using command:\n%s' % command \
        + '\nand save results in the log-file: %s' % logave
    logger.info(msg)

    return command

def command_for_peds_aver(str_sources):
    command = str_command_for_peds_aver(str_sources)
    if command is None: return False
    logname = fnm.path_peds_aver_log() # log file name for averaging
    err = gu.subproc_in_log(command.split(), logname) # , shell=True)
    if err != '':
        logger.warning('Warning/error message from subprocess:\n%s' % (err))
        return False
    else:
        logger.info('Avereging for run %s is completed' % cp.str_run_number.value())
        return True

def remove_subprocess_logs():
    for fname in (fnm.path_peds_aver_log(), fnm.path_peds_scan_log()):
        logger.debug('remove subprocess log file %s' % fname)
        os.remove(fname)
    logger.info('See log file: %s' % cp.logname.value())

def exit_for_missing_parameter(s= '--run or -r'):
    sys.exit('MISSING PARAMETER %s NEEDS TO BE SPECIFIED' % s)

class CommandLineCalib():
    """module for dark run processing CLI"""
    sep = '\n' + 30*'-' + '\n'

    def __init__(self, **kwargs):

        if not self.set_pars(**kwargs): return

        self.print_local_pars()
        print_list_of_detectors(self.sep)
        print_list_of_xtc_files(title=self.sep+'List of xtc files for %s\n' % self.dsname)
        print_list_of_sources_from_regdb(self.sep)

        gu.create_directory(fnm.dir_results(), mode=self.dirmode)

        if self.process:
            self.proc_dark_run_interactively(self.sep)
        else:
            logger.critical(self.sep + '\nDARK PROCESSING OPTION IS TURNED OFF...'\
                            + '\nAdd option "-P" in the command line to process files\n')
            return

        if self.pattern_in_sources(ptrn='rayonix'): # rayonix_is_in_list
            self.add_files_for_rayonix()

        self.deploy_calib_files()
        remove_subprocess_logs()

    def set_pars(self, **kwa):
        cp.commandlinecalib = self
        self.count_msg = 0
        self.set_of_str_event_keys = None

        if kwa['run'] is None: exit_for_missing_parameter('--run or -r')
        self.run = kwa['run']
        self.runnum = int(self.run.split(',')[0].split('-')[0])  # grabs the 1-st run number from string like '2,4-7'
        self.str_run_number = '%04d' % self.runnum
        self.str_run_range = '%s-end' % self.runnum if kwa['runrange'] is None else kwa['runrange']

        if kwa['exp'] is None: exit_for_missing_parameter('--exp or -e')
        self.exp_name = kwa['exp']

        if kwa['detector'] is None: exit_for_missing_parameter('--detector or -d')
        self.det_name = kwa['detector'].replace(","," ")
        list_of_dets_sel_lower = [det.lower() for det in self.det_name.split()]

        #print('XXX list_of_dets_sel_lower', list_of_dets_sel_lower)
        #msg = self.sep + 'List of detectors:'
        #print('XXX cp.list_of_dets_lower', cp.list_of_dets_lower)

        for det, par in zip(cp.list_of_dets_lower, cp.det_cbx_states_list):
            par.setValue(det in list_of_dets_sel_lower)
            #msg += '\n%s %s' % (det.ljust(10), par.value())
        #logger.info(msg)

        if all(not p.value() for p in cp.det_cbx_states_list):
            msg = sys.exit('EXIT - specified detector type-name(s) (-d or --detector): %s not found in the list of allowed names: %s' % (self.det_name, str(cp.list_of_dets_lower)))
            logger.error(msg)
            #sys.exit(msg)

        self.event_code  = kwa['event_code']
        self.scan_events = kwa['scan_events']
        self.skip_events = kwa['skip_events']
        self.num_events  = kwa['num_events']
        self.thr_int_min = kwa['thr_int_min']
        self.thr_int_max = kwa['thr_int_max']
        self.thr_rms_min = kwa['thr_rms_min']
        self.thr_rms_max = kwa['thr_rms_max']
        self.intnlo      = kwa['intnlo']
        self.intnhi      = kwa['intnhi']
        self.rmsnlo      = kwa['rmsnlo']
        self.rmsnhi      = kwa['rmsnhi']
        self.workdir     = kwa['workdir']
        self.process     = kwa['process']
        self.deploy      = kwa['deploy']
        self.deploygeo   = kwa['deploygeo']
        self.zeropeds    = kwa['zeropeds']
        self.dirmode     = kwa['dirmode']
        self.filemode    = kwa['filemode']
        self.loglev      = kwa['loglev']   # str
        self.logname     = kwa['logname']  # str
        self.group       = kwa['group']    # ps-users
        self.dsnamex     = kwa['dsnamex']  # :std:dir=...
        self.dsname      = uc.str_dsname(self.exp_name, self.run, self.dsnamex)
        self.instr_name  = self.exp_name[:3]

        cp.nrecs         = kwa['num_events']
        cp.nrecs1        = kwa['nrecs1']

        cp.str_run_number.setValue(self.str_run_number)
        cp.exp_name      .setValue(self.exp_name)
        cp.instr_name    .setValue(self.instr_name)

        self.calibdir    = kwa['calibdir']
        if kwa['calibdir'] is None:
            self.calibdir = fnm.path_to_calib_dir_default()

        #cp.det_name        .setValue(self.det_name)
        cp.dsname          .setValue(self.dsname)
        cp.dsnamex         .setValue(self.dsnamex)
        cp.calib_dir       .setValue(self.calibdir)
        cp.dir_work        .setValue(self.workdir)
        cp.bat_dark_sele   .setValue(self.event_code)
        cp.bat_dark_scan   .setValue(self.scan_events)
        cp.bat_dark_start  .setValue(self.skip_events)
        cp.bat_dark_end    .setValue(self.num_events+self.skip_events)
        cp.mask_min_thr    .setValue(self.thr_int_min)
        cp.mask_max_thr    .setValue(self.thr_int_max)
        cp.mask_rms_thr_min.setValue(self.thr_rms_min)
        cp.mask_rms_thr_max.setValue(self.thr_rms_max)
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
        + '\n     dsnamex       : %s' % self.dsnamex\
        + '\n     dsname        : %s' % self.dsname\
        + '\n     det_name      : %s' % self.det_name\
        + '\n     num_events    : %d' % self.num_events\
        + '\n     skip_events   : %d' % self.skip_events\
        + '\n     scan_events   : %d' % self.scan_events\
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
        + '\n     dirmode       : %s' % oct(self.dirmode)\
        + '\n     filemode      : %s' % oct(self.filemode)\
        + '\n     loglev        : %s' % self.loglev\
        + '\n     logname       : %s' % self.logname\

        logger.info(msg)

    def proc_dark_run_interactively(self, sep='--'):
        #command_for_peds_scan()
        self.set_of_str_event_keys = scan_event_keys()
        self.list_of_types, self.list_of_sources = make_list_of_types_and_sources(self.set_of_str_event_keys)
        print_list_of_types_and_sources(self.list_of_types, self.list_of_sources)
        str_sources = self.str_of_sources()
        logger.debug('use string sources: %s' % str_sources)
        #sys.exit('TEST EXIT')

        if not command_for_peds_aver(str_sources):
            msg = sep + 'Subprocess for averaging is completed with warning/error message(s);'\
                  +'\nsee details in the logfile(s).'
            logger.critical(msg)
        print_dark_ave_log(sep)

    def get_list_of_type_sources(self):
        if self.set_of_str_event_keys is None: self.proc_dark_run_interactively()
        return list(zip(self.list_of_types, self.list_of_sources))

    def list_of_types_and_sources_for_detector(self, det_name):

        #if not self.scan_log_exists(): # Use RegDB
        #    ins, exp, run_number = cp.instr_name.value(), cp.exp_name.value(), int(cp.str_run_number.value())
        #    lst_srcs = ru.list_of_sources_in_run_for_selected_detector(ins, exp, run_number, det_name)
        #    dtype = cp.dict_of_det_data_types[det_name]
        #    ctype = cp.dict_of_det_calib_types[det_name]
        #    lst_dtypes = [dtype for src in lst_srcs]
        #    lst_ctypes = [ctype for src in lst_srcs]
        #    #print 'lst_ctypes::: ', lst_ctypes
        #    #print 'lst_dtypes::: ', lst_dtypes
        #    #print 'lst_srcs  ::: ', lst_srcs
        #    return lst_dtypes, lst_srcs, lst_ctypes

        pattern_det = det_name.lower() + '.'
        pattern_type = cp.dict_of_det_data_types[det_name]
        ##print 'XXX: pattern_type, pattern_det', pattern_type, pattern_det

        list_of_ctypes_for_det=[]
        list_of_dtypes_for_det=[]
        list_of_srcs_for_det=[]
        for t,s in self.get_list_of_type_sources():
            #print('XXX:   type, src: %24s  %s' % (t,s))
            if t.find(pattern_type)       == -1: continue
            if s.lower().find(pattern_det) == -1: continue
            list_of_ctypes_for_det.append(cp.dict_of_det_calib_types[det_name])
            list_of_dtypes_for_det.append(t)
            list_of_srcs_for_det.append(s)
        #print 'list of types and sources for detector %s:\n  %s\n  %s' \
        #      % (det_name, str(list_of_types_for_det), str(list_of_srcs_for_det))
        return list_of_dtypes_for_det, list_of_srcs_for_det, list_of_ctypes_for_det

    def list_of_types_and_sources_for_selected_detectors(self):
        """Returns the list of data types, sources, and calib types in run for selected detector.
        For example, for CSPAD returns
        ['CsPad::DataV2',    'CsPad::DataV2'],
        ['CxiDs1.0::Cspad.0', 'CxiDs2.0::Cspad.0']
        ['CsPad::CalibV1',   'CsPad::CalibV1'],
        """
        lst_ctypes = []
        lst_types  = []
        lst_srcs   = []
        for det_name in cp.list_of_dets_selected():
            lst_t, lst_s, lst_c = self.list_of_types_and_sources_for_detector(det_name)
            #print 'lst_t: ', lst_t
            #print 'lst_s: ', lst_s
            #print 'lst_c: ', lst_c
            lst_ctypes += lst_c
            lst_types += lst_t
            lst_srcs += lst_s
        return lst_types, lst_srcs, lst_ctypes

    def str_of_sources(self):
        """Returns comma separated sources. For example
           'CxiDg2.0:Cspad2x2.0,CxiEndstation.0:Opal4000.1'
        """
        list_of_all_srcs = []
        #print('XXX str_of_sources():cp.list_of_dets_selected():', cp.list_of_dets_selected())
        for det_name in cp.list_of_dets_selected():
            #lst_types, lst_srcs, lst_ctypes = cp.blsp.list_of_types_and_sources_for_detector(det_name)
            lst_types, lst_srcs, lst_ctypes = self.list_of_types_and_sources_for_detector(det_name)
            list_of_all_srcs += lst_srcs
        return ','.join(list_of_all_srcs)

    def list_of_sources_for_selected_detectors(self):
        """Returns the list of sources in run for selected detectors."""
        lst_types, lst_srcs, lst_ctypes = self.list_of_types_and_sources_for_selected_detectors()
        return lst_srcs

    def pattern_in_sources(self, ptrn='rayonix'):
        #lst_of_srcs = cp.blsp.list_of_sources_for_selected_detectors() # ['MfxEndstation.0:Rayonix.0']
        lst_of_srcs = self.list_of_sources_for_selected_detectors() # ['MfxEndstation.0:Rayonix.0']
        lst_bool = [(ptrn.lower() in s.lower()) for s in lst_of_srcs]
        logger.debug('pattern_in_sources - all sources: %s conditions: %s' % (str(lst_of_srcs),str(lst_bool)))
        return any(lst_bool)

    def deploy_calib_files(self):

        print_list_of_files_dark_in_work_dir(self.sep)

        if self.deploy:
            logger.info(self.sep + 'Begin deployment of calibration files')

            s = fdmets.deploy_calib_files(self.str_run_number, self.str_run_range, mode='calibrun-dark', ask_confirm=False,\
                                          zeropeds=self.zeropeds, deploygeo=self.deploygeo,\
                                          dirmode=self.dirmode, filemode=self.filemode, group=self.group, mets_from=self)
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

        #lst_of_srcs = cp.blsp.list_of_sources_for_selected_detectors() # ['MfxEndstation.0:Rayonix.0']
        lst_of_srcs = self.list_of_sources_for_selected_detectors() # ['MfxEndstation.0:Rayonix.0']
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
                gu.cgu.change_file_ownership(fname_peds_zero, user=None, group=self.group)

            # make/save default geometry
            if self.deploygeo:
                geo_segment = str_geo_segment_rayonix_v2(shape=ave.shape)
                str_geo = load_text_with_insets(fname_geo, insets={'SEGMENT_V2':geo_segment})
                logger.debug('str_geo:\n%s' % str_geo)
                fname_geometry  = str_filename_with_source(fnm.path_geometry(), s)
                logger.info('fname_geometry  :%s' % fname_geometry)
                gu.save_textfile(str_geo, fname_geometry, mode='w', accmode=self.filemode, group=self.group)

# EOF
