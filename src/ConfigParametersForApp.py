
""":py:class:`ConfigParametersForApp` - class supporting configuration parameters for specific application.

This software was developed for the SIT project.
If you use all or part of it, please give an appropriate acknowledgment.
"""
__author__ = "Mikhail S. Dubrovin"

from CalibManager.Logger import logger
from .ConfigParameters import *
from PyQt5 import QtCore, QtGui
from . import AppDataPath as apputils # for icons

import PSCalib.GlobalUtils as gu
from CalibManager.dir_root import DIR_PSDM_DATA, DIR_REPO

class ConfigParametersForApp(ConfigParameters):
    """Is intended as a storage for configuration parameters for CorAna project."""
    name = 'ConfigParametersForApp'

    list_pars = []

    char_expand    = u' \u25BC' # down-head triangle
    char_shrink    = u' \u25B2' # solid up-head triangle

    list_of_queues = ['psanaq',    'psnehhiprioq', 'psfehhiprioq', 'psnehprioq', 'psfehprioq', 'psnehq',    'psfehq']
    list_of_farms  = ['psanafarm', 'psnehfarm',    'psfehfarm',    'psnehfarm',  'psfehfarm',  'psnehfarm', 'psfehfarm']
    dict_of_queue_farm = dict(zip(list_of_queues, list_of_farms))

    list_of_instr     = ['AMO', 'SXR', 'XPP', 'XCS', 'CXI', 'MEC', 'MFX', 'DET', 'DIA', 'USR', 'MOB']
    list_of_show_runs = ['in range', 'dark', 'all']
    list_of_show_dets = ['any', 'selected any', 'selected all']

    list_geo_log_levels=['DEBUG', 'INFO', 'WARNING', 'CRITICAL', 'ERROR', 'NONE']

    list_of_depl_cmod = [gu.PNCCD] # see also self.dark_deploy_cmod

    par01 = 'MPA1SdCp7h18m'
    par02 = __author__.split()[2].lower()

    dict_bjpeds = {} # dictionary of run_num:BatchJobPedestals objects
    dict_guidarklistitem = {} # dictionary of run_num:GUIDarkListItem objects

    def __init__(self, fname=None):
        """Constructor.
        @param fname  the file name with configuration parameters, if not specified then it will be set to the default value at declaration.
        """
        ConfigParameters.__init__(self)
        self.fname_cp = 'confpars-calibman.txt' # Re-define default config file name

        self.declareAllParameters()
        self.readParametersFromFile (fname)
        self.initRunTimeParameters()
        self.defineStyles()


    def initRunTimeParameters(self):
        self.iconsAreLoaded    = False
        self.guilogger         = None
        self.guimain           = None
        self.guidark           = None
        self.guidata           = None
        self.guidarklist       = None
        self.guitabs           = None
        self.guistatus         = None
        self.guiinsexpdirdet   = None
        self.guifilebrowser    = None
        self.blsp              = None
        self.guidarkcontrolbar = None
        self.guigeometry       = None
        self.guimetrology      = None
        self.dark_list         = None
        self.guifilemanager    = None
        self.guifilemanagersingle = None
        self.guifilemanagersinglecontrol = None
        self.guifilemanagergroup  = None
        self.guifilemanagergroupcontrol = None
        self.guiexpcalibdir    = None
        self.guidirtree        = None
        self.dirtreemodel      = None
        self.maskeditor        = None
        self.commandlinecalib  = None
        self.plotimgspe        = None

        if self.bat_queue.value() == 'psanacsq': self.bat_queue.setValue('psanaq')


    def setIcons(self):

        if self.iconsAreLoaded: return

        self.iconsAreLoaded = True

        path_icon_contents       = apputils.AppDataPath('CalibManager/icons/contents.png'     ).path()
        path_icon_mail_forward   = apputils.AppDataPath('CalibManager/icons/mail-forward.png' ).path()
        path_icon_button_ok      = apputils.AppDataPath('CalibManager/icons/button_ok.png'    ).path()
        path_icon_button_cancel  = apputils.AppDataPath('CalibManager/icons/button_cancel.png').path()
        path_icon_exit           = apputils.AppDataPath('CalibManager/icons/exit.png'         ).path()
        path_icon_home           = apputils.AppDataPath('CalibManager/icons/home.png'         ).path()
        path_icon_redo           = apputils.AppDataPath('CalibManager/icons/redo.png'         ).path()
        path_icon_undo           = apputils.AppDataPath('CalibManager/icons/undo.png'         ).path()
        path_icon_reload         = apputils.AppDataPath('CalibManager/icons/reload.png'       ).path()
        path_icon_save           = apputils.AppDataPath('CalibManager/icons/save.png'         ).path()
        path_icon_save_cfg       = apputils.AppDataPath('CalibManager/icons/fileexport.png'   ).path()
        path_icon_edit           = apputils.AppDataPath('CalibManager/icons/edit.png'         ).path()
        path_icon_browser        = apputils.AppDataPath('CalibManager/icons/fileopen.png'     ).path()
        path_icon_monitor        = apputils.AppDataPath('CalibManager/icons/icon-monitor.png' ).path()
        path_icon_unknown        = apputils.AppDataPath('CalibManager/icons/icon-unknown.png' ).path()
        path_icon_plus           = apputils.AppDataPath('CalibManager/icons/icon-plus.png'    ).path()
        path_icon_minus          = apputils.AppDataPath('CalibManager/icons/icon-minus.png'   ).path()
        path_icon_logviewer      = apputils.AppDataPath('CalibManager/icons/logviewer.png'    ).path()
        path_icon_lock           = apputils.AppDataPath('CalibManager/icons/locked-icon.png'  ).path()
        path_icon_unlock         = apputils.AppDataPath('CalibManager/icons/unlocked-icon.png').path()
        path_icon_convert        = apputils.AppDataPath('CalibManager/icons/icon-convert.png' ).path()

        path_icon_table          = apputils.AppDataPath('CalibManager/icons/table.gif'        ).path()
        path_icon_folder_open    = apputils.AppDataPath('CalibManager/icons/folder_open.gif'  ).path()
        path_icon_folder_closed  = apputils.AppDataPath('CalibManager/icons/folder_closed.gif').path()

        self.icon_contents      = QtGui.QIcon(path_icon_contents     )
        self.icon_mail_forward  = QtGui.QIcon(path_icon_mail_forward )
        self.icon_button_ok     = QtGui.QIcon(path_icon_button_ok    )
        self.icon_button_cancel = QtGui.QIcon(path_icon_button_cancel)
        self.icon_exit          = QtGui.QIcon(path_icon_exit         )
        self.icon_home          = QtGui.QIcon(path_icon_home         )
        self.icon_redo          = QtGui.QIcon(path_icon_redo         )
        self.icon_undo          = QtGui.QIcon(path_icon_undo         )
        self.icon_reload        = QtGui.QIcon(path_icon_reload       )
        self.icon_save          = QtGui.QIcon(path_icon_save         )
        self.icon_save_cfg      = QtGui.QIcon(path_icon_save_cfg     )
        self.icon_edit          = QtGui.QIcon(path_icon_edit         )
        self.icon_browser       = QtGui.QIcon(path_icon_browser      )
        self.icon_monitor       = QtGui.QIcon(path_icon_monitor      )
        self.icon_unknown       = QtGui.QIcon(path_icon_unknown      )
        self.icon_plus          = QtGui.QIcon(path_icon_plus         )
        self.icon_minus         = QtGui.QIcon(path_icon_minus        )
        self.icon_logviewer     = QtGui.QIcon(path_icon_logviewer    )
        self.icon_lock          = QtGui.QIcon(path_icon_lock         )
        self.icon_unlock        = QtGui.QIcon(path_icon_unlock       )
        self.icon_convert       = QtGui.QIcon(path_icon_convert      )

        self.icon_table         = QtGui.QIcon(path_icon_table        )
        self.icon_folder_open   = QtGui.QIcon(path_icon_folder_open  )
        self.icon_folder_closed = QtGui.QIcon(path_icon_folder_closed)

        self.icon_logger        = self.icon_edit
        self.icon_help          = self.icon_unknown
        self.icon_reset         = self.icon_reload


    def declareAllParameters(self):
        # Possible typs for declaration: 'str', 'int', 'long', 'float', 'bool'

        # GUILogger.py
        self.log_level        = self.declareParameter( name='LOG_LEVEL_OF_MSGS',    val_def='info',         type='str' )
        self.log_file         = self.declareParameter( name='LOG_FILE_FOR_LEVEL',   val_def='./log_for_level.txt',       type='str' )
        self.save_log_at_exit = self.declareParameter( name='SAVE_LOG_AT_EXIT',     val_def=True,           type='bool')
        self.dir_log_cpo      = self.declareParameter( name='DIR_FOR_LOG_FILE_CPO', val_def=DIR_REPO+'logs/calibman', type='str' )
        self.logname          = self.declareParameter( name='LOGNAME',              val_def='./work/logs/2022/log.txt',  type='str' )

        # GUIMain.py (10, 25, 800, 700)
        self.main_win_width  = self.declareParameter( name='MAIN_WIN_WIDTH',  val_def=800, type='int' )
        self.main_win_height = self.declareParameter( name='MAIN_WIN_HEIGHT', val_def=700, type='int' )
        self.main_win_pos_x  = self.declareParameter( name='MAIN_WIN_POS_X',  val_def=5,   type='int' )
        self.main_win_pos_y  = self.declareParameter( name='MAIN_WIN_POS_Y',  val_def=5,   type='int' )

        # GUIInsExpDirDet.py
        self.instr_dir          = self.declareParameter( name='INSTRUMENT_DIR',    val_def=DIR_PSDM_DATA,  type='str' )
        self.instr_name         = self.declareParameter( name='INSTRUMENT_NAME',   val_def='Select',       type='str' ) # 'CXI'
        self.exp_name           = self.declareParameter( name='EXPERIMENT_NAME',   val_def='Select',       type='str' ) # 'cxitut13'
        self.det_but_title      = self.declareParameter( name='DETECTOR_BUT_TITLE',val_def='Select',       type='str' ) # 'Select' or 'Selected:N'
        self.det_name           = self.declareParameter( name='DETECTOR_NAMES',    val_def='',             type='str' ) # 'CSPAD'
        self.calib_dir          = self.declareParameter( name='CALIB_DIRECTORY',   val_def='Select',       type='str' ) # '/reg/d/psdm/CXI/cxitut13/calib'

        # GUIExpCalibDet.py
        self.calib_dir_src      = self.declareParameter( name='CALIB_DIRECTORY_SRC', val_def='Select',     type='str' ) # '/reg/d/psdm/CXI/cxitut13/calib'
        self.exp_name_src       = self.declareParameter( name='EXPERIMENT_NAME_SRC', val_def='Select',     type='str' ) # 'cxitut13'

        # FileDeployer.py
        self.fname_history      = self.declareParameter( name='HISTORY_FILE_NAME', val_def='HISTORY',      type='str' )

        # GUIMainTabs.py
        self.current_tab    = self.declareParameter( name='CURRENT_TAB'      , val_def='Status',        type='str' )

        # GUIConfig.py
        self.current_config_tab   = self.declareParameter( name='CURRENT_CONFIG_TAB', val_def='Configuration File', type='str' )

        # GUIFileManager.py
        self.current_fmanager_tab = self.declareParameter( name='CURRENT_FILE_MANAGER_TAB', val_def='Single File', type='str' )
        self.path_fm_selected     = self.declareParameter( name='PATH_FILE_MANAGER_SELECTED', val_def='', type='str' )

        # GUIMainSplit.py
        ####self.fname_cp       = self.declareParameter( name='FNAME_CONFIG_PARS', val=fname, val_def='confpars.txt', type='str' )

        # GUIConfigPars.py
        self.dir_work          = self.declareParameter( name='DIRECTORY_WORK',        val_def='./work',       type='str' )
        self.dir_results       = self.declareParameter( name='DIRECTORY_RESULTS',     val_def='./results',    type='str' )
        self.fname_prefix      = self.declareParameter( name='FILE_NAME_PREFIX',      val_def='clb-',         type='str' )
        self.save_cp_at_exit   = self.declareParameter( name='SAVE_CONFIG_AT_EXIT',   val_def=True,           type='bool')

        # ConfigFileGenerator.py
        self.smd_is_on         = self.declareParameter( name='SMD_IS_ON', val_def=False, type='bool')

        # GUIGeometry.py
        self.current_geometry_tab = self.declareParameter( name='CURRENT_GEOMETRY_TAB',    val_def='Metrology',     type='str' )
        self.fname_metrology_xlsx = self.declareParameter( name='FNAME_METROLOGY_XLSX',    val_def='*.xlsx',        type='str' )
        self.fname_metrology_text = self.declareParameter( name='FNAME_METROLOGY_TEXT',    val_def='metrology.txt', type='str' )

        # GUIDark.py
        self.dark_more_opts    = self.declareParameter( name='DARK_MORE_OPTIONS',     val_def=True,          type='bool')

        # GUIData.py
        self.current_guidata_tab = self.declareParameter( name='CURRENT_GUIDATA_TAB',    val_def='Average',     type='str' )

        # GUIDarkRunGo.py
        self.str_run_number    = self.declareParameter( name='STRING_RUN_NUMBER',     val_def='None',         type='str' )
        self.str_run_from      = self.declareParameter( name='STRING_RUN_FROM',       val_def='0000',         type='str' )
        self.str_run_to        = self.declareParameter( name='STRING_RUN_TO',         val_def='end',          type='str' )

        # GUIDarkControlBar.py
        self.dark_list_show_runs  = self.declareParameter( name='DARK_LIST_SHOW_RUNS', val_def=self.list_of_show_runs[0], type='str' )
        self.dark_list_show_dets  = self.declareParameter( name='DARK_LIST_SHOW_DETS', val_def=self.list_of_show_dets[0], type='str' )
        self.dark_deploy_hotpix   = self.declareParameter( name='DARK_DEPLOY_HOTPIX',  val_def=True,                      type='bool')
        self.dark_deploy_cmod     = self.declareParameter( name='DARK_DEPLOY_CMODE',   val_def=True,                      type='bool')
        self.dark_list_run_min    = self.declareParameter( name='DARK_LIST_RUN_MIN',   val_def=1,      type='int' )
        self.dark_list_run_max    = self.declareParameter( name='DARK_LIST_RUN_MAX',   val_def=10,     type='int' )

        #PlotImgSpeWidget.py
        self.plot_intens_min = self.declareParameter( name='PLOT_INTENSITY_MIN',    val_def='', type='str' )
        self.plot_intens_max = self.declareParameter( name='PLOT_INTENSITY_MAX',    val_def='', type='str' )

        self.bat_dark_start    = self.declareParameter( name='BATCH_DARK_START',      val_def=1,        type='int' )
        self.bat_dark_end      = self.declareParameter( name='BATCH_DARK_END',        val_def=1000,     type='int' )
        self.bat_dark_scan     = self.declareParameter( name='BATCH_DARK_SCAN',       val_def=10,       type='int' )
        self.bat_dark_sele     = self.declareParameter( name='BATCH_DARK_EVCODES',    val_def=None,     type='str' )
        self.bat_det_info      = self.declareParameter( name='BATCH_DET_INFO',        val_def='DetInfo(:Princeton)',  type='str' )
        self.bat_img_rec_mod   = self.declareParameter( name='BATCH_IMG_REC_MODULE',  val_def='ImgAlgos.PrincetonImageProducer',  type='str' )
        self.mask_rms_thr_min  = self.declareParameter( name='MASK_PIX_MIN_THR_RMS',  val_def=  0.1,  type='float' )
        self.mask_rms_thr_max  = self.declareParameter( name='MASK_PIX_MAX_THR_RMS',  val_def=10000,  type='float' )
        self.mask_min_thr      = self.declareParameter( name='MASK_PIX_ADU_THR_MIN',  val_def=  0.1,  type='float' )
        self.mask_max_thr      = self.declareParameter( name='MASK_PIX_ADU_THR_MAX',  val_def=16000,  type='float' )
        self.mask_hot_is_used  = self.declareParameter( name='MASK_PIX_IS_USED',      val_def= True,  type='bool'  )
        self.mask_rmsnlo       = self.declareParameter( name='MASK_PIX_RMSNLO',       val_def=5,      type='float' )
        self.mask_rmsnhi       = self.declareParameter( name='MASK_PIX_RMSNHI',       val_def=5,      type='float' )
        self.mask_intnlo       = self.declareParameter( name='MASK_PIX_INTNLO',       val_def=5,      type='float' )
        self.mask_intnhi       = self.declareParameter( name='MASK_PIX_INTNHI',       val_def=5,      type='float' )

        # For batch jobs
        self.bat_queue               = self.declareParameter( name='BATCH_QUEUE',                val_def=self.list_of_queues[0], type='str' )
        self.bat_submit_interval_sec = self.declareParameter( name='BATCH_SUBMIT_INTERVAL_SEC',  val_def=30,      type='int' )

        # GUIMaskEditor.py
        cdir = '/reg/g/psdm/detector/alignment/cspad/calib-cxi-ds1-2014-03-19/calib/'
        def_fname_geometry    = cdir + 'CsPad::CalibV1/CxiDs1.0:Cspad.0/geometry/0-end.data'
        def_fname_roi_img_nda = cdir + '../cspad-ndarr-ave-cxii0114-r0227.npy'
        self.fname_geometry         = self.declareParameter( name='FNAME_GEOMETRY',             val_def=def_fname_geometry,              type='str' )
        self.fname_roi_img_nda      = self.declareParameter( name='FNAME_ROI_IMAGE_NDARRAY',    val_def=def_fname_roi_img_nda,           type='str' )
        self.fname_roi_img          = self.declareParameter( name='FNAME_ROI_IMAGE',            val_def='./work/roi_img.npy',            type='str' )
        self.fname_roi_mask_img     = self.declareParameter( name='FNAME_ROI_MASK_IMAGE',       val_def='./work/roi_mask_img.npy',       type='str' )
        self.fname_roi_mask_nda     = self.declareParameter( name='FNAME_ROI_MASK_NDARRAY',     val_def='./work/roi_mask_nda.txt',       type='str' )
        self.fname_roi_mask_nda_tst = self.declareParameter( name='FNAME_ROI_MASK_NDARRAY_TEST',val_def='./work/roi_mask_nda_tst.npy',   type='str' )
        self.sensor_mask_cbits      = self.declareParameter( name='SENSOR_MASK_CONTROL_BITS',   val_def=255,       type='int' )

        def_fname_geo         = cdir + 'CsPad::CalibV1/CxiDs1.0:Cspad.0/geometry/0-end.data'
        def_fname_geo_img_nda = cdir + '../cspad-ndarr-ave-cxii0114-r0227.dat'
        self.fname_geo_img_nda      = self.declareParameter( name='FNAME_GEO_IMAGE_NDARRAY',    val_def=def_fname_geo_img_nda,           type='str' )
        self.fname_geo_in           = self.declareParameter( name='FNAME_GEO_IN',               val_def=def_fname_geo,                   type='str' )
        self.fname_geo_out          = self.declareParameter( name='FNAME_GEO_OUT',              val_def='./work/geometry.data',          type='str' )
        self.geo_log_level          = self.declareParameter( name='GEO_LIST_LOG_LEVELS', val_def=self.list_geo_log_levels[1],            type='str' )

        # GUIFileManagerSingleControl.py
        #self.path_fm_selected   = self.declareParameter( name='PATH_FM_SELECTED',  val_def='./work/*.txt',       type='str' )

        # CommandLineCalib.py
        self.dsname             = self.declareParameter( name='DSNAME',            val_def='',       type='str' ) # 'exp=...:run=...:smd:dir=...'
        self.dsnamex            = self.declareParameter( name='DSNAMEX',           val_def='',       type='str' ) # './my/xtc'
        self.job_timeout_sec    = self.declareParameter( name='JOB_TIMEOUT_SEC',   val_def=2000,     type='int' )

        # GUIMaskEditor: parameters for med - mask editor command line
        self.med_line_width = self.declareParameter( name='MED_LINE_WIDTH',      val_def= 1,                type='int' )
        self.med_line_color = self.declareParameter( name='MED_LINE_COLOR',      val_def='k',               type='str' )
        self.med_picker     = self.declareParameter( name='MED_PICKER',          val_def= 5,                type='int' )
        self.med_img_fname  = self.declareParameter( name='MED_IMAGE_FNAME',     val_def='./work/plot.png', type='str' )


        self.list_of_dets   = ['CSPAD', 'CSPAD2x2', 'Princeton', 'pnCCD', 'Tm6740',\
                               'Opal1000', 'Opal2000', 'Opal4000', 'Opal8000',\
                               'OrcaFl40', 'Epix100a', 'Epix10ka', 'Epix10ka2M', 'Fccd960',\
                               'Rayonix', 'Andor', 'DualAndor', 'Jungfrau', 'Zyla',\
                               'Uxi', 'Pixis', 'StreakC7700', 'Archon', 'Acqiris', 'iStar', 'Alvium']

        self.list_of_dets_lower = [det.lower() for det in self.list_of_dets]

        self.list_of_data_types  = ['CsPad::DataV',
                                    'CsPad2x2::ElementV',
                                    'Princeton::FrameV',
                                    'PNCCD::FullFrameV',
                                    'Camera::FrameV',
                                    'Camera::FrameV',
                                    'Camera::FrameV',
                                    'Camera::FrameV',
                                    'Camera::FrameV',
                                    'Camera::FrameV',
                                    'Epix::ElementV',
                                    'Epix::ElementV',
                                    'Epix::ArrayV',
                                    'Camera::FrameV',
                                    'Camera::FrameV',
                                    'Andor::FrameV',
                                    'Andor3d::FrameV',
                                    'Jungfrau::ElementV1',
                                    'Zyla::FrameV',
                                    'Uxi::FrameV',
                                    'Pixis::FrameV',
                                    'Camera::FrameV',
                                    'Camera::FrameV',
                                    'Acqiris::DataDesc',
                                    'Zyla::FrameV',
                                    'Vimba::FrameV1']
        self.dict_of_det_data_types = dict( zip(self.list_of_dets, self.list_of_data_types) )
        #self.print_dict_of_det_data_types()

        self.list_of_calib_types = ['CsPad::CalibV1',
                                    'CsPad2x2::CalibV1',
                                    'Princeton::CalibV1',
                                    'PNCCD::CalibV1',
                                    'Camera::CalibV1',
                                    'Camera::CalibV1',
                                    'Camera::CalibV1',
                                    'Camera::CalibV1',
                                    'Camera::CalibV1',
                                    'Camera::CalibV1',
                                    'Epix100a::CalibV1',
                                    'Epix10ka::CalibV1',
                                    'Epix10ka2M::CalibV1',
                                    'Camera::CalibV1',
                                    'Camera::CalibV1',
                                    'Andor::CalibV1',
                                    'Andor3d::CalibV1',
                                    'Jungfrau::CalibV1',
                                    'Camera::CalibV1',
                                    'Uxi::CalibV1',
                                    'Pixis::CalibV1',
                                    'Camera::CalibV1',
                                    'Camera::CalibV1',
                                    'Acqiris::CalibV1',
                                    'iStar::CalibV1',
                                    'Alvium::CalibV1']
        self.dict_of_det_calib_types = dict( zip(self.list_of_dets, self.list_of_calib_types) )
        #self.print_dict_of_det_calib_types()

        det_cbx_states = [ (False, False ,'bool'), \
                           (False, False ,'bool'), \
                           (False, False ,'bool'), \
                           (False, False ,'bool'), \
                           (False, False ,'bool'), \
                           (False, False ,'bool'), \
                           (False, False ,'bool'), \
                           (False, False ,'bool'), \
                           (False, False ,'bool'), \
                           (False, False ,'bool'), \
                           (False, False ,'bool'), \
                           (False, False ,'bool'), \
                           (False, False ,'bool'), \
                           (False, False ,'bool'), \
                           (False, False ,'bool'), \
                           (False, False ,'bool'), \
                           (False, False ,'bool'), \
                           (False, False ,'bool'), \
                           (False, False ,'bool'), \
                           (False, False ,'bool'), \
                           (False, False ,'bool'), \
                           (False, False ,'bool'), \
                           (False, False ,'bool'), \
                           (False, False ,'bool'), \
                           (False, False ,'bool'), \
                           (False, False ,'bool') ]
        self.det_cbx_states_list = self.declareListOfPars( 'DETECTOR_CBX_STATE', det_cbx_states )

        self.const_types_cspad = [
            'center'
           ,'center_global'
           ,'offset'
           ,'offset_corr'
           ,'marg_gap_shift'
           ,'quad_rotation'
           ,'quad_tilt'
           ,'rotation'
           ,'tilt'
           ,'pedestals'
           ,'pixel_status'
           ,'status_extra'
           ,'common_mode'
           ,'filter'
           ,'pixel_gain'
           ,'pixel_rms'
           ,'pixel_mask'
           ,'pixel_bkgd'
           ,'geometry'
           #,'beam_vector'
           #,'beam_intersect'
            ]

        self.const_types_cspad2x2 = [
            'geometry'
           ,'center'
           ,'tilt'
           ,'pedestals'
           ,'pixel_status'
           ,'status_extra'
           ,'common_mode'
           ,'filter'
           ,'pixel_gain'
           ,'pixel_rms'
           ,'pixel_mask'
           ,'pixel_bkgd'
            ]

        self.const_types_princeton = [
            'pedestals'
           ,'pixel_status'
           ,'status_extra'
           ,'pixel_gain'
           ,'pixel_rms'
           ,'pixel_mask'
           ,'pixel_bkgd'
           ,'common_mode'
           ,'geometry'
            ]

        self.const_types_pnccd = [
            'pedestals'
           ,'pixel_status'
           ,'status_extra'
           ,'pixel_gain'
           ,'pixel_rms'
           ,'pixel_mask'
           ,'pixel_bkgd'
           ,'common_mode'
           ,'geometry'
            ]

        self.const_types_camera = [
            'pedestals'
           ,'pixel_status'
           ,'status_extra'
           ,'pixel_gain'
           ,'pixel_rms'
           ,'pixel_mask'
           ,'pixel_bkgd'
           ,'common_mode'
           ,'geometry'
            ]

        self.const_types_orcafl40 = [
            'pedestals'
           ,'pixel_status'
           ,'status_extra'
           ,'pixel_gain'
           ,'pixel_rms'
           ,'pixel_mask'
           ,'pixel_bkgd'
           ,'common_mode'
           ,'geometry'
            ]

        self.const_types_epix = [
            'pedestals'
           ,'pixel_status'
           ,'status_extra'
           ,'pixel_gain'
           ,'pixel_offset'
           ,'pixel_rms'
           ,'pixel_mask'
           ,'pixel_bkgd'
           ,'common_mode'
           ,'geometry'
            ]

        self.const_types_fccd960 = [
            'pedestals'
           ,'pixel_status'
           ,'status_extra'
           ,'pixel_gain'
           ,'pixel_rms'
           ,'pixel_mask'
           ,'pixel_bkgd'
           ,'common_mode'
           ,'geometry'
            ]

        self.const_types_andor = [
            'pedestals'
           ,'pixel_status'
           ,'status_extra'
           ,'pixel_gain'
           ,'pixel_rms'
           ,'pixel_mask'
           ,'pixel_bkgd'
           ,'common_mode'
           ,'geometry'
            ]

        self.const_types_andor3d = [
            'pedestals'
           ,'pixel_status'
           ,'status_extra'
           ,'pixel_gain'
           ,'pixel_rms'
           ,'pixel_mask'
           ,'pixel_bkgd'
           ,'common_mode'
           ,'geometry'
            ]

        self.const_types_jungfrau = [
            'pedestals'
           ,'pixel_status'
           ,'status_extra'
           ,'pixel_gain'
           ,'pixel_offset'
           ,'pixel_rms'
           ,'pixel_mask'
           ,'pixel_bkgd'
           ,'common_mode'
           ,'geometry'
            ]

        self.const_types_zyla = [
            'pedestals'
           ,'pixel_status'
           ,'status_extra'
           ,'pixel_gain'
           ,'pixel_rms'
           ,'pixel_mask'
           ,'pixel_bkgd'
           ,'common_mode'
           ,'geometry'
            ]

        self.const_types_uxi = [
            'pedestals'
           ,'pixel_status'
           ,'status_extra'
           ,'pixel_gain'
           ,'pixel_rms'
           ,'pixel_mask'
           ,'pixel_bkgd'
           ,'common_mode'
           ,'geometry'
            ]

        self.const_types_pixis = [
            'pedestals'
           ,'pixel_status'
           ,'status_extra'
           ,'pixel_gain'
           ,'pixel_rms'
           ,'pixel_mask'
           ,'pixel_bkgd'
           ,'common_mode'
           ,'geometry'
            ]

        self.const_types_streak = [
            'pedestals'
           ,'pixel_status'
           ,'status_extra'
           ,'pixel_gain'
           ,'pixel_rms'
           ,'pixel_mask'
           ,'pixel_bkgd'
           ,'common_mode'
           ,'geometry'
            ]

        self.const_types_archon = [
            'pedestals'
           ,'pixel_status'
           ,'status_extra'
           ,'pixel_gain'
           ,'pixel_rms'
           ,'pixel_mask'
           ,'pixel_bkgd'
           ,'common_mode'
           ,'geometry'
            ]

        self.const_types_acqiris = [
            'pedestals'
           ,'hex_config'
           ,'hex_table'
            ]

        self.const_types_istar = [
            'pedestals'
           ,'pixel_status'
           ,'status_extra'
           ,'pixel_gain'
           ,'pixel_rms'
           ,'pixel_mask'
           ,'pixel_bkgd'
           ,'common_mode'
           ,'geometry'
            ]

        self.const_types_alvium = [
            'pedestals'
           ,'pixel_status'
           ,'status_extra'
           ,'pixel_gain'
           ,'pixel_rms'
           ,'pixel_mask'
           ,'pixel_bkgd'
           ,'common_mode'
           ,'geometry'
            ]

        self.dict_of_det_const_types = dict( zip(self.list_of_dets, [ self.const_types_cspad
                                                                     ,self.const_types_cspad2x2
                                                                     ,self.const_types_princeton
                                                                     ,self.const_types_pnccd
                                                                     ,self.const_types_camera
                                                                     ,self.const_types_camera
                                                                     ,self.const_types_camera
                                                                     ,self.const_types_camera
                                                                     ,self.const_types_camera
                                                                     ,self.const_types_orcafl40
                                                                     ,self.const_types_epix
                                                                     ,self.const_types_epix
                                                                     ,self.const_types_epix
                                                                     ,self.const_types_fccd960
                                                                     ,self.const_types_camera
                                                                     ,self.const_types_andor
                                                                     ,self.const_types_andor3d
                                                                     ,self.const_types_jungfrau
                                                                     ,self.const_types_zyla
                                                                     ,self.const_types_uxi
                                                                     ,self.const_types_pixis
                                                                     ,self.const_types_streak
                                                                     ,self.const_types_archon
                                                                     ,self.const_types_acqiris
                                                                     ,self.const_types_istar
                                                                     ,self.const_types_alvium
                                                                      ]) )

        self.srcs_cspad = [
            'CxiDs1.0:Cspad.0'
           ,'CxiDs2.0:Cspad.0'
           ,'CxiDsd.0:Cspad.0'
           ,'MecTargetChamber.0:Cspad.0'
           ,'XcsEndstation.0:Cspad.0'
           ,'XppGon.0:Cspad.0'
            ]

        self.srcs_cspad2x2 = [
            'CxiDg2.0:Cspad2x2.0'
           ,'CxiDg2.0:Cspad2x2.1'
           ,'CxiSc1.0:Cspad2x2.0'
           ,'CxiSc2.0:Cspad2x2.0'
           ,'CxiSc2.0:Cspad2x2.1'
           ,'CxiSc2.0:Cspad2x2.2'
           ,'CxiSc2.0:Cspad2x2.3'
           ,'CxiSc2.0:Cspad2x2.4'
           ,'CxiSc2.0:Cspad2x2.5'
           ,'CxiSc2.0:Cspad2x2.6'
           ,'CxiSc2.0:Cspad2x2.7'
           ,'MecEndstation.0:Cspad2x2.6'
           ,'MecTargetChamber.0:Cspad2x2.0'
           ,'MecTargetChamber.0:Cspad2x2.1'
           ,'MecTargetChamber.0:Cspad2x2.2'
           ,'MecTargetChamber.0:Cspad2x2.3'
           ,'MecTargetChamber.0:Cspad2x2.4'
           ,'MecTargetChamber.0:Cspad2x2.5'
           ,'SxrBeamline.0:Cspad2x2.2'
           ,'SxrBeamline.0:Cspad2x2.3'
           ,'XcsEndstation.0:Cspad2x2.0'
           ,'XcsEndstation.0:Cspad2x2.1'
           ,'XppGon.0:Cspad2x2.0'
           ,'XppGon.0:Cspad2x2.1'
           ,'XppGon.0:Cspad2x2.2'
           ,'XppGon.0:Cspad2x2.3'
            ]

        self.srcs_princeton = [
            'CxiEndstation.0:Princeton.0'
           ,'MecTargetChamber.0:Princeton.0'
           ,'MecTargetChamber.0:Princeton.1'
           ,'MecTargetChamber.0:Princeton.2'
           ,'MecTargetChamber.0:Princeton.3'
           ,'MecTargetChamber.0:Princeton.4'
           ,'MecTargetChamber.0:Princeton.5'
           ,'SxrEndstation.0:Princeton.0'
           ,'XcsBeamline.0:Princeton.0'
            ]

        self.srcs_pnccd = [
            'Camp.0:pnCCD.0'
           ,'Camp.0:pnCCD.1'
           ,'SxrEndstation.0:pnCCD.0'
           ,'XcsEndstation.0:pnCCD.0'
            ]

        self.srcs_tm6740 = [
            'CxiDg1.0:Tm6740.0'
           ,'CxiDg2.0:Tm6740.0'
           ,'CxiDg4.0:Tm6740.0'
           ,'CxiDsd.0:Tm6740.0'
           ,'CxiDsu.0:Tm6740.0'
           ,'CxiKb1.0:Tm6740.0'
           ,'CxiSc1.0:Tm6740.0'
           ,'CxiSc2.0:Tm6740.0'
           ,'CxiSc2.0:Tm6740.1'
           ,'XcsBeamline.1:Tm6740.4'
           ,'XcsBeamline.1:Tm6740.5'
           ,'XppEndstation.1:Tm6740.1'
           ,'XppMonPim.1:Tm6740.1'
           ,'XppSb3Pim.1:Tm6740.1'
           ,'XppSb4Pim.1:Tm6740.1'
            ]

        self.srcs_opal1000 = [
            'AmoBPS.0:Opal1000.0'
           ,'AmoBPS.0:Opal1000.1'
           ,'AmoEndstation.0:Opal1000.0'
           ,'AmoEndstation.1:Opal1000.0'
           ,'AmoEndstation.2:Opal1000.0'
           ,'AmoVMI.0:Opal1000.0'
           ,'CxiDg3.0:Opal1000.0'
           ,'CxiEndstation.0:Opal1000.1'
           ,'CxiEndstation.0:Opal1000.2'
           ,'MecTargetChamber.0:Opal1000.1'
           ,'SxrBeamline.0:Opal1000.0'
           ,'SxrBeamline.0:Opal1000.1'
           ,'SxrBeamline.0:Opal1000.100'
           ,'SxrEndstation.0:Opal1000.0'
           ,'SxrEndstation.0:Opal1000.1'
           ,'SxrEndstation.0:Opal1000.2'
           ,'SxrEndstation.0:Opal1000.3'
           ,'XcsEndstation.0:Opal1000.0'
           ,'XcsEndstation.0:Opal1000.1'
           ,'XcsEndstation.1:Opal1000.1'
           ,'XcsEndstation.1:Opal1000.2'
           ,'XppEndstation.0:Opal1000.0'
           ,'XppEndstation.0:Opal1000.1'
           ,'XppEndstation.0:Opal1000.2'
            ]

        self.srcs_opal2000 = [
            'CxiEndstation.0:Opal2000.1'
           ,'CxiEndstation.0:Opal2000.2'
           ,'CxiEndstation.0:Opal2000.3'
           ,'MecTargetChamber.0:Opal2000.0'
           ,'MecTargetChamber.0:Opal2000.1'
           ,'MecTargetChamber.0:Opal2000.2'
            ]

        self.srcs_opal4000 = [
            'CxiEndstation.0:Opal4000.1'
           ,'CxiEndstation.0:Opal4000.3'
           ,'MecTargetChamber.0:Opal4000.0'
           ,'MecTargetChamber.0:Opal4000.1'
            ]

        self.srcs_opal8000 = [
            'MecTargetChamber.0:Opal8000.0'
           ,'MecTargetChamber.0:Opal8000.1'
            ]

        self.srcs_orcafl40 = [
            'XcsEndstation.0:OrcaFl40.0'
           ,'XppEndstation.0:OrcaFl40.0'
            ]

        self.srcs_epix = [
            'NoDetector.0:Epix.0'
           ,'XcsEndstation.0:Epix.0'
           ,'XcsEndstation.0:Epix.1'
            ]

        self.srcs_epix10k = [
            'NoDetector.0:Epix10k.0'
            ]

        self.srcs_epix10ka = [
            'MfxEndstation.0:Epix10ka.0'
            ]

        self.srcs_epix10ka2m = [
            'NoDetector.0:Epix10ka2M.0'
            ]

        self.srcs_epix100a = [
            'MecTargetChamber.0:Epix100a.0'
           ,'MfxEndstation.0:Epix100a.0'
           ,'NoDetector.0:Epix100a.0'
           ,'NoDetector.0:Epix100a.1'
           ,'XcsEndstation.0:Epix100a.0'
           ,'XcsEndstation.0:Epix100a.1'
           ,'XcsEndstation.0:Epix100a.2'
           ,'XcsEndstation.0:Epix100a.3'
           ,'XcsEndstation.0:Epix100a.4'
            ]

        self.srcs_fccd960 = [
            'XcsEndstation.0:Fccd960.0'
           ]

        self.srcs_rayonix = [
            'CxiEndstation.0:Rayonix.0'
           ,'MfxEndstation.0:Rayonix.0'
           ,'XppEndstation.0:Rayonix.0'
           ,'XppSb1Pim.0:Rayonix.0'
           ]

        self.srcs_andor = [
            'AmoEndstation.0:Andor.0'
           ,'MecTargetChamber.0:Andor.1'
           ,'MecTargetChamber.0:Andor.2'
           ,'SxrEndstation.0:Andor.0'
           ,'SxrEndstation.0:Andor.1'
           ,'SxrEndstation.0:Andor.2'
           ]

        self.srcs_andor3d = [
            'SxrEndstation.0:DualAndor.0'
           ]

        self.srcs_jungfrau = [
            'CxiEndstation.0:Jungfrau.0'
           ]

        self.srcs_zyla = [
            'XppEndstation.0:Zyla.0'
           ]

        self.srcs_uxi = [
            'DetLab.0:Uxi.0'
           ]

        self.srcs_pixis = [
            'MecTargetChamber.0:Pixis.1'
           ]

        self.srcs_streak = [
            'DetLab.0:StreakC7700.0'
           ]

        self.srcs_archon = [
            'SxrEndstation.0:Archon.0'
           ]

        self.srcs_acqiris = [
            'AmoETOF.0:Acqiris.0'
           ,'AmoITOF.0:Acqiris.0'
           ,'Camp.0:Acqiris.0'
           ,'CxiEndstation.0:Acqiris.0'
           ,'CxiSc1.0:Acqiris.0'
           ,'MecTargetChamber.0:Acqiris.0'
           ,'SxrEndstation.0:Acqiris.0'
           ,'SxrEndstation.0:Acqiris.1'
           ,'SxrEndstation.0:Acqiris.2'
           ,'SxrEndstation.0:Acqiris.3'
           ,'SxrEndstation.0:Acqiris.4'
           ,'XcsBeamline.0:Acqiris.0'
           ,'XppLas.0:Acqiris.0'
            ]

        self.srcs_istar = [
            'XcsEndstation.0:iStar.0'
           ,'XppEndstation.0:iStar.0'
           ,'DetLab.0:iStar.0'
           ]

        self.srcs_alvium = [
            'MecTargetChamber.0:Alvium.0',
           ]

        self.dict_of_det_sources = dict( zip(self.list_of_dets, [ self.srcs_cspad
                                                                 ,self.srcs_cspad2x2
                                                                 ,self.srcs_princeton
                                                                 ,self.srcs_pnccd
                                                                 ,self.srcs_tm6740
                                                                 ,self.srcs_opal1000
                                                                 ,self.srcs_opal2000
                                                                 ,self.srcs_opal4000
                                                                 ,self.srcs_opal8000
                                                                 ,self.srcs_orcafl40
                                                                 ,self.srcs_epix100a
                                                                 ,self.srcs_epix10ka
                                                                 ,self.srcs_epix10ka2m
                                                                 ,self.srcs_fccd960
                                                                 ,self.srcs_rayonix
                                                                 ,self.srcs_andor
                                                                 ,self.srcs_andor3d
                                                                 ,self.srcs_jungfrau
                                                                 ,self.srcs_zyla
                                                                 ,self.srcs_uxi
                                                                 ,self.srcs_pixis
                                                                 ,self.srcs_streak
                                                                 ,self.srcs_archon
                                                                 ,self.srcs_acqiris
                                                                 ,self.srcs_istar
                                                                 ,self.srcs_alvium
                                                                  ]) )


        self.dict_of_metrology_scripts = dict( zip(self.list_of_dets, [ ['CSPADV1', 'CSPADV2']
                                                                       ,['CSPAD2X2V1']
                                                                       ,['PRINCETONV1']
                                                                       ,['PNCCDV1']
                                                                       ,['TM6740V1']
                                                                       ,['OPAL1000V1']
                                                                       ,['OPAL2000V1']
                                                                       ,['OPAL4000V1']
                                                                       ,['OPAL8000V1']
                                                                       ,['ORCAFL40V1']
                                                                       ,['EPIX100AV1']
                                                                       ,['EPIX10KAV1']
                                                                       ,['EPIX10KA2MV1']
                                                                       ,['FCCD960V1']
                                                                       ,['RAYONIX']
                                                                       ,['ANDOR']
                                                                       ,['ANDOR3D']
                                                                       ,['JUNGFRAU']
                                                                       ,['ZYLA']
                                                                       ,['UXI']
                                                                       ,['PIXIS']
                                                                       ,['STREAK']
                                                                       ,['ARCHON']
                                                                       ,['ACQIRISV1']
                                                                       ,['ISTAR']
                                                                       ,['ALVIUM']
                                                                        ]) )


        self.list_of_det_pars = zip(self.list_of_dets, self.list_of_data_types, self.det_cbx_states_list)


    def list_of_dets_selected(self):
        return [det for det,state in zip(self.list_of_dets,self.det_cbx_states_list) if state.value()]

    def print_dict_of_det_data_types(self):
        s = 'List of detector names and associated types:'
        for det, type in self.dict_of_det_data_types.items():
            s += '\n%10s: %s' % (det, type)
        logger.info(s)

    def print_dict_of_det_calib_types(self):
        s = 'List of detector names and associated calibration types:'
        for det, type in self.dict_of_det_calib_types.items():
            s += '\n%10s: %s' % (det, type)
        logger.info(s)


    def defineStyles(self):
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
        #self.styleDefault   = "background-color: rgb(239, 235, 231, 255); color: rgb(0, 0, 0);" # Gray bkgd
        self.styleDefault   = ""
        #self.styleTitle  = "color: rgb(150, 160, 100);"
        self.styleBlue   = "color: rgb(100, 0, 150);"
        self.styleBlueM  = "color: rgb(200, 0, 150);"
        self.styleBuriy  = "color: rgb(150, 100, 50);"
        self.styleRed    = "color: rgb(255, 0, 0);"
        self.styleGreen  = "color: rgb(0, 150, 0);"
        self.styleYellow = "color: rgb(0, 150, 150);"

        #self.styleBkgd         = self.styleGreenMy # styleYellowish
        self.styleBkgd         = self.styleDefault
        self.styleTitle        = self.styleBlueM
        self.styleLabel        = self.styleBlue
        self.styleEdit         = self.styleWhite
        self.styleEditInfo     = self.styleGreenish # self.styleBkgd
        #self.styleEditInfo     = self.styleGreenish
        #self.styleEditInfo     = self.styleGreenish # Bluish
        self.styleEditBad      = self.styleRedBkgd
        self.styleButton       = self.styleGray
        self.styleButtonLeft   = self.styleButton + 'text-align: left;'
        self.styleButtonOn     = self.styleBluish
        self.styleButtonClose  = self.stylePink
        self.styleButtonWarning= self.styleYellowBkg
        self.styleButtonGood   = self.styleGreenPure
        #self.styleButtonBad    = self.stylePink
        self.styleButtonBad    = self.styleReddish
        self.styleBox          = self.styleGray
        self.styleCBox         = self.styleYellowish
        self.styleStatusGood   = self.styleGreen
        self.styleStatusWarning= self.styleYellow
        self.styleStatusAlarm  = self.styleRed
        self.styleTitleBold    = self.styleTitle + 'font-size: 18pt; font-family: Courier; font-weight: bold;'
        self.styleWhiteFixed   = self.styleWhite + 'font-family: Fixed;'

        self.colorEditInfo     = QtGui.QColor(100, 255, 200)
        self.colorEditBad      = QtGui.QColor(255,   0,   0)
        self.colorEdit         = QtGui.QColor('white')
        self.colorTabItem      = QtGui.QColor('white')

        self.styleTitleInFrame = self.styleWhite # self.styleDefault # self.styleWhite # self.styleGray

    def printParsDirectly(self):
        logger.info('Direct use of parameter:' + self.fname_ped.name() + ' ' + self.fname_ped.value(), self.name )
        logger.info('Direct use of parameter:' + self.fname_dat.name() + ' ' + self.fname_dat.value(), self.name )

    def close(self):
        if self.save_cp_at_exit.value():
            fname = self.fname_cp
            logger.info('save configuration parameters in file: %s' % fname, __name__)
            self.saveParametersInFile( fname )


confpars = ConfigParametersForApp()
cp = confpars


def test_ConfigParametersForApp():
    confpars.printParameters()
    #confpars.printParsDirectly()
    confpars.saveParametersInFile()


if __name__ == "__main__":
    import sys
    test_ConfigParametersForApp()
    sys.exit (0)

# EOF
