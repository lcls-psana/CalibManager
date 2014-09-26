#!/usr/bin/env python

#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#------------------------------------------------------------------------
""" Processing of optical measurements for XPP-CSPAD (fixed geometry)

@see OpticAlignmentCspadMethods.py

@version $Id$

@author Mikhail S. Dubrovin
"""

#------------------------------
__version__ = "$Revision$"
# $Source$
#----------------------------------
#import os
#import sys
#import numpy
#import numpy as np
#import math
#from time import localtime, gmtime, strftime, clock, time, sleep

#import matplotlib.pyplot as plt
#import matplotlib.lines  as lines

from CalibManager.OpticAlignmentCspadMethods import *
#from OpticAlignmentCspadMethods import *

#----------------------------------
#  Numeration of quads in the metrology file should be consistent with numeration in DAQ.
#  Orientation of CSPAD for
#
#  n90=0,          n90=1, etc.
#  ^               ^           
#  | Q0  Q1        | Q1  Q2    
#  |               |           
#  | Q3  Q2        | Q0  Q3    
#  +-------->      +-------->  
#
#----------------------------------

class OpticAlignmentCspad2x2V1 (OpticAlignmentCspadMethods) :
    """OpticAlignmentCspad2x2V1"""

    nquads  = 1
    nsegms  = 2
    npoints = 8

    #Base index of 2x1s in the quad:
    #        0  1  
    ibase = [1, 5] 

    #Segment origin index
    iorgn = [2, 6]

    #sensor_rotation = [0,0,270,270,180,180,270,270]
    sensor_n90_in_quad = [0,0]

    quad_n90_in_det = [0]


    def __init__(self, fname=None, path='calib-tmp', save_calib_files=True, print_bits=07777, plot_bits=0377, exp='Any', det='CSPAD2X1', n90=0):
        """Constructor."""

        if print_bits &  1 : print 'Start OpticAlignmentCspad2x2V1'

        if fname != None : self.fname = fname
        else             : self.fname = '/reg/neh/home1/dubrovin/LCLS/CSPadMetrologyProc/metrology_standard.txt'

        if not os.path.lexists(self.fname) : 
            if print_bits &  1 : print 'Non-available input file: ' + self.fname
            return

        self.path             = path
        self.save_calib_files = save_calib_files
        self.print_bits       = print_bits
        self.plot_bits        = plot_bits
        self.exp              = exp
        self.det              = det

        self.fname_geometry   = os.path.join(self.path, 'geometry-0-end.data')
        self.fname_plot_det   = os.path.join(self.path, 'metrology_standard_det.png')

        self.readOpticalAlignmentFile()
        self.evaluate_deviation_from_flatness()
        self.evaluate_center_coordinates()
        self.evaluate_length_width_angle()

        self.present_results()


#----------------------------------

    def present_results(self): 

        if self.print_bits & 2 : print '\n' + self.txt_deviation_from_flatness()
        if self.print_bits & 4 : print '\nQuality check in XY plane:\n', self.txt_qc_table_xy() 
        if self.print_bits & 8 : print '\nQuality check in Z:\n', self.txt_qc_table_z()

        geometry_txt   = self.txt_geometry()
        if self.print_bits & 128 : print '\nCalibration type "geometry"\n%s' % geometry_txt

        if self.save_calib_files :
            self.create_directory(self.path)
            self.save_text_file(self.fname_geometry, geometry_txt)

        if self.plot_bits & 1 :
            print 'Draw array from metrology file'
            self.drawOpticalAlignmentFile()

#----------------------------------

    def readOpticalAlignmentFile(self): 
        """Reads the metrology.txt file with original optical measurements for a single CSPAD2x1
        """
        if self.print_bits & 1 : print 'readOpticalAlignmentFile()'

                                 # quad 0:3
                                   # point 1:32
                                      # record: point, X, Y, Z 0:3
        self.arr_opt = numpy.zeros( (self.nquads,self.npoints+1,4), dtype=numpy.int32 )
        self.quad = 0
        
        #infile = './2012-01-12-Run5-DSD-Metrology-corrected.txt'
        file = open(self.fname, 'r')
        # Print out 7th entry in each line.
        for linef in file:

            line = linef.strip('\n')

            #if len(line) == 1 : continue # ignore empty lines
            #print len(line),  ' Line: ', line
            if not line : continue   # discard empty strings

            list_of_fields = line.split()

            if list_of_fields[0] == 'Quad' : # Treat quad header lines
                self.quad = int(list_of_fields[1])
                if self.print_bits & 256 : print 'Stuff for quad', self.quad  
                continue

            if list_of_fields[0] == 'Sensor' \
            or list_of_fields[0] == 'Point' : # Treat the title lines
                if self.print_bits & 256 : print 'Comment line:', line  
                continue
            
            if len(list_of_fields) != 4 : # Ignore lines with non-expected number of fields
                if self.print_bits & 256 : print 'len(list_of_fields) =', len(list_of_fields),
                if self.print_bits & 256 : print 'RECORD IS IGNORED due to unexpected format of the line:',line
                continue              

            point, X, Y, Z = [int(v) for v in list_of_fields]
            
            #record = [point, X, Y, Z, Title]
            if self.print_bits & 256 : print 'ACCEPT RECORD:', point, X, Y, Z #, Title

            self.arr_opt[self.quad,point,:] = [point, X, Y, Z]

        file.close()

        if self.print_bits & 256 : print '\nArray of alignment info:\n', self.arr_opt

        self.arr = self.arr_opt


#----------------------------------

#    def txt_geometry_segments(self) :
#        txt = ''        
#        name_segm   = 'SENS2X1:V1'
#        segm_index  = -1
#        name_parent = 'CSPAD2X1:V1'
#        name_index  = 0
#        rotXZ, rotYZ = 0,0
#        for quad in range(self.nquads) :
#            for segm in range(self.nsegms) :
#                segm_index += 1 
#                txt += '%s %3d  %s %3d   %7d %7d %7d   %5d %5d %5d   %8.5f %8.5f %8.5f \n' % \
#                       (name_parent.ljust(12), name_index, name_segm.ljust(12), segm_index, \
#                       self.arrXmu[quad][segm], \
#                       self.arrYmu[quad][segm], \
#                       self.arrZmu[quad][segm], \
#                       self.rotXYDegree[quad][segm], \
#                       rotXZ, \
#                       rotYZ, \
#                       self.tiltXYDegree[quad][segm], \
#                       self.tiltXZDegree[quad][segm], \
#                       self.tiltYZDegree[quad][segm])
#            txt += '\n' 
#        return txt

#----------------------------------
 
    def txt_geometry(self) :
        return self.txt_geometry_header() + \
               self.txt_geometry_segments(name_segm='SENS2X1:V1', name_parent='CSPAD2X1:V1')
               #self.txt_geometry_quads()

#----------------------------------
#----------------------------------
#----------------------------------
#----------------------------------

def main():

    fname = '2014-04-25-CSPAD2X2-3-MEC-Metrology.txt'

    base_dir = '/reg/neh/home1/dubrovin/LCLS/CSPad2x2Metrology/CSPad2x2'
    path_metrol = os.path.join(base_dir,fname)

    OpticAlignmentCspad2x2V1(path_metrol, print_bits=0777, plot_bits=0377)
    sys.exit()

if __name__ == '__main__':
    main()

#----------------------------------