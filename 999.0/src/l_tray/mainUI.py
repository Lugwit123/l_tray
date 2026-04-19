import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from Lugwit_Module import *
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QApplication

LugwitPath=os.environ.get('LugwitPath')
lugwit_PluginPath=os.environ.get('lugwit_PluginPath')
Lugwit_publicPath=os.environ.get('Lugwit_publicPath')

class Ui_MainWindow(QWidget):

    def __init__(self,logFile=f'{Lugwit_publicPath}\\\Lugwit_syncPlug\\syncLog.txt'):
        self.logFile=logFile
        super(Ui_MainWindow, self).__init__()
        
    def setupUi(self, MainWindow=''):
        lprint (MainWindow)
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.QVBoxLayout=QVBoxLayout()
        self.centralwidget.setLayout(self.QVBoxLayout)
        
        self.textBrowser = QtWidgets.QTextEdit()
        
        self.getlogContent()
        
        self.QVBoxLayout.addWidget(self.textBrowser)
        self.pushButton = QtWidgets.QPushButton()
        self.pushButton.clicked.connect(self.getlogContent)
        
        self.QVBoxLayout.addWidget(self.pushButton)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "更新日志"))
        self.pushButton.setText(_translate("MainWindow", "刷新"))
        
    def getlogContent(self):
        if not os.path.exists(self.logFile):
            return
        with open(self.logFile,'r') as f:
            f_read=f.read()
        self.textBrowser.setText(f_read)
        




if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QMainWindow()
    MainWindow=Ui_MainWindow()
    MainWindow.setupUi(win)
    win.show()
    sys.exit(app.exec_())
