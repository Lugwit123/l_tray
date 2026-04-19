import sys
import os
import codecs
import time
os.environ['QT_API'] = 'PySide6'
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import json
from typing import Literal
from functools import partial
sys.path.append(r'D:\TD_Depot\Software\Lugwit_syncPlug\lugwit_insapp\trayapp\src')
from tool_env import *

sys.path.insert(0,LugwitToolDir+'/Lib')

from Lugwit_Module import lprint
from Lugwit_Module.l_src.UILib.QTLib.styleSheet import self_qss
from Lugwit_Module.l_src.UILib.QTLib import l_QWidgets
import customWgt

curDir = os.path.dirname(__file__)

ui_file_path = os.path.join(LugwitToolDir, "data/pyqt_ui_file/setEnvVar.ui")

import os,re,sys,codecs
curDir=os.path.dirname(__file__)

def readToolEnv(jsonFile):
    #_ = ToolEnvJsonFile if os.path.exists(ToolEnvJsonFile) else ToolEnvJsonFile_orgi
    #names=locals()
    with codecs.open(jsonFile,'r','utf-8') as f:
        configJson=f.read()
        ToolEnvDict=eval(configJson)
        # for key,val in ToolEnvDict.items():
        #     names[key]=val
        #     os.environ[key]=val
    return ToolEnvDict



def get_widgets_from_gridlayout(grid_layout):
    widgets = []
    # 获取网格布局的行数和列数
    rows = grid_layout.rowCount()
    cols = grid_layout.columnCount()

    # 遍历每行每列
    for row in range(rows):
        for col in range(cols):
            item = grid_layout.itemAtPosition(row, col)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widgets.append(widget)
    return widgets

class UiLoader(QWidget):
    def __init__(self, ui_file_path, parent=None):
        super(UiLoader, self).__init__(parent)
        self.loader = QUiLoader()  # Ui 文件加载器
        self.ui_file_path = ui_file_path  # UI 文件路径


    def load_ui(self):
        """加载 UI 文件的函数"""
        ui_file = QFile(self.ui_file_path)
        
        if not ui_file.open(QFile.ReadOnly):
            print(f"无法打开文件 {self.ui_file_path}")
            return None
        
        # 从 UI 文件加载 UI
        loaded_ui = self.loader.load(ui_file, self)
        ui_file.close()  # 关闭文件
        
        return loaded_ui  # 返回加载的 UI


class Ui(QWidget):
    def __init__(self,):
        super(Ui,self).__init__()
        self.setMinimumWidth(1000)
        self.setMinimumHeight(800)
        
        self.lay=QVBoxLayout()
        self.lay.setContentsMargins(0,0,0,0)
        self.setLayout(self.lay)

        
        self.Ui_Loader = UiLoader(ui_file_path,self).load_ui()
        self.Ui_Loader.setMouseTracking(True)
        self.lay.addWidget(self.Ui_Loader)
        self.Ui_Loader.EnvVar_gridLay.setSpacing(0)
        self.Ui_Loader.toolEnv_gridLay.setSpacing(0)
        self.EnvVal_UI()
        self.ToolEnvVal_UI()
        self.Ui_Loader.cancle_btn.clicked.connect(self.cancle_btn_func)
        self.Ui_Loader.ensure_btn.clicked.connect(self.ensure_btn_func)
        self.Ui_Loader.restoreDefaultValue_Btn.clicked.connect(self.restoreDefaultValue_Func)
        
        #帮我完成self.addToolVarBtn和self.addToolVarBtn
        self.Ui_Loader.addEnvVarBtn.clicked.connect(
                    lambda:self.addEnvVar(self.Ui_Loader.EnvVar_gridLay))
        self.Ui_Loader.addToolVarBtn.clicked.connect(
                    lambda:self.addEnvVar(self.Ui_Loader.toolEnv_gridLay))

        
    
    def addEnvVar(self, layout):
        index = layout.rowCount()
        key_edit = customWgt.DoubleClickLineEdit('变量名称')  # 创建自定义的可双击编辑的 QLineEdit
        val_edit = QLineEdit('变量值')
        delete_btn = QPushButton('-')
        delete_btn.clicked.connect(partial(self.deleteColumn, index, layout))
        
        layout.addWidget(key_edit, index, 0)
        layout.addWidget(customWgt.customQLabel(':'), index, 1)
        layout.addWidget(val_edit, index, 2)
        layout.addWidget(delete_btn, index, 3)  
        
    def EnvVal_UI(self):
        clearLayout(self.Ui_Loader.EnvVar_gridLay)
        self.createToolEnv_UI(oriEnvVarJsonFile,self.Ui_Loader.EnvVar_gridLay) 

    def ToolEnvVal_UI(self):
        clearLayout(self.Ui_Loader.toolEnv_gridLay)
        jsonFile = ToolEnvJsonFile if os.path.exists(ToolEnvJsonFile) else ToolEnvJsonFile_orgi
        self.createToolEnv_UI(jsonFile,self.Ui_Loader.toolEnv_gridLay)
    def cancle_btn_func(self):
        self.close()
        
    def ensure_btn_func(self):
        # 加入系统环境变量
        EnvValDict=self.getEnvVar_gridLayValue(self.Ui_Loader.EnvVar_gridLay)
        for key,val in EnvValDict.items():
            os.system(f'setx {key} {val}')
        with codecs.open(oriEnvVarJsonFile,'w',encoding='utf8') as f:
            json.dump(EnvValDict,f,ensure_ascii=False,indent=4)
        # 加入工具环境变量
        EnvValDict=self.getEnvVar_gridLayValue(self.Ui_Loader.toolEnv_gridLay)
        EnvValDict['LugwitToolDir']=LugwitToolDir
        with codecs.open(ToolEnvJsonFile,'w',encoding='utf8') as f:
            json.dump(EnvValDict,f,ensure_ascii=False,indent=4)
            
    def restoreDefaultValue_Func(self):
        self.createToolEnv_UI(ToolEnvJsonFile_orgi)
        
    def createToolEnv_UI(self,jsonFile,layout):
        clearLayout(layout)
        ToolEnvDict=readToolEnv(jsonFile)
        EnvValDict=self.getEnvVar_gridLayValue(self.Ui_Loader.EnvVar_gridLay)
        
        
        layout:QGridLayout
        layout.setSpacing(5)

        print  ('layout.parent()',layout.parent())
        layout.setContentsMargins(10, 10, 10, 10)

        #layout.setParent(self.Ui_Loader.scrollAreaWidgetContents)
        for index,(key,ori_val) in enumerate(ToolEnvDict.items()):
            #val = $TD_DepotDir\Software\ProgramFiles\NukePlug
            real_val=ori_val
            findAll=re.findall(r'\$\w+',ori_val)
            for _ in findAll:
                real_val=real_val.replace(_,EnvValDict[_[1:]])

            DoubleClickLineEdit=customWgt.DoubleClickLineEdit(key)# 第一个按钮
            layout.addWidget(DoubleClickLineEdit,index,0)

            label=customWgt.customQLabel(':') # "这就是个冒号"
            layout.addWidget(label,index,1)

            val_wgt=QLineEdit(ori_val)
            val_wgt.setFixedWidth(800)
            val_wgt.setToolTip(real_val)
            layout.addWidget(val_wgt,index,2)
            
            DoubleClickLineEdit.setFixedWidth(200)


            deleteColumnBtn=QPushButton('-')
            deleteColumnBtn.setFixedHeight(20)
            layout.addWidget(deleteColumnBtn,index,3)
            deleteColumnBtn.clicked.connect(
                partial(self.deleteColumn,index,layout))

        self.Ui_Loader.scrollAreaWidgetContents.setLayout(layout)
    
    def deleteColumn(self,index,layout):
        for column in range(layout.columnCount()):
            # 获取位于(row, column)位置的项
            item = layout.itemAtPosition(index, column)
            if item is not None:
                # 移除项并获取对应的控件
                widget = item.widget()
                if widget is not None:
                    # 从布局中移除控件
                    layout.removeWidget(widget)
                    # 删除控件
                    widget.deleteLater()
        self.adjustSize()
         
    def getEnvVar_gridLayValue(self,
        grid_layout=Literal['self.EnvVar_gridLay','self.toolEnv_gridLay']):
        widgets = get_widgets_from_gridlayout(grid_layout)
        EnvValDict={}
        for i in range(0,int(len(widgets)/4)):
            EnvValDict[widgets[i*4].text()]=widgets[i*4+2].text()
        return EnvValDict
    
    def getWidgetsInGridLay(self,grid_layout):
        rowCount = grid_layout.rowCount()
        columnCount = grid_layout.columnCount()
        widgetList=[]
        for row in range(rowCount):
            for column in range(columnCount):
                layoutItem = grid_layout.itemAtPosition(row, column)
                if layoutItem is not None:
                    widget = layoutItem.widget()
                    if widget is not None:
                        widgetList.append(widget)
        return widgetList
                        
    def getUsrEnvVarValue(self):
        widgetList:[QLabel,QLineEdit]=self.getWidgetsInGridLay(self.Ui_Loader.EnvVar_gridLay)
        for i in range(0,int(len(widgetList)/4)):
            setattr(self,widgetList[i*4].text(),widgetList[i*4+2].text())
            lineedit:QLineEdit=widgetList[i*4]
            lineedit.textChanged.connect(self.ToolEnvVal_UI)

        
def clearLayout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            
def main():
    global loader
    loader = QUiLoader()  
    app = QApplication(sys.argv)
    aa='*{font-family:Microsoft YaHei UI;font-size:12pt;}'
    app.setStyleSheet(aa+self_qss)
    window = Ui()
    window.show()
    window.setWindowTitle("设置工具环境变量")
    window.setMinimumHeight(800)
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()
