# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

from os import path
from chardet.universaldetector import UniversalDetector
import codecs
import re


class IncludeFile(object):
    """docstring for IncludeFile"""
    def __init__(self):
        super(IncludeFile, self).__init__()
        self.parentFileName = None
        self.fileName = None
        self.encodeType = 'utf-8'
        self.lines = []
        self.foundIndex = 0
        self.startPosition = 0
        self.endPosition = 0
        self.indentStr = ''

    def load_file(self):
        includeFile = open(self.fileName, mode='r')
        detector = UniversalDetector()
        rawLines = includeFile.readlines()
        for line in rawLines:
            detector.feed(line)
            if detector.done: 
                break
        detector.close()
        self.encodeType = detector.result['encoding']
        for line in rawLines:
            self.lines.append(line.decode(self.encodeType).encode('utf-8'))
        includeFile.close()



class MaxScript(object):
    """docstring for MaxScript"""
    def __init__(self):
        super(MaxScript, self).__init__()
        self.fileDir = ''
        self.fileName = ''
        self.encodeType = 'utf-8'
        self.file = None
        self.lines = []
        self.includeFiles = []
        self.resultFileFullname = ''
        self.returnMessage = 'Process success'

    def reset_process(self):
        self.fileDir = ''
        self.fileName = ''
        self.encodeType = 'utf-8'
        self.file = None
        self.lines = []
        self.includeFiles = []
        self.resultFileFullname = ''
        self.returnMessage = 'Process success'

    def load_file(self, inputFullFileName):
        self.fileDir = path.dirname(inputFullFileName)
        self.fileName = path.basename(inputFullFileName)

        scriptFile = open(inputFullFileName, mode='r')
        detector = UniversalDetector()
        rawLines = scriptFile.readlines()
        for line in rawLines:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
        self.encodeType = detector.result['encoding']
        for line in rawLines:
            self.lines.append(line.decode(self.encodeType).encode('utf-8'))
        scriptFile.close()

    def find_includeFiles(self):
        p = re.compile('([ \t]*)include "(\S*)"')
        for foundIncludeIndex, line in enumerate(self.lines):
            matchResult = p.search(line)
            if matchResult:
                foundInclude = IncludeFile()
                foundInclude.indentStr = matchResult.group(1)
                foundInclude.fileName = path.join(self.fileDir, matchResult.group(2))
                foundInclude.parentFileName = path.join(self.fileDir, self.fileName)
                foundInclude.startPosition = matchResult.start()
                foundInclude.endPosition = matchResult.end()
                foundInclude.foundIndex = foundIncludeIndex
                foundInclude.load_file()
                self.includeFiles.append(foundInclude)

    def convert_line_to_includeFile(self):
        for includeFile in self.includeFiles:
            includeFileStream = ''''''
            for line in includeFile.lines:
                includeFileStream += (includeFile.indentStr + line)
            
            self.lines[includeFile.foundIndex] = self.lines[includeFile.foundIndex][:includeFile.startPosition] + includeFileStream + self.lines[includeFile.foundIndex][includeFile.endPosition:]

        self.includeFiles = []
        self.find_includeFiles()
        if len(self.includeFiles) > 0:
            self.convert_line_to_includeFile()

    def combine_icludes(self, outFileName='Compile_Result.ms'):
        try:
            self.find_includeFiles()
            self.convert_line_to_includeFile()

            resultFileName = outFileName
            resultFullFileName = path.join(self.fileDir, resultFileName)
            self.resultFileFullname = resultFullFileName
            resultFile = codecs.open(self.resultFileFullname, encoding='utf-8', mode='w')
            resultFile.writelines(self.lines[2:])
            resultFile.close()
        except:
            self.returnMessage = 'Failed to Compile'
