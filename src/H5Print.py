#--------------------------------------------------------------------------
# File and Version Information:
#  $Id: H5Print.py 13101 2017-01-29 21:22:43Z dubrovin@SLAC.STANFORD.EDU $
#
# Description:
#  Module H5Print
#------------------------------------------------------------------------

"""Print structure and content of HDF5 file

This software was developed for the SIT project.
If you use all or part of it, please give an appropriate acknowledgment.

@version $Id: H5Print.py 13101 2017-01-29 21:22:43Z dubrovin@SLAC.STANFORD.EDU $

@author Mikhail S. Dubrovin
"""
from __future__ import print_function
#------------------------------
import sys
import os
import time
import h5py
from CalibManager.H5Logger import log
#------------------------------

def print_hdf5_file_structure(fname):
    """Prints the HDF5 file structure"""

    offset = '    '
    f = h5py.File(fname, 'r') # open read-only
    print_hdf5_item_structure(f)
    f.close()
    log.info('=== EOF ===')

#------------------------------

def print_hdf5_item_structure(g, offset='    ') :
    """Prints the input file/group/dataset (g) name and begin iterations on its content"""
    msg = str_hdf5_item_structure('', g, offset)
    log.info(msg)
    #print msg

#------------------------------

def str_hdf5_item_structure(msg, g, offset='    ') :
    """Prints the input file/group/dataset (g) name and begin iterations on its content"""
    if   isinstance(g, h5py.File) :
        msg += '(File) %s %s\n' % (g.file, g.name)
        #print '%s (File) %s' % (g.file, g.name)
        
    elif isinstance(g, h5py.Dataset) :
        msg += '(Dataset) %s    shape=%s\n' % (g.name, str(g.shape)) #, g.dtype
        #print '(Dataset)', g.name, '    len =', g.shape #, g.dtype
        
    elif isinstance(g, h5py.Group) :
        msg += '(Group) %s\n' % g.name
        #print '(Group)', g.name

    else :
        #print 'WORNING: UNKNOWN ITEM IN HDF5 FILE', g.name
        log.info(msg)
        log.worning('WORNING: UNKNOWN ITEM IN HDF5 FILE %s\n' % g.name)
        sys.exit('EXECUTION IS TERMINATED')

    if isinstance(g, h5py.File) or isinstance(g, h5py.Group) :
        for key,val in dict(g).items() :
            subg = val
            #print offset, key, #,"   ", subg.name #, val, subg.len(), type(subg),
            msg += '%s%s' % (offset, key) #,"   ", subg.name #, val, subg.len(), type(subg),
            msg = str_hdf5_item_structure(msg, subg, offset + '    ')

    return msg

#------------------------------

def get_item_last_name(dsname):
    """Returns the last part of the full item name (after last slash)"""

    path,name = os.path.split(str(dsname))
    return name

def get_item_path_to_last_name(dsname):
    """Returns the path to the last part of the item name"""

    path,name = os.path.split(str(dsname))
    return path

def get_item_path_and_last_name(dsname):
    """Returns the path and last part of the full item name"""

    path,name = os.path.split(str(dsname))
    return path, name

#------------------------------

def get_item_second_to_last_name(dsname):
    """Returns the 2nd to last part of the full item name"""

    path1,name1 = os.path.split(str(dsname))
    path2,name2 = os.path.split(str(path1))

    return name2 

#------------------------------

def get_item_third_to_last_name(dsname):
    """Returns the 3nd to last part of the full item name"""

    path1,name1 = os.path.split(str(dsname))
    path2,name2 = os.path.split(str(path1))
    path3,name3 = os.path.split(str(path2))

    str(name3)

    return name3 

#------------------------------

def get_item_name_for_title(dsname):
    """Returns the last 3 parts of the full item name (after last slashes)"""

    path1,name1 = os.path.split(str(dsname))
    path2,name2 = os.path.split(str(path1))
    path3,name3 = os.path.split(str(path2))

    return name3 + '/' + name2 + '/' + name1

#------------------------------

def CSpadIsInTheName(dsname):
    
    path1,name1 = os.path.split(str(dsname))
    path2,name2 = os.path.split(str(path1))
    path3,name3 = os.path.split(str(path2))

    #print '       last name:', name1
    #print '2nd to last name:', name2
    #print '3rd to last name:', name3
    #print 'name3[0:5]', name3[0:5]

    cspadIsInTheName = False
    if name3[0:5] == 'CsPad' and name1 == 'data' : cspadIsInTheName = True
    #print 'cspadIsInTheName :', cspadIsInTheName

    return cspadIsInTheName

#------------------------------

def print_time(ds, ind):
    """DATA HDF5 ONLY! Prints formatted time if the dataset is 'time'"""
    
    item_last_name = get_item_last_name(str(ds.name))
    if item_last_name == 'time' :
        tarr = ds[ind]
        tloc = time.localtime(tarr[0]) # converts sec to tuple struct_time in local
        msg = 'Special stuff for "time" : %d sec, %d nsec, time local : %s' %\
              (tarr[0], tarr[1], time.strftime('%Y-%m-%d %H:%M:%S',tloc))
        
        log.info(msg)
        #tgmt = time.gmtime(tarr[0])    # converts sec to tuple struct_time in UTC
        #print 'time (GMT) :', time.strftime('%Y-%m-%d %H:%M:%S',tgmt)
    
#------------------------------

def is_dataset(ds):
    """Check if the input dataset is a h5py.Dataset (exists as expected in HDF5)"""
    return isinstance(ds, h5py.Dataset)

#------------------------------

def print_dataset_info(ds):
    """Prints attributes and all other available info for group or data"""
    if isinstance(ds, h5py.Dataset):

        msg = 'Dataset:  ds.name = %s  ds.dtype = %s  ds.shape = %s  ds.ndim  = %d' %\
            (ds.name, str(ds.dtype), str(ds.shape), len(ds.shape))
        log.info(msg)

        if len(ds.shape) > 0 :
            log.info('ds.shape[0] = %s' % str(ds.shape[0]))

        # Print data array
        if len(ds.shape)==1 and ds.shape[0] == 0 : #check if the ds.shape scalar and in not an array 
            log.info('%s - item has no associated data.' % get_item_last_name(ds.name))

        elif len(ds.shape)==0 or ds.shape[0] == 0  or ds.shape[0] == 1 : #check if the ds.shape scalar or array with dimension 0 or 1
            log.info('ds.value = %s' % str(ds.value))

        else : # ds.shape[0] < cp.confpars.eventCurrent: #check if the ds.shape array size less than current event number
            msg = ' data for ds[0]: %s' % str(ds[0])
            log.info(msg)            
            print_time(ds,0)

        #else :
        #    print " Assume that the array 1st index is an event number ", cp.confpars.eventCurrent
        #    print ds[cp.confpars.eventCurrent]
        #    print_time(ds,cp.confpars.eventCurrent)

        print_data_structure(ds)   

    if isinstance(ds, h5py.Group):
        msg = 'Group:\nds.name = %s' % ds.name
        log.info(msg)
        print_group_items(ds)

    if isinstance(ds, h5py.File):
        msg = 'File:\n  file.name = %s\n  Run number = %d' % (file.name, file.attrs['runNumber'])\
            + '\nds.id     = %s\nds.ref    = %s\nds.parent = %s\nds.file   = %s'%\
            (str(ds.id), str(ds.ref), str(ds.parent), str(ds.file))
        log.info(msg)

    #print_attributes(ds)

#------------------------------

def print_data_structure(ds):
    """Prints data structure of the dataset"""
    log.info(50*'-' + '\nUNROLL AND PRINT DATASET SUBSTRUCTURE')
    iterate_over_data_structure(ds)
    log.info(50*'-')

#------------------------------

def iterate_over_data_structure(ds, offset0=''):
    """Prints data structure of the dataset"""

    offset=offset0+'    '

    msg = '%sds.shape = %s  len(ds.shape) = %d  shape dimension(s) =' % (offset, str(ds.shape), len(ds.shape)) 
    if len(ds.shape) == 0 :
        msg += '%sZERO-CONTENT DATA! : ds.dtype=%s' % (offset, str(ds.dtype))
        log.info(msg)
        return

    for shapeDim in ds.shape:
        msg += '%s'%str(shapeDim)
        log.info('%s  '%msg)

    if len(ds.shape) > 0 :
        log.info('%sSample of data ds[0]=%s' % (offset, str(ds[0])))

    if len(ds.dtype) == 0 or ds.dtype.names == None :
        msg = '%sNO MORE DAUGHTERS AVAILABLE because len(ds.dtype) = %d ds.dtype.names =%s'%\
              (offset, len(ds.dtype), str(ds.dtype.names))
        log.info(msg)
        return

    msg = '%sds.dtype        =%s\n%sds.dtype.names  =%s' % (offset, str(ds.dtype), offset, str(ds.dtype.names))
    log.info(msg)

    if ds.dtype.names==None :
        log.info('%sZERO-DTYPE.NAMES!' % offset)
        return

    for indname in ds.dtype.names :
        log.info('%sIndex Name =%s' % (offset, indname))      
        iterate_over_data_structure(ds[indname], offset)

#------------------------------

def print_file_info(file):
    """Prints attributes and all other available info for group or data"""
    msg =   "file.name           = %s" % file.name\
        + "\nfile.attrs          = %s" % str(file.attrs)\
        + "\nfile.attrs.keys()   = %s" % str(list(file.attrs.keys()))\
        + "\nfile.attrs.values() = %s" % str(list(file.attrs.values()))\
        + "\nfile.id             = %s" % str(file.id)\
        + "\nfile.ref            = %s" % str(file.ref)\
        + "\nfile.parent         = %s" % str(file.parent)\
        + "\nfile.file           = %s" % str(file.file)
    log.info(msg)

    #print "Run number          = ", file.attrs['runNumber']
    print_attributes(file)

#------------------------------

def print_group_items(g):
    """Prints items in this group"""

    list_of_items = list(g.items())
    Nitems = len(list_of_items)
    log.info('Number of items in the group = %d' % Nitems)
    #print "g.items() = ", list_of_items
    if Nitems != 0 :
        for item in list_of_items :
            log.info('     %s' % str(item)) 
                        
#------------------------------

def print_attributes(ds):
    """Prints all attributes for data set or file"""

    Nattrs = len(ds.attrs)
    log.info('Number of attrs.  = %d' % Nattrs)
    if Nattrs != 0 :
        msg = '  ds.attrs          = %s\n  ds.attrs.keys()   = %s\n  ds.attrs.values() = %s\n  Attributes :' %\
              (str(ds.attrs), str(list(ds.attrs.keys())), str(list(ds.attrs.values())))
        log.info(msg)
        for key,val in dict(ds.attrs).items() :
            log.info('%24s : %s' % (key, val))

#------------------------------

def print_dataset_metadata_from_file(fname, dsname):
    """Open file and print attributes for input dataset"""

    # Check for unreadable datasets:
    #if(dsname == '/Configure:0000/Run:0000/CalibCycle:0000/CsPad::ElementV1/XppGon.0:Cspad.0/data'):
    #    print 'This is CSpad data'
    #    return

    #if(dsname == '/Configure:0000/Run:0000/CalibCycle:0000/EvrData::DataV3/NoDetector.0:Evr.0'):
    #    print 'TypeError: No NumPy equivalent for TypeVlenID exists...\n',70*'='
    #    return

    #if(dsname == '/Configure:0000/Run:0000/CalibCycle:0000/EvrData::DataV3/NoDetector.0:Evr.0/evrData'):
    #    print 'TypeError: No NumPy equivalent for TypeVlenID exists...\n',70*'='        
    #    return

    #fname = cp.confpars.dirName+'/'+cp.confpars.fileName
    log.info('Open file : %s' % fname, 'print_dataset_metadata_from_file')
    f  = h5py.File(fname, 'r') # open read-only
    ds = f[dsname]
    print_dataset_info(ds)
    print_attributes(ds)
    #log.info('Path: %s' % str(dsname))
    f.close()
    log.info(70*'_')

#------------------------------

def get_list_of_dataset_par_names(fname, dsname=None):
    """Makes a list of the dataset parameter names"""

    get_list_of_dataset_par_names = []
    if dsname=='None'  or \
       dsname=='Index' or \
       dsname=='Time'  or \
       dsname=='Is-not-used' or \
       dsname=='Select-X-parameter' :

        get_list_of_dataset_par_names.append('None')
        return get_list_of_dataset_par_names

    #fname = cp.confpars.dirName+'/'+cp.confpars.fileName
    f = h5py.File(fname, 'r') # open read-only
    ds = f[dsname]

    for parName in ds.dtype.names :
        print(parName)
        get_list_of_dataset_par_names.append(parName)

    f.close()

    get_list_of_dataset_par_names.append('None')
    return get_list_of_dataset_par_names

#------------------------------

def get_list_of_dataset_par_indexes(dsname=None, parname=None):
    """Makes a list of the dataset parameter indexes"""

    list_of_dataset_par_indexes = []
    if dsname=='None'  or \
       dsname=='Index' or \
       dsname=='Time'  or \
       dsname=='Is-not-used' or \
       dsname=='Select-X-parameter' :

        list_of_dataset_par_indexes.append('None')
        return list_of_dataset_par_indexes


    if not (parname=='ipimbData'   or \
            parname=='ipimbConfig' or \
            parname=='ipmFexData') :

        list_of_dataset_par_indexes.append('None')
        return list_of_dataset_par_indexes
 
    fname = cp.confpars.dirName+'/'+cp.confpars.fileName
    f = h5py.File(fname, 'r') # open read-only
    ds = f[dsname]

    dspar = ds[parname]

    for parIndex in dspar.dtype.names :
        print(parIndex)
        list_of_dataset_par_indexes.append(parIndex)

    f.close()

    list_of_dataset_par_indexes.append('None')
    return list_of_dataset_par_indexes

                            
#------------------------------

def usage() :
    #print '\nUsage: %s fname.h5' % os.path.basename(sys.argv[0])
    print('\nUsage: python %s fname.h5' % (sys.argv[0]))

#----------------------------------
if __name__ == "__main__" :

    log.setPrintBits(0o377)
    #fname = sys.argv[1] if len(sys.argv)==2 else '/reg/d/psdm/CXI/cxitut13/hdf5/cxitut13-r0135.h5'    
    fname = sys.argv[1] if len(sys.argv)==2 else '/reg/g/psdm/detector/calib/epix100a/epix100a-test.h5'    
    print_hdf5_file_structure(fname)
    #log.saveLogInFile('log-test.txt')
    usage()
    sys.exit ( "End of test" )

#----------------------------------
