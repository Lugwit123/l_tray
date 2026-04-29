import sys,re
import os,json,subprocess
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QMessageBox, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from tool_env import *
sys.path.insert(0,LugwitToolDir+'/Lib')

from Lugwit_Module import lprint

curDir=os.path.dirname(__file__)
diskLinkFile=f"{LugwitToolDir}/data/diskLink.json"
diskLinkList=[]
with open(diskLinkFile,'r',encoding='utf-8') as f:
    diskLinkList=json.load(f)["linkList"]

import main_ui  # 从 main_ui.py 导入 UI 类
from imp import reload
reload(main_ui)

class Ui_Form(QWidget,main_ui.Ui_Form):
    def __init__(self, ):
        super(Ui_Form, self).__init__()
        self.setupUi(self)
        self.setFixedHeight(60)  
        self.setFixedWidth(1240)
        # 设置统一字体
        app_font = QFont("Microsoft YaHei UI", 10)  # 使用微软雅黑UI字体
        self.setFont(app_font)
        
        # 新增：交换按钮和状态标签
        self.swapBtn = QPushButton('⇄')
        self.swapBtn.setFixedWidth(32)
        self.sourceStatus = QLabel()
        self.targetStatus = QLabel()
        self.sourceStatus.setFixedWidth(20)
        self.targetStatus.setFixedWidth(20)
        
        # 新增：单行创建链接按钮
        self.createLinkBtn = QPushButton('创建')
        self.createLinkBtn.setFixedWidth(50)
        self.parent_app = None  # 用于存储父窗口引用
        
        # 设置状态标签字体
        status_font = QFont("Segoe UI Symbol", 12)  # 使用支持Unicode符号的字体
        self.sourceStatus.setFont(status_font)
        self.targetStatus.setFont(status_font)
        
        # 假设布局为水平，插入控件
        self.layout().insertWidget(1, self.swapBtn)
        self.layout().insertWidget(2, self.sourceStatus)
        self.layout().insertWidget(4, self.targetStatus)
        self.layout().insertWidget(6, self.createLinkBtn)  # 在最右侧添加创建按钮
        
        # 绑定事件
        self.swapBtn.clicked.connect(self.swapSourceTarget)
        self.sourceLink.textChanged.connect(self.updateStatus)
        self.targetLink.textChanged.connect(self.updateStatus)
        self.createLinkBtn.clicked.connect(self.onCreateButtonClicked)
        self.updateStatus()

    def set_parent_app(self, app):
        self.parent_app = app

    def onCreateButtonClicked(self):
        if self.parent_app:
            self.createSingleLink(self.parent_app.linkTypeCombo.currentIndex())

    def swapSourceTarget(self):
        src = self.sourceLink.text()
        tgt = self.targetLink.text()
        self.sourceLink.setText(tgt)
        self.targetLink.setText(src)

    def updateStatus(self):
        src = self.sourceLink.text()
        tgt = self.targetLink.text()
        if os.path.exists(src):
            self.sourceStatus.setText('✔')
            self.sourceStatus.setProperty('status', 'success')  # 使用属性选择器
        else:
            self.sourceStatus.setText('✘')
            self.sourceStatus.setProperty('status', 'error')  # 使用属性选择器
        if os.path.exists(tgt):
            self.targetStatus.setText('✔')
            self.targetStatus.setProperty('status', 'success')
        else:
            self.targetStatus.setText('✘')
            self.targetStatus.setProperty('status', 'error')
        # 强制更新样式
        self.sourceStatus.style().unpolish(self.sourceStatus)
        self.sourceStatus.style().polish(self.sourceStatus)
        self.targetStatus.style().unpolish(self.targetStatus)
        self.targetStatus.style().polish(self.targetStatus)

    def createSingleLink(self, link_type):
        sourceLink = self.sourceLink.text()
        targetLink = self.targetLink.text()
        try:
            if os.path.exists(targetLink) or os.path.islink(targetLink):
                QMessageBox.warning(self, "创建失败", f"目标已存在: {targetLink}")
                return
            if link_type == 0:
                os.symlink(sourceLink, targetLink, target_is_directory=True)
            else:
                cmd=f'cmd.exe /c mklink /J "{targetLink}" "{sourceLink}"'
                subprocess.check_call(cmd, shell=True)
            QMessageBox.information(self, "创建成功", f"链接创建成功！\\n源: {sourceLink}\\n目标: {targetLink}")
        except Exception as e:
            QMessageBox.critical(self, "创建失败", f"创建链接失败：{e}")

class ExampleApp(QWidget):
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.topLay=QVBoxLayout()
        self.cell_vLay=QVBoxLayout()
        self.topLay.addLayout(self.cell_vLay)
        self.ExObj_Ui_FormList=[]
        
        # 先加载QSS样式，确保所有子控件都能继承样式
        qss_path = os.path.join(os.path.dirname(__file__), 'qss_style', 'setDiskLink.qss')
        if os.path.exists(qss_path):
            with open(qss_path, 'r', encoding='utf-8') as f:
                qss = f.read()
                self.setStyleSheet(qss)
                QApplication.instance().setStyleSheet(qss)
        
        # 新增：链接类型选择
        self.linkTypeCombo = QComboBox()
        self.linkTypeCombo.addItems(["软链接 (symlink)", "目录联接 (Junction)"])
        self.topLay.addWidget(self.linkTypeCombo)
        
        # 初始化第一个表单
        self.ui_from = Ui_Form()
        self.ui_from.set_parent_app(self)
        self.ui_from.sourceLink.setText(self.parseVar(diskLinkList[0][0]))
        self.ui_from.targetLink.setText(diskLinkList[0][1])
        self.ExObj_Ui_FormList.append(self.ui_from)
        self.cell_vLay.addWidget(self.ui_from)
        
        # 初始化其他表单
        self.initExWinFromJsonFile()
        self.ui_from.addBtn.clicked.connect(self.addExWin)

        self.createLinkWgt=QPushButton('创建链接')
        self.createLinkWgt.clicked.connect(self.createLink)
        self.topLay.addWidget(self.createLinkWgt)

        self.saveBtn = QPushButton('保存设置')
        self.saveBtn.clicked.connect(self.saveSettings)
        self.topLay.addWidget(self.saveBtn)

        self.setLayout(self.topLay)
        self.setMinimumHeight(100 + 60 * len(self.ExObj_Ui_FormList))
        #self.ui_from.exRangeGrbox.setStyleSheet("QGroupBox::title { font-size: 3pt; }")
    
        # 优化QSS样式
        self.setStyleSheet('''
            QPushButton {
                min-height: 28px;
                border-radius: 4px;
                background: #f0f0f0;
                border: 1px solid #bdbdbd;
                padding: 0 12px;
            }
            QPushButton:hover {
                background: #e0eaff;
                border: 1.5px solid #5b9bd5;
            }
            QPushButton:pressed {
                background: #d0d8e8;
            }
            QLineEdit {
                border: 1px solid #bdbdbd;
                border-radius: 3px;
                padding: 2px 6px;
                background: #fcfcfc;
                font-size: 14px;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
            }
            QComboBox {
                border: 1px solid #bdbdbd;
                border-radius: 3px;
                padding: 2px 6px;
                background: #fcfcfc;
                font-size: 14px;
            }
        ''')

    def initExWinFromJsonFile(self):
        lprint(diskLinkList)
        for a,b in diskLinkList[1:]:
            uiForm=self.addExWin()
            uiForm.sourceLink.setText(self.parseVar(a))
            uiForm.targetLink.setText(b)
    def addExWin(self):
        uiForm=Ui_Form()
        uiForm.set_parent_app(self)  # 设置父窗口引用
        uiForm.addBtn.setText('删除')
        self.ExObj_Ui_FormList.append(uiForm)
        uiForm.addBtn.clicked.connect(self.removeUiForm)  # 直接传递方法引用
        self.cell_vLay.addWidget(uiForm)
        self.setMinimumHeight(self.height()+44)
        return uiForm
        
    def removeUiForm(self, uiForm):
        # 从布局中移除部件
        self.cell_vLay.removeWidget(uiForm)
        # 销毁部件
        uiForm.deleteLater()
        # 适当调整窗口高度
        self.setFixedHeight(self.height() - 40)
        self.ExObj_Ui_FormList.remove(uiForm)
    
    def parseVar(self,Var):
        findAll=re.findall(r'\$\w+',Var)
        lprint (findAll)
        for _ in findAll:
            Var=Var.replace(_,os.environ[_[1:]])
        return Var
    def createLink(self):
        link_type = self.linkTypeCombo.currentIndex()  # 0: symlink, 1: junction
        success_count = 0
        fail_msgs = []
        for ui_from in self.ExObj_Ui_FormList:
            sourceLink=ui_from.sourceLink.text()
            targetLink=ui_from.targetLink.text()
            lprint (sourceLink,targetLink)
            try:
                if os.path.exists(targetLink) or os.path.islink(targetLink):
                    fail_msgs.append(f"目标已存在: {targetLink}")
                    continue
                if link_type == 0:
                    os.symlink(sourceLink, targetLink, target_is_directory=True)
                else:
                    # Windows下用mklink /J创建目录联接
                    cmd=f'cmd.exe /c mklink /J "{targetLink}" "{sourceLink}"'
                    subprocess.check_call(cmd, shell=True)
                success_count += 1
            except Exception as e:
                fail_msgs.append(f"{targetLink} 创建失败: {e}")
        msg = f"成功创建 {success_count} 个链接。"
        if fail_msgs:
            msg += "\n失败信息:\n" + "\n".join(fail_msgs)
        QMessageBox.information(self, "创建结果", msg)
        self.setMinimumHeight(100 + 60 * len(self.ExObj_Ui_FormList))

    def saveSettings(self):
        link_list = []
        for ui_from in self.ExObj_Ui_FormList:
            source = ui_from.sourceLink.text()
            target = ui_from.targetLink.text()
            link_list.append([source, target])
        try:
            with open(diskLinkFile, 'w', encoding='utf-8') as f:
                json.dump({"linkList": link_list}, f, ensure_ascii=False, indent=2)
            QMessageBox.information(self, "保存设置", "设置已成功保存！")
        except Exception as e:
            QMessageBox.critical(self, "保存失败", f"保存设置时出错：{e}")

def findAllWidgetsByName(parentWidget, widgetName):
    foundWidgets = []
    # 检查当前部件是否匹配
    if parentWidget.objectName() == widgetName:
        foundWidgets.append(parentWidget)

    # 递归查找所有子部件
    for child in parentWidget.children():
        if isinstance(child, QWidget):  # 确保子部件是 QWidget 或其子类
            foundWidgets.extend(findAllWidgetsByName(child, widgetName))

    return foundWidgets


app = QApplication(sys.argv)
mainWin = ExampleApp()
mainWin.show()
sys.exit(app.exec_())

'''
import sys
import hou
sys.path.append(r'D:\TD_Depot\interview_test\HoudiniExCache' )
print (sys.executable)
import main
from imp import reload
reload (main)
mainwin = main.ExampleApp()
mainwin.show()

'''