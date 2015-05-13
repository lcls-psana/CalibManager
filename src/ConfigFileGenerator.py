#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module ConfigFileGenerator...
#
#------------------------------------------------------------------------

"""Generates the configuration files for psana from current configuration parameters

This software was developed for the LCLS project.  If you use all or 
part of it, please give an appropriate acknowledgment.

@version $Id$

@author Mikhail S. Dubrovin
"""

#------------------------------
#  Module's version from SVN --
#------------------------------
__version__ = "$Revision$"
# $Source$

#--------------------------------
#  Imports of standard modules --
#--------------------------------
import sys
import os

from ConfigParametersForApp import cp
from Logger                 import logger
from FileNameManager        import fnm
import GlobalUtils          as     gu

#import AppUtils.AppDataPath as apputils
import           AppDataPath as apputils # My version, added in path the '../../data:'

#-----------------------------

class ConfigFileGenerator :
    """Generates the configuration files for psana from current configuration parameters
    """

    def __init__ (self, do_test=False) :
        """
        @param path_in  path to the input psana configuration stub-file
        @param path_out path to the output psana configuration file with performed substitutions
        @param d_subs   dictionary of substitutions
        @param keys     keys from the dictionary       
        """
        self.path_in  = None 
        self.path_out = None 
        self.d_subs   = None
        self.keys     = None 
        self.do_test_print = do_test
        

#-----------------------------
#-----------------------------
#-----------------------------
#-----------------------------

    def list_of_path_to_xtc_files_for_run (self) :
        """Makes the string of xtc files for non-default directory. For example:
        './myxtc/xpp/xppi0613/xtc/e319-r0173-s00-c00.xtc ./myxtc/xpp/xppi0613/xtc/e319-r0173-s01-c00.xtc'
        """
        xtcdir = fnm.path_to_xtc_dir() # './myxtc/xpp/xppi0613/xtc/'
        pattern = '-r%s' % cp.str_run_number.value()
        lst = fnm.get_list_of_xtc_files()
        lst_for_run = [ os.path.join(xtcdir, path) for path in lst if pattern in os.path.basename(path)]
        return ' '.join(lst_for_run)

#-----------------------------

    def path_to_data_files (self) :
        """Returns something like 'exp=xcs72913:run=49:xtc'
        """
        if cp.xtc_dir_non_std.value() != cp.xtc_dir_non_std.value_def() :
            #return self.list_of_path_to_xtc_files_for_run()
            xtcdir = fnm.path_to_xtc_dir() # './myxtc/xpp/xppi0613/xtc/'
            live = ':live' if 'ffb' in xtcdir else ''
            return 'exp=%s:run=%d:xtc:dir=%s%s' % (cp.exp_name.value(), int(cp.str_run_number.value()), xtcdir, live)

        else :
            return 'exp=%s:run=%d:xtc' % (cp.exp_name.value(), int(cp.str_run_number.value()))

#-----------------------------

    def make_psana_cfg_file_for_peds_scan (self) :
        self.path_in  = apputils.AppDataPath('CalibManager/scripts/psana-scan.cfg').path()
        self.d_subs   = {'FNAME_XTC' : self.path_to_data_files(),
                         'SKIP'      : str( cp.bat_dark_start.value() - 1 ),
                         'EVENTS'    : str( cp.bat_dark_scan.value() ),
                         }

        txt_cfg = self.text_for_section ()

        self.save_cfg_file(txt_cfg, fnm.path_peds_scan_psana_cfg())

#-----------------------------

    def make_psana_cfg_file_for_peds_aver (self) :

        self.str_of_modules = ''
        self.txt_cfg_header = '# Autogenerated config file for psana\n' \
                            + '# Useful command:\n' \
                            + '# psana -m EventKeys -n 5 ' + self.path_to_data_files() \
                            + '\n'
        self.txt_cfg_body   = '\n'

        self.add_cfg_module_tahometer()
        if cp.bat_dark_sele.value() : self.add_cfg_module_event_code_filter()
        status = self.cfg_file_body_for_peds_aver()
        self.cfg_file_header()

        self.save_cfg_file(self.txt_cfg_header + self.txt_cfg_body, fnm.path_peds_aver_psana_cfg())

        return status

#-----------------------------

    def cfg_file_header (self) :
        self.path_in  = apputils.AppDataPath('CalibManager/scripts/psana-header.cfg').path()
        self.d_subs   = {'FNAME_XTC' : self.path_to_data_files(),
                         'SKIP'      : str( cp.bat_dark_start.value() - 1 ),
                         'EVENTS'    : str( cp.bat_dark_end.value() - cp.bat_dark_start.value() ),
                         'MODULES'   : self.str_of_modules
                         }

        self.txt_cfg_header += self.text_for_section ()

#-----------------------------

    def add_cfg_module_event_code_filter (self) :
        self.path_in  = apputils.AppDataPath('CalibManager/scripts/psana-module-event-code-filter.cfg').path()
        module = 'ImgAlgos.EventCodeFilter'

        evcode = cp.bat_dark_sele.value()
        mode = 0
        if   evcode>0: mode=1
        elif evcode<0: mode=-1

        self.d_subs   = {
                         'MODULE'     : module,
                         'EVENTCODE'  : str(evcode),
                         'MODE'       : str(mode),
                         'PRINT_BITS' : '5',
                        }

        self.add_module_in_cfg ('%s' % (module))

#-----------------------------

    def cfg_file_body_for_peds_aver(self) :

        txt_cfg_body   = '#Module parameters'
        self.ind = 0

        for det_name in cp.list_of_dets_selected() :
            lst_types, lst_srcs, lst_ctypes = cp.blsp.list_of_types_and_sources_for_detector(det_name)
            list_path_peds_ave    = gu.get_list_of_files_for_list_of_insets(fnm.path_peds_ave(),    lst_srcs)
            list_path_peds_rms    = gu.get_list_of_files_for_list_of_insets(fnm.path_peds_rms(),    lst_srcs)
            list_path_hotpix_mask = gu.get_list_of_files_for_list_of_insets(fnm.path_hotpix_mask(), lst_srcs)

            if self.do_test_print : print 'Detector selected: %10s' % (det_name), '  sources:', lst_srcs

            for (self.source, self.fname_ave, self.fname_rms, self.fname_mask) in zip(lst_srcs, list_path_peds_ave, list_path_peds_rms, list_path_hotpix_mask) :
                self.ind += 1 
                #print self.ind, self.source, self.fname_ave, self.fname_rms

                #list_of_dets   = ['CSPAD', 'CSPAD2x2', 'Princeton', 'pnCCD', 'Tm6740', 'Opal1000', 'Opal2000', 'Opal4000', 'Opal8000', \
                #                  'OrcaFl40', 'Epix', 'Epix10k', 'Epix100a', 'Fccd960', 'Andor', 'Acqiris']
                #if   det_name == cp.list_of_dets[0] : self.add_cfg_module_peds_aver_cspad('cspad_mod.CsPadPedestals')
                #elif det_name == cp.list_of_dets[1] : self.add_cfg_module_peds_aver_cspad('cspad_mod.CsPad2x2Pedestals')
                if   det_name == cp.list_of_dets[0] : self.add_cfg_module_peds_aver_cspad_with_mask('CSPadPixCoords.CSPadNDArrProducer')
                elif det_name == cp.list_of_dets[1] : self.add_cfg_module_peds_aver_cspad_with_mask('CSPadPixCoords.CSPad2x2NDArrProducer')
                elif det_name == cp.list_of_dets[2] : self.add_cfg_module_peds_aver_princeton()
                elif det_name == cp.list_of_dets[3] : self.add_cfg_module_peds_aver_pnccd_ndarr()
               #elif det_name == cp.list_of_dets[3] : self.add_cfg_module_peds_aver_pnccd_img()
                elif det_name == cp.list_of_dets[4] : self.add_cfg_module_peds_aver_camera()
                elif det_name == cp.list_of_dets[5] : self.add_cfg_module_peds_aver_camera()
                elif det_name == cp.list_of_dets[6] : self.add_cfg_module_peds_aver_camera()
                elif det_name == cp.list_of_dets[7] : self.add_cfg_module_peds_aver_camera()
                elif det_name == cp.list_of_dets[8] : self.add_cfg_module_peds_aver_camera()
                elif det_name == cp.list_of_dets[9] : self.add_cfg_module_peds_aver_camera()
                elif det_name == cp.list_of_dets[10]: self.add_cfg_module_peds_aver_epix()
                elif det_name == cp.list_of_dets[11]: self.add_cfg_module_peds_aver_epix()
                elif det_name == cp.list_of_dets[12]: self.add_cfg_module_peds_aver_epix()
                elif det_name == cp.list_of_dets[13]: self.add_cfg_module_peds_aver_camera(out_dtype='int')
                elif det_name == cp.list_of_dets[14]: self.add_cfg_module_peds_aver_andor()
                elif det_name == cp.list_of_dets[15]: self.add_cfg_module_peds_aver_acqiris()
                elif det_name == cp.list_of_dets[16]: self.print_warning()
                else : logger.warning('UNKNOWN DETECTOR: %s' % det_name, __name__)

        if self.ind > 0 : return True

        msg = 'Selected detectors NOT FOUND in the list of keys in xtc scan log file !!!'
        logger.warning(msg, __name__)
        return False

#-----------------------------

    def print_warning (self) :
        msg = 'cfg_file_body_for_peds_aver_%s - IS NOT IMPLEMENTED YET!!!' % self.det_name
        logger.warning(msg, __name__)

#-----------------------------

    def add_cfg_module_peds_aver_cspad (self, module='cspad_mod.CsPadPedestals') :

        self.path_in  = apputils.AppDataPath('CalibManager/scripts/psana-module-peds-aver-cspad.cfg').path()
        mod = '%s:%i' % (module, self.ind)
        self.d_subs = {'MODULE'           : mod,
                       'DETINFO'          : self.source,
                       'FNAME_PEDS_AVE'   : self.fname_ave,
                       'FNAME_PEDS_RMS'   : self.fname_rms
                      }

        self.add_module_in_cfg (mod)

#-----------------------------

    def add_cfg_module_peds_aver_cspad_with_mask (self,
                                                  module_prod='CSPadPixCoords.CSPadNDArrProducer',
                                                  module_aver='ImgAlgos.NDArrAverage') : 

        self.path_in  = apputils.AppDataPath('CalibManager/scripts/psana-module-peds-aver-cspad-with-mask.cfg').path()
        mod_prod = '%s:%i' % (module_prod, self.ind)
        mod_aver = '%s:%i' % (module_aver, self.ind)
        self.d_subs = {'MODULE_PROD'       : mod_prod,
                       'MODULE_AVER'       : mod_aver,
                       'DETINFO'           : self.source,
                       'FNAME_PEDS_AVE'    : self.fname_ave,
                       'FNAME_PEDS_RMS'    : self.fname_rms,
                       'FNAME_PEDS_HOT'    : self.fname_mask,
                       'THR_RMS_HOTPIX_MIN': str( cp.mask_rms_thr_min.value() ),
                       'THR_RMS_HOTPIX'    : str( cp.mask_rms_thr.value() ),
                       'THR_MIN_HOTPIX'    : str( cp.mask_min_thr.value() ),
                       'THR_MAX_HOTPIX'    : str( cp.mask_max_thr.value() )
                      }

        self.add_module_in_cfg ('%s %s' % (mod_prod, mod_aver))

#-----------------------------

    def add_cfg_module_peds_aver_princeton (self, module='ImgAlgos.PrincetonImageProducer', ftype='metatxt') :
        self.path_in  = apputils.AppDataPath('CalibManager/scripts/psana-module-peds-aver-princeton.cfg').path()
        mod_img_rec = '%s:%i' % (module, self.ind) # str( cp.bat_img_rec_mod.value()
        mod         = '%s:%i' % ('ImgAlgos.NDArrAverage', self.ind)
        self.d_subs   = {
                         'MODULE_IMG_REC'       : mod_img_rec,
                         'DETINFO'              : self.source, # str( cp.bat_det_info.value() ),
                         'KEY_TRANSIT'          : 'img-%i' % self.ind,
                         'MODULE_AVERAGE'       : mod,
                         'FNAME_PEDS_AVE'       : self.fname_ave,
                         'FNAME_PEDS_RMS'       : self.fname_rms,
                         'FNAME_HOTPIX_MASK'    : self.fname_mask,
                         'FTYPE'                : str(ftype),
                         'THR_RMS_HOTPIX_MIN'   : str( cp.mask_rms_thr_min.value() ),
                         'THR_RMS_HOTPIX'       : str( cp.mask_rms_thr.value() ),
                         'THR_MIN_HOTPIX'       : str( cp.mask_min_thr.value() ),
                         'THR_MAX_HOTPIX'       : str( cp.mask_max_thr.value() )
                         }

        #self.d_subs['FNAME_HOTPIX_MASK'   ] = self.fname_mask # fnm.path_hotpix_mask()
        #self.d_subs['HOTPIX_THRESHOLD_ADU'] = str( cp.mask_rms_thr.value() )

        #if cp.mask_hot_is_used.value() : 
        #    self.d_subs['FNAME_HOTPIX_MASK'   ] = fnm.path_hotpix_mask()
        #    self.d_subs['HOTPIX_THRESHOLD_ADU'] = str( cp.mask_rms_thr.value() )
        #else :
        #    self.d_subs['FNAME_HOTPIX_MASK'   ] = ''
        #    self.d_subs['HOTPIX_THRESHOLD_ADU'] = '10000'

        self.add_module_in_cfg ('%s %s' % (mod_img_rec, mod))

#-----------------------------

    def add_cfg_module_peds_aver_pnccd_ndarr (self, module='ImgAlgos.PnccdNDArrProducer') :
        self.path_in  = apputils.AppDataPath('CalibManager/scripts/psana-module-peds-aver-pnccd-ndarr.cfg').path()
        mod_ndarr_prod= '%s:%i' % (module, self.ind)
        mod           = '%s:%i' % ('ImgAlgos.NDArrAverage', self.ind)
        self.d_subs   = {
                         'MODULE_NDARR_PROD'    : mod_ndarr_prod,
                         'DETINFO'              : self.source, # str( cp.bat_det_info.value() ),
                         'KEY_TRANSIT'          : 'img-%i' % self.ind,
                         'MODULE_AVERAGE'       : mod,
                         'FNAME_PEDS_AVE'       : self.fname_ave,
                         'FNAME_PEDS_RMS'       : self.fname_rms,
                         'FNAME_HOTPIX_MASK'    : self.fname_mask,
                         'THR_RMS_HOTPIX_MIN'   : str( cp.mask_rms_thr_min.value() ),
                         'THR_RMS_HOTPIX'       : str( cp.mask_rms_thr.value() ),
                         'THR_MIN_HOTPIX'       : str( cp.mask_min_thr.value() ),
                         'THR_MAX_HOTPIX'       : str( cp.mask_max_thr.value() )
                         }

        self.add_module_in_cfg ('%s %s' % (mod_ndarr_prod, mod))

#-----------------------------

    def add_cfg_module_peds_aver_pnccd_img (self, module='ImgAlgos.PnccdImageProducer') :
        self.path_in  = apputils.AppDataPath('CalibManager/scripts/psana-module-peds-aver-pnccd-img.cfg').path()
        mod_img_rec = '%s:%i' % (module, self.ind)
        mod         = '%s:%i' % ('ImgAlgos.NDArrAverage', self.ind)
        self.d_subs   = {
                         'MODULE_IMG_REC'       : mod_img_rec,
                         'DETINFO'              : self.source, # str( cp.bat_det_info.value() ),
                         'KEY_TRANSIT'          : 'img-%i' % self.ind,
                         'MODULE_AVERAGE'       : mod,
                         'FNAME_PEDS_AVE'       : self.fname_ave,
                         'FNAME_PEDS_RMS'       : self.fname_rms,
                         'FNAME_HOTPIX_MASK'    : self.fname_mask,
                         'THR_RMS_HOTPIX_MIN'   : str( cp.mask_rms_thr_min.value() ),
                         'THR_RMS_HOTPIX'       : str( cp.mask_rms_thr.value() ),
                         'THR_MIN_HOTPIX'       : str( cp.mask_min_thr.value() ),
                         'THR_MAX_HOTPIX'       : str( cp.mask_max_thr.value() )
                         }

        self.add_module_in_cfg ('%s %s' % (mod_img_rec, mod))

#-----------------------------

    def add_cfg_module_peds_aver_camera (self, module='ImgAlgos.CameraImageProducer', ftype='metatxt', out_dtype='asdata') :
        self.path_in  = apputils.AppDataPath('CalibManager/scripts/psana-module-peds-aver-camera.cfg').path()
        mod_img_rec = '%s:%i' % (module, self.ind)
        mod         = '%s:%i' % ('ImgAlgos.NDArrAverage', self.ind)
        self.d_subs   = {
                         'MODULE_IMG_REC'       : mod_img_rec,
                         'DETINFO'              : self.source, # str( cp.bat_det_info.value() ),
                         'KEY_TRANSIT'          : 'img-%i' % self.ind,
                         'OUT_DATA_TYPE'        : out_dtype,
                         'MODULE_AVERAGE'       : mod,
                         'FNAME_PEDS_AVE'       : self.fname_ave,
                         'FNAME_PEDS_RMS'       : self.fname_rms,
                         'FNAME_HOTPIX_MASK'    : self.fname_mask,
                         'FTYPE'                : str(ftype),
                         'THR_RMS_HOTPIX_MIN'   : str( cp.mask_rms_thr_min.value() ),
                         'THR_RMS_HOTPIX'       : str( cp.mask_rms_thr.value() ),
                         'THR_MIN_HOTPIX'       : str( cp.mask_min_thr.value() ),
                         'THR_MAX_HOTPIX'       : str( cp.mask_max_thr.value() )
                         }

        self.add_module_in_cfg ('%s %s' % (mod_img_rec, mod))

#-----------------------------

    def add_cfg_module_peds_aver_epix (self, module='ImgAlgos.EpixNDArrProducer', ftype='metatxt') :
        self.path_in  = apputils.AppDataPath('CalibManager/scripts/psana-module-peds-aver-epix.cfg').path()
        mod_img_rec = '%s:%i' % (module, self.ind)
        mod         = '%s:%i' % ('ImgAlgos.NDArrAverage', self.ind)
        self.d_subs   = {
                         'MODULE_IMG_REC'       : mod_img_rec,
                         'DETINFO'              : self.source, # str( cp.bat_det_info.value() ),
                         'KEY_TRANSIT'          : 'img-%i' % self.ind,
                         'MODULE_AVERAGE'       : mod,
                         'FNAME_PEDS_AVE'       : self.fname_ave,
                         'FNAME_PEDS_RMS'       : self.fname_rms,
                         'FNAME_HOTPIX_MASK'    : self.fname_mask,
                         'FTYPE'                : str(ftype),
                         'THR_RMS_HOTPIX_MIN'   : str( cp.mask_rms_thr_min.value() ),
                         'THR_RMS_HOTPIX'       : str( cp.mask_rms_thr.value() ),
                         'THR_MIN_HOTPIX'       : str( cp.mask_min_thr.value() ),
                         'THR_MAX_HOTPIX'       : str( cp.mask_max_thr.value() )
                         }

        self.add_module_in_cfg ('%s %s' % (mod_img_rec, mod))

#-----------------------------

    def add_cfg_module_peds_aver_andor (self, module='ImgAlgos.AndorImageProducer', ftype='metatxt', out_dtype='asdata') :
        self.path_in  = apputils.AppDataPath('CalibManager/scripts/psana-module-peds-aver-andor.cfg').path()
        mod_img_rec = '%s:%i' % (module, self.ind)
        mod         = '%s:%i' % ('ImgAlgos.NDArrAverage', self.ind)
        self.d_subs   = {
                         'MODULE_IMG_REC'       : mod_img_rec,
                         'DETINFO'              : self.source, # str( cp.bat_det_info.value() ),
                         'KEY_TRANSIT'          : 'img-%i' % self.ind,
                         'OUT_DATA_TYPE'        : out_dtype,
                         'MODULE_AVERAGE'       : mod,
                         'FNAME_PEDS_AVE'       : self.fname_ave,
                         'FNAME_PEDS_RMS'       : self.fname_rms,
                         'FNAME_HOTPIX_MASK'    : self.fname_mask,
                         'FTYPE'                : str(ftype),
                         'THR_RMS_HOTPIX_MIN'   : str( cp.mask_rms_thr_min.value() ),
                         'THR_RMS_HOTPIX'       : str( cp.mask_rms_thr.value() ),
                         'THR_MIN_HOTPIX'       : str( cp.mask_min_thr.value() ),
                         'THR_MAX_HOTPIX'       : str( cp.mask_max_thr.value() )
                         }

        self.add_module_in_cfg ('%s %s' % (mod_img_rec, mod))

#-----------------------------

    def add_cfg_module_peds_aver_acqiris (self, module='ImgAlgos.AcqirisArrProducer') :
        self.path_in  = apputils.AppDataPath('CalibManager/scripts/psana-module-peds-aver-acqiris.cfg').path()
        mod_img_rec = '%s:%i' % (module, self.ind)
        mod         = '%s:%i' % ('ImgAlgos.AcqirisAverage', self.ind)
        self.d_subs   = {
                         'MODULE_IMG_REC'       : mod_img_rec,
                         'DETINFO'              : self.source, # str( cp.bat_det_info.value() ),
                         'KEY_TRANSIT'          : 'img-%i' % self.ind,
                         'MODULE_AVERAGE'       : mod,
                         'FNAME_PEDS_AVE'       : self.fname_ave,
                         }

        self.add_module_in_cfg ('%s %s' % (mod_img_rec, mod))

#-----------------------------

    def add_cfg_module_tahometer (self) :
        self.path_in  = apputils.AppDataPath('CalibManager/scripts/psana-module-tahometer.cfg').path()
        mod = 'ImgAlgos.Tahometer'
        self.d_subs   = {
                         'MODULE'          : mod,
                         'PRINT_BITS'      : '7',
                         'EVENTS_INTERVAL' : '100'
                        }

        self.add_module_in_cfg ('%s' % (mod))

#-----------------------------
#-----------------------------
#-----------------------------
#-----------------------------

    def print_substitution_dict (self) :
        logger.debug('Substitution dictionary:',__name__)
        for k,v in self.d_subs.iteritems() :
            msg = '%s : %s' % (k.ljust(16), v.ljust(32))
            logger.debug(msg)

#-----------------------------

    def field_substituted(self, field) :
        if field in self.keys : return self.d_subs[field]
        else                  : return field

#-----------------------------

    def line_with_substitution(self, line) :
        fields = line.split()
        line_sub = ''
        for field in fields :

            field_sub = self.field_substituted(field)
            line_sub += field_sub + ' '

        line_sub.rstrip(' ')
        line_sub += '\n'
        return line_sub

#-----------------------------

    def text_for_section (self) :
        """Make txt for cfg file section 
        """
        logger.debug('Make text for: ' + self.path_in,__name__)

        self.keys   = self.d_subs.keys()

        txt = ''
        fin = open(self.path_in, 'r')
        for line in fin :
            line_sub = self.line_with_substitution(line)
            txt += line_sub
        fin.close() 

        return txt

#-----------------------------

    def add_module_in_cfg (self, module_name) :
        self.print_substitution_dict()
        self.str_of_modules += ' ' + module_name
        self.txt_cfg_body += self.text_for_section ()
        
#-----------------------------

    def save_cfg_file (self, text, path) :
        msg = 'Save configuration file: %s' % path
        logger.info(msg,__name__)
        if self.do_test_print : print msg
        gu.save_textfile(text, path)

#-----------------------------

cfg = ConfigFileGenerator ()

#-----------------------------
#
#  In case someone decides to run this module
#
if __name__ == "__main__" :

    cp.instr_name    .setValue('CXI')
    cp.exp_name      .setValue('cxib2313')
    cp.str_run_number.setValue('0002')

    cfg_test = ConfigFileGenerator (do_test=True)

    print '\nTest make_psana_cfg_file_for_peds_scan()'
    cfg_test.make_psana_cfg_file_for_peds_scan()

    print '\nTest make_psana_cfg_file_for_peds_aver()'
    cfg_test.make_psana_cfg_file_for_peds_aver()

    sys.exit ( 'End of test for ConfigFileGenerator' )

#-----------------------------
