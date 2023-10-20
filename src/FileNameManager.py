
"""Dynamically generates the file names from the confoguration parameters

This software was developed for the LCLS project.  If you use all or
part of it, please give an appropriate acknowledgment.

@author Mikhail Dubrovin
"""
#import logging
#logger = logging.getLogger(__name__)

import os

from   CalibManager.ConfigParametersForApp import cp
import CalibManager.GlobalUtils as gu

def log_file_cpo():
    """Returns name like /reg/g/psdm/logs/calibman/2016/07/2016-07-19-12:20:59-log-dubrovin-562.txt"""
    from CalibManager.Logger import logger
    fname = logger.getLogFileName()     # 2016-07-19-11:53:02-log.txt
    year, month = fname.split('-')[:2]  # 2016, 07
    name, ext = os.path.splitext(fname) # 2016-07-19-11:53:02-log, .txt
    return '%s/%s/%s/%s-%s-%s%s' % (cp.dir_log_cpo.value(), year, month, name, gu.get_login(), gu.get_pid(), ext)


class FileNameManager:
    """Dynamically generates the file names from the confoguration parameters."""
    def __init__ (self):
        pass

    def path_dir_work(self):
        return cp.dir_work.value()

    def str_exp_run_for_xtc_path(self, path):
        instrument, experiment, run_str, run_num = gu.parse_xtc_path(path)
        if experiment is None: return 'exp-run-'
        else                 : return experiment + '-' + run_str + '-'

    def str_run_for_xtc_path(self, path):
        instrument, experiment, run_str, run_num = gu.parse_xtc_path(path)
        if run_str is None: return 'run-'
        else              : return run_str + '-'

    def path_prefix_data(self):
        return './'

    def path_gui_image(self):
        return self.path_prefix_data() + 'gui-image.png'

    def path_dark_xtc(self):
        return self.path_to_xtc_files_for_run()

    def path_dark_xtc_all_chunks(self):
        return self.path_to_xtc_files_for_run()

    def path_dark_xtc_cond(self):
        if cp.use_dark_xtc_all.value(): return self.path_dark_xtc_all_chunks()
        else                          : return self.path_dark_xtc()

    def str_exp_run_dark(self):
        """ returns str like 'xpptut15-r0240-'"""
        #return self.str_exp_run_for_xtc_path(self.path_dark_xtc())
        return '%s-r%s-' % (cp.exp_name.value(), cp.str_run_number.value())

    def path_to_calib_dir_custom(self):
        """Returns path to the user selected (non-default) calib dir, for example /reg/neh/home1/<user-name>/<further-path>/calib"""
        return cp.calib_dir.value()

    def path_to_calib_dir_default(self):
        """Returns somthing like /reg/d/psdm/CXI/cxitut13/calib or None"""
        if cp.instr_dir .value() is None: return None
        if cp.instr_name.value() is None: return None
        if cp.exp_name  .value() is None: return None
        return cp.instr_dir.value() + '/' + cp.instr_name.value() + '/' + cp.exp_name.value() + '/calib'

    def path_to_calib_dir(self):
        if cp.calib_dir.value() != 'None': return self.path_to_calib_dir_custom()
        else                             : return self.path_to_calib_dir_default()

    def path_to_calib_dir_src_custom(self):
        """Returns path to the user selected (non-default) calib dir, for example /reg/neh/home1/<user-name>/<further-path>/calib"""
        return cp.calib_dir_src.value()

    def path_to_calib_dir_src_default(self):
        """Returns somthing like /reg/d/psdm/CXI/cxitut13/calib or None"""
        if cp.instr_dir.value()    is None: return None
        if cp.instr_name.value()   is None: return None
        if cp.exp_name_src.value() is None: return None
        return cp.instr_dir.value() + '/' + cp.instr_name.value() + '/' + cp.exp_name_src.value() + '/calib'

    def path_to_calib_dir_src(self):
        if cp.calib_dir_src.value() != 'None': return self.path_to_calib_dir_src_custom()
        else                                 : return self.path_to_calib_dir_src_default()

    def path_to_xtc_dir(self):
        """Returns somthing like /reg/d/psdm/CXI/cxitut13/xtc/ or None"""
        if cp.dsnamex.value() != cp.dsnamex.value_def():
            return cp.dsnamex.value()
        if cp.instr_dir.value()  is None: return None
        if cp.instr_name.value() is None: return None
        if cp.exp_name.value()   is None: return None
        return os.path.join(cp.instr_dir.value(), cp.instr_name.value(), cp.exp_name.value(), 'xtc')

    def get_list_of_xtc_files(self):
        return gu.get_list_of_files_in_dir_for_ext(self.path_to_xtc_dir(), '.xtc')

    def get_list_of_xtc_runs(self):
        """Returns the list of xtc runs as string, for example:  ['0001', '0202', '0203', '0204',...]"""
        list_of_xtc_files = self.get_list_of_xtc_files()
        list_of_xtc_runs = []
        for fname in list_of_xtc_files:
            exp, run, stream, chunk, ext = gu.parse_xtc_file_name(fname)
            if run in list_of_xtc_runs: continue
            list_of_xtc_runs.append(run)
        return list_of_xtc_runs

    def get_list_of_xtc_run_nums(self):
        """Returns the list of xtc integer run numbers:  [1, 202, 203, 204,...]"""
        return [int(run) for run in self.get_list_of_xtc_runs()]

    def path_to_xtc_files_for_run(self):
        """Returns somthing like /reg/d/psdm/CXI/cxitut13/xtc/e304-r0022-*.xtc"""
        if cp.str_run_number.value() == 'None': return None
        pattern = '-r' + cp.str_run_number.value()
        for fname in self.get_list_of_xtc_files():
            if fname.find(pattern) != -1:
                exp, runnum, stream, chunk, ext = gu.parse_xtc_file_name(fname) # Parse: e170-r0003-s00-c00.xtc
                return os.path.join(self.path_to_xtc_dir(), exp + '-r' + runnum + '-*.xtc')
        return None

    def get_list_of_metrology_text_files(self):
        return [self.path_metrology_text()]

    def path_metrology_text_def(self):
        return cp.dir_work.value() + '/' + cp.fname_metrology_text.value_def()

    def path_metrology_text(self):
        if cp.fname_metrology_text.value() == cp.fname_metrology_text.value_def():
            return self.path_metrology_text_def()
        else:
            return cp.fname_metrology_text.value()

    def path_metrology_xlsx(self):
        return cp.fname_metrology_xlsx.value()

    def path_metrology_alignment_const(self):
        return self.path_prefix() + 'metro-align.txt'

    def dir_results(self, dname='/results'):
        return cp.dir_work.value() + dname

    def path_prefix(self):
        return self.dir_results() + '/' + cp.fname_prefix.value()

    def path_prefix_dark(self):
        return self.path_prefix() + self.str_exp_run_dark()

    def log_file(self):
        return cp.dir_work.value()

    def log_file_cpo(self):
        return log_file_cpo()

    def logname_base(self):
        return cp.logname.value().rsplit('.',1)[0]

    def path_peds_scan_log(self):
        return self.logname_base() + '_peds_scan.txt'

    def path_peds_aver_log(self):
        return self.logname_base() + '_peds_aver.txt'

    def path_peds_scan_psana_cfg(self):
        return self.path_prefix_dark() + 'peds-scan.cfg'

    def path_peds_scan_batch_log(self):
        return self.path_peds_scan_log()

    def path_peds_aver_psana_cfg(self):
        return self.path_prefix_dark() + 'peds-aver.cfg'

    def path_peds_aver_batch_log(self):
        return self.path_peds_aver_log()

    def path_peds_template(self):
        return self.path_prefix() + '#exp-#run-peds-#type-#src.txt'

    def path_peds_ave(self):
        return self.path_prefix_dark() + 'peds-ave.txt'

    def path_peds_rms(self):
        return self.path_prefix_dark() + 'peds-rms.txt'

    def path_hotpix_mask(self):
        return self.path_prefix_dark() + 'peds-sta.txt'

    def path_peds_cmod(self):
        return self.path_prefix_dark() + 'peds-cmo.txt'

    def path_peds_zero(self):
        return self.path_prefix_dark() + 'peds-zero.txt'

    def path_geometry(self):
        return self.path_prefix_dark() + 'geometry.txt'

    def path_peds_ave_plot(self):
        return self.path_prefix_dark() + 'peds-ave-plot.png'

    def path_hotpix_mask_prefix(self):
        return os.path.splitext(self.path_hotpix_mask())[0]

    def path_hotpix_mask_plot(self):
        return self.path_hotpix_mask_prefix() + '-plot.png'

    def get_list_of_files_peds_scan(self):
        return [self.path_peds_scan_batch_log(),]

    def get_list_of_files_peds_aver(self):
        return [self.path_peds_aver_batch_log(),]

    def get_list_of_files_peds_view(self):
        return self.get_list_of_files_peds_scan()\
             + self.get_list_of_files_peds_aver()

    def get_list_of_files_peds(self):
        self.list_of_files_peds = self.get_list_of_files_peds_view()
        self.list_of_files_peds.append(self.path_peds_ave_plot())
        return self.list_of_files_peds

    def path_to_data_files(self):
        """Returns something like 'exp=xcs72913:run=49:xtc' + ':dir=./myxtc/xpp/xppi0613/xtc/:live'"""
        mode = ':smd' if cp.smd_is_on.value() else ':xtc'
        if cp.dsnamex.value() != cp.dsnamex.value_def():
            xtcdir = fnm.path_to_xtc_dir() # './myxtc/xpp/xppi0613/xtc/'
            live = ':live' if 'ffb' in xtcdir else ''
            return 'exp=%s:run=%d:stream=0-79%s:dir=%s%s' % (cp.exp_name.value(), int(cp.str_run_number.value()), mode, xtcdir, live)
        else:
            return 'exp=%s:run=%d:stream=0-79%s' % (cp.exp_name.value(), int(cp.str_run_number.value()), mode)

fnm = FileNameManager()

if __name__ == "__main__":
    import sys
    ntest = 1
    if len(sys.argv)>1: ntest = sys.argv[1]
    if ntest == 1: print('fnm.log_file_cpo(): ', fnm.log_file_cpo())
    sys.exit( 'End of test for FileNameManager' )

# EOF
