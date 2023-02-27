#!/usr/bin/env python

""" Processing of optical measurements for CSPAD2x2

@see OpticAlignmentCspadMethods.py

@author Mikhail S. Dubrovin
"""
from __future__ import print_function
from CalibManager.OpticAlignmentCspadMethods import *

class OpticAlignmentCspad2x2V1(OpticAlignmentCspadMethods):
    """OpticAlignmentCspad2x2V1"""

    nquads  = 1
    nsegms  = 2
    npoints = 8

    #Base index of 2x1s in the quad:
    #        0  1
    ibase = [1, 5]

    #Segment origin index
    iorgn = [4, 8]

    #sensor_rotation = [180,180]
    sensor_n90_in_quad = [2,2]

    quad_n90_in_det = [0]


    def __init__(self, fname, path='calib-tmp', save_calib_files=True, print_bits=0o7777, plot_bits=0o377, exp='Any', det='CSPAD2X2', n90=0):
        """Constructor."""

        if print_bits &  1: print('Start OpticAlignmentCspad2x2V1')

        assert os.path.lexists(fname), 'optical metrology (txt) file IS NOT FOUND: %s' % fname

        self.fname            = fname
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


    def present_results(self):

        if self.print_bits & 2: print('\n' + self.txt_deviation_from_flatness())
        if self.print_bits & 4: print('\nQuality check in XY plane:\n', self.txt_qc_table_xy())
        if self.print_bits & 8: print('\nQuality check in Z:\n', self.txt_qc_table_z())

        geometry_txt   = self.txt_geometry()
        if self.print_bits & 128: print('\nCalibration type "geometry"\n%s' % geometry_txt)

        if self.save_calib_files:
            self.create_directory(self.path)
            self.save_text_file(self.fname_geometry, geometry_txt)

        if self.plot_bits & 1:
            print('Draw array from metrology file')
            self.drawOpticalAlignmentFile()


    def readOpticalAlignmentFile(self):
        """Reads the metrology.txt file with original optical measurements for a single CSPAD2x2
        """
        if self.print_bits & 1: print('readOpticalAlignmentFile()')

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

            #if len(line) == 1: continue # ignore empty lines
            #print len(line),  ' Line: ', line
            if not line: continue   # discard empty strings

            list_of_fields = line.split()

            if list_of_fields[0] == 'Quad': # Treat quad header lines
                self.quad = int(list_of_fields[1])
                if self.print_bits & 256: print('Stuff for quad', self.quad)
                continue

            if list_of_fields[0] == 'Sensor' \
            or list_of_fields[0] == 'Point': # Treat the title lines
                if self.print_bits & 256: print('Comment line:', line)
                continue

            if len(list_of_fields) != 4: # Ignore lines with non-expected number of fields
                if self.print_bits & 256: print('len(list_of_fields) =', len(list_of_fields), end=' ')
                if self.print_bits & 256: print('RECORD IS IGNORED due to unexpected format of the line:',line)
                continue

            point, X, Y, Z = [int(v) for v in list_of_fields]

            #record = [point, X, Y, Z, Title]
            if self.print_bits & 256: print('ACCEPT RECORD:', point, X, Y, Z) #, Title

            self.arr_opt[self.quad,point,:] = [point, X, Y, Z]

        file.close()

        if self.print_bits & 256: print('\nArray of alignment info:\n', self.arr_opt)

        self.arr = self.arr_opt


    def txt_geometry_det_ip(self):
        txt = ''
        name_object = 'CSPAD2X2:V1'
        name_parent = 'IP'
        num_parent, num_object, x0, y0, z0, rotXY, rotXZ, rotYZ, tiltXY, tiltXZ, tiltYZ = 0,0,0,0,1e6,0,0,0,0,0,0
        txt += self.str_fmt() % \
            (name_parent.ljust(12), num_parent, name_object.ljust(12), num_object, \
            x0, y0, z0, rotXY, rotXZ, rotYZ, tiltXY, tiltXZ, tiltYZ)

        return txt + '\n'


    def txt_geometry(self):
        return self.txt_geometry_header() + \
               self.txt_geometry_segments(name_segm='SENS2X1:V1', name_parent='CSPAD2X2:V1') + \
               self.txt_geometry_det_ip()

def main():

    #fname = 'CSPad2x2-1.txt'
    #fname = 'CSPad2x2-2.txt'
    #fname = 'CSPad2x2-3.txt'
    #fname = 'CSPad2x2-4.txt'
    #fname = 'CSPad2x2-5.txt'
    #fname = 'CSPad2x2-6.txt'
    #fname = '2014-04-25-CSPAD2X2-3-MEC-Metrology.txt'
    #base_dir = '/reg/neh/home1/dubrovin/LCLS/CSPad2x2Metrology/CSPad2x2'

    fname = 'optical_metrology.txt'
    base_dir = gu.get_cwd()  # '/reg/g/psdm/detector/alignment/cspad/calib-.../'

    (opts, args) = input_option_parser(base_dir, fname)
    path_metrol = os.path.join(opts.dir, opts.fname)

    OpticAlignmentCspad2x2V1(path_metrol, print_bits=opts.pbits, plot_bits=opts.gbits, n90=opts.n90)
    sys.exit()

if __name__ == '__main__':
    main()

# EOF
