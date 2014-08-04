#!/usr/bin/env python

class Helper:
    def __init__(self):
        pass
        
    def fileRead(self, file, mode):
        file1 = open(file,mode)
        string = [i for i in file1]
        return string
