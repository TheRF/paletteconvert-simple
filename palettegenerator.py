#!/usr/bin/env python3
import sys
import re
from helper import Helper


class Palette:
    
    def __init__(self, filename='template.gpl', name='Template', columns=0, colors=[(0,0,0)]):
        self.filename = filename
        self.name = name
        self.columns = columns
        self.colors = colors

    def gimpToJasc(self, oldPalette):
        oldpal = []
        try:
            help = Helper()
            oldpal = help.fileRead(oldPalette, 'r')
            print('read successfull')
            #print(oldpal)
            # get colors
            tmp1 = oldpal[4:]
            tmp2 = []
            for i in tmp1:
                tmp2.append(re.findall('\d+', i))
            #print(tmp2)
            self.colors = tmp2
            self.filename = oldPalette+'.pal'
            self.writeJascPalette()
        except:
            print("Error found:", sys.exc_info()[0])
            raise
        
    def jascToGimp(self, oldPalette):
        oldpal = []
        try:
            help = Helper()
            oldpal = help.fileRead(oldPalette, 'r')
            print('read successfull')
            tmp1 = oldpal[3:]
            tmp2 = []
            for i in tmp1:
                tmp2.append(re.findall('\d+', i))
            self.colors = tmp2
            self.filename = oldPalette+'.gpl'
            self.writeGimpPalette()
        except:
            print("Error found:", sys.exc_info()[0])
            raise
        
    def convertPalette(self, oldPalette= '', convert='none'):
        if convert.find('GimpToJASC') != -1:
            self.gimpToJasc(oldPalette)
        elif convert.find('JASCToGimp') != -1:
            self.jascToGimp(oldPalette)
        else:
            return
        
    def writeJascPalette(self):
        palette = open(self.filename, 'w')
        palette.write('JASC-PAL\n')
        palette.write('0100\n')
        palette.write('256\n')
        
        for col in self.colors:
            indices = str(col[0])+' '+str(col[1])+' '+str(col[2])+'\n'
            palette.write(indices)
        
    def writeJascPalette2(self):
        palette = open(self.filename, 'w')
        palette.write('JASC-PAL\n')
        palette.write('0100\n')
        palette.write('256\n')
        
        for col in range(0,256):
            palette.write(str(self.colors[0][0])+' '+str(self.colors[0][1])+' '+str(self.colors[0][2])+'\n')
        
    def writeGimpPalette(self):
        palette = open(self.filename, 'w')
        palette.write('GIMP Palette\n')
        palette.write('Name: '+self.name+'\n')
        palette.write('Columns: '+str(self.columns)+'\n')
        palette.write('#\n')
        
        index = 0
        for col in self.colors:
            indices = ' '+str(col[0])+'   '+str(col[1])+'  '+str(col[2])+'\t'+'Index'+str(index)+'\n'
            palette.write(indices)
            index = index + 1
        
    def writeGimpPalette2(self):
        palette = open(self.filename, 'w')
        palette.write('GIMP Palette\n')
        palette.write('Name: '+self.name+'\n')
        palette.write('Columns: '+str(self.columns)+'\n')
        palette.write('#\n')
        
        index = 0
        for col in range(0,256):
            indices = ' '+str(self.colors[0][0])+'   '+str(self.colors[0][1])+'  '+str(self.colors[0][2])+'\t'+'Index'+str(index)+'\n'
            palette.write(indices)
            index = index + 1
        
if __name__ == '__main__':
    gimp = Palette()
    gimp.convertPalette(oldPalette='Random.pal', convert='JASCToGimp')
