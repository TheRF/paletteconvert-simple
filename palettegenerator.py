#!/usr/bin/env python3
import sys
import re

class Helper:
    '''simple helper class for file manipulation
    methods:
            file_read = main method for file input
    '''
    def __init__(self):
        '''constructor'''
        pass

#------------------

    def file_read(self, file, mode):
        '''read a file
        arguments:
                file = name and location of the file that should be read
                mode = should be 'r' for read
        returns:
                list of strings containing file data
        '''
        file1 = open(file,mode)
        string = [i for i in file1]
        return string

#-----------------

class PaletteError(Exception):
    '''base error class for palettes'''
    def __init__(self, message):
        self.message = message

#-----------------

class Palette:
    '''our base palette class
    methods:
            gimp_to_jasc = converts a gimp palette into jasc format
            jasc_to_gimp = converts a jasc palette into gimp format
            convert_palette = wrapper for above methods
            write_jasc_palette = use a list of color tuples to write a jasc palette file
            write_gimp_palette = use a list of color tuples to write a jasc palette file
    '''
    def __init__(self):
        '''constructor'''
        pass

#--------------------------

    def gimp_to_jasc(self, oldPalette, outfile=''):
        '''read the gimp file and rewrite the info as a jasc file
        arguments:
                oldPalette = name of the old palette file
                outfile = name of the new palette file
        '''
        oldpal = []
        try:
            # we read the file
            help = Helper()
            oldpal = help.file_read(oldPalette, 'r')
            tmp1 = oldpal[4:]
            tmp2 = []
            # parse all the rgb tupels
            for i in tmp1:
                tmp2.append(re.findall('\d+', i))
            colors = tmp2
            out = ''
            # write the new file
            if outfile == '':
                out = oldPalette+'.pal'
            else:
                out = outfile
            self.write_jasc_palette(colors, out)
        except:
            raise PaletteError(message='Error during gimp to jasc conversion: '+sys.exc_info()[0])

#---------------------------

    def jasc_to_gimp(self, oldPalette, outfile=''):
        '''read the jasc file and rewrite the info as a gimp file
        arguments:
                oldPalette = name of the old palette file
                outfile = name of the new palette file
        '''
        oldpal = []
        try:
            # we read the file
            help = Helper()
            oldpal = help.file_read(oldPalette, 'r')
            tmp1 = oldpal[3:]
            tmp2 = []
            # parse all the rgb tupels
            for i in tmp1:
                tmp2.append(re.findall('\d+', i))
            colors = tmp2
            # write the new file
            out = ''
            if outfile == '':
                out = oldPalette+'.gpl'
            else:
                out = outfile
            self.write_gimp_palette(colors, out)
        except:
            raise PaletteError(message='Error during jasc to gimp conversion: '+sys.exc_info()[0])

#----------------------------

    def convert_palette(self, oldPalette= '', convert='none', outfile=''):
        '''depending on the mode we determine which conversion should take place
        arguments:
                oldPalette = file name of the old palette
                convert = modus that we want to use; either GimpToJASC or JASCToGimp
                outfile = name out the target palette file
        '''
        # determine which format we want to convert
        if convert.find('GimpToJASC') != -1:
            # we have a gimp file
            out = ''
            if outfile == '':
                out = oldPalette+'.pal'
            else:
                out = outfile
            self.gimp_to_jasc(oldPalette, outfile=out)
        elif convert.find('JASCToGimp') != -1:
            # we have a jasc file
            out = ''
            if outfile == '':
                out = oldPalette+'.gpl'
            else:
                out = outfile
            self.jasc_to_gimp(oldPalette, outfile=out)
        else:
            # we have nothing, throw an error
            raise PaletteError(message='wrong or missing convert-parameter: must be JASCToGimp, or GimpToJASC')
        
#-----------------------------
        
    def write_jasc_palette(self, colors, outfile=''):
        '''we take a list of colors and put it into a JASC palette file
        arguments:
                colors = list of RGB tuples; each tupel is one color
        '''
        # we determine the name of the output file
        out = ''
        if outfile == '':
            out = 'palette.pal'
        else:
            out = outfile
        # first we write the palette header
        palette = open(out, 'w')
        palette.write('JASC-PAL\n')
        palette.write('0100\n')
        palette.write('256\n')
        
        # then we add each color tupel line after line
        for col in colors:
            indices = str(col[0])+' '+str(col[1])+' '+str(col[2])+'\n'
            palette.write(indices)
         
#-------------------------
         
    def write_gimp_palette(self, colors, outfile='', columns=0, name='palette'):
        '''we take a list of colors and put it into a Gimp palette file
        arguments:
                colors = list of RGB tuples; each tupel is one color
        '''
        # we determine the name of the output file
        out = ''
        if outfile == '':
            out = 'palette.pal'
        else:
            out = outfile
        # we write the palette header
        palette = open(out, 'w')
        palette.write('GIMP Palette\n')
        palette.write('Name: '+name+'\n')
        palette.write('Columns: '+str(columns)+'\n')
        palette.write('#\n')
        
        # then we add each color tupel line after line
        index = 0
        for col in colors:
            indices = ' '+str(col[0])+'   '+str(col[1])+'  '+str(col[2])+'\t'+'Index'+str(index)+'\n'
            palette.write(indices)
            index = index + 1
            
#-------------------------
