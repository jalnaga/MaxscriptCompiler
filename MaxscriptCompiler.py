# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os

from PySide import QtGui, QtCore

from combineInclude import MaxScript


PATH_PROGRAM = os.path.dirname(__file__)


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.compiler = MaxScript()
        self.compileOutName = 'Compile_Result.ms'
        self.compileOutFullName = 'Compile_Result.ms'
        self.jalToolPath = 'D:\\JalTool'

        self.ui = QtGui.QWidget()

        self.init_ui()
    
    def init_ui_toolLocation(self):
        self.toolLocHBox = QtGui.QHBoxLayout()
        self.setToolLocBtn = QtGui.QPushButton('Set JalTool:')
        self.toolLocLdt = QtGui.QLineEdit(self.jalToolPath, self)
        self.toolLocLdt.setReadOnly(True)

        self.toolLocHBox.addWidget(self.setToolLocBtn)
        self.toolLocHBox.addWidget(self.toolLocLdt)
        self.toolLocHBox.addStretch(1)

        self.setToolLocBtn.clicked.connect(self.setToolLocBtn_pressed)

    def init_ui_loadScript(self):
        self.loadScriptVBox = QtGui.QVBoxLayout()
        self.loadScriptBtnHBox = QtGui.QHBoxLayout()
        self.filenameLdt = QtGui.QLineEdit('', self)
        self.loadBtn = QtGui.QPushButton('Load Script File')
        self.convertBtn = QtGui.QPushButton('Compile')

        self.loadScriptVBox.addStretch(1)
        self.loadScriptVBox.addWidget(self.filenameLdt)
        self.loadScriptVBox.addLayout(self.loadScriptBtnHBox)
        self.loadScriptBtnHBox.addWidget(self.loadBtn)
        self.loadScriptBtnHBox.addWidget(self.convertBtn)
        
        self.loadBtn.clicked.connect(self.loadBtn_pressed)
        self.convertBtn.clicked.connect(self.convertBtn_pressed)

    def init_ui(self):
        self.init_ui_toolLocation()
        self.init_ui_loadScript()

        self.setWindowTitle('Maxscript Compiler')

        self.mainVBox = QtGui.QVBoxLayout()
        self.mainVBox.addLayout(self.toolLocHBox)
        self.mainVBox.addLayout(self.loadScriptVBox)

        self.ui.setLayout(self.mainVBox)
        self.setCentralWidget(self.ui)

        self.resize(400, 200)

    def setToolLocBtn_pressed(self):
        folderLoadDlg = QtGui.QFileDialog()
        jalToolFolderName = folderLoadDlg.getExistingDirectory()
        if jalToolFolderName != '':
            self.toolLocLdt.setText(jalToolFolderName)
            self.jalToolPath = jalToolFolderName
    
    def loadBtn_pressed(self):
        fileLoadDlg = QtGui.QFileDialog()
        maxscriptFileName = fileLoadDlg.getOpenFileName(
            self, 'Open Maxscript to Compile', PATH_PROGRAM, 'Max Script file (*.ms)')[0]
        if maxscriptFileName != '':
            self.filenameLdt.setText(maxscriptFileName)
            
            folder_structure = os.path.dirname(maxscriptFileName).split('/')
            if folder_structure[-1] == 'src':
                self.compileOutName = folder_structure[-2] + '.ms'
            else:
                self.compileOutName = folder_structure[-1] + '.ms'

    def convertBtn_pressed(self):
        for toolFolder in os.walk(self.jalToolPath):
            if self.compileOutName.split('.')[0] == toolFolder[0].split('\\')[-1]:
                self.compileOutFullName = os.path.join(toolFolder[0], self.compileOutName)

        self.compiler.load_file(self.filenameLdt.text())
        self.compiler.combine_icludes(outFileName=self.compileOutFullName)

        QtGui.QMessageBox.information(self, "Result", self.compiler.returnMessage)

        self.compiler.reset_process()

def main():
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
