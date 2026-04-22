# coding:utf-8
import os,sys,subprocess
import socket
import os,sys,json,traceback,re,subprocess
from typing import List   ,Tuple 
import ins 
# 从 _config.py 统一读取 Perforce 开关，避免循环导入
from _config import ENABLE_PERFORCE
import  winshell 
import console
import copy
import webbrowser
import ctypes
import os
import psutil
import win32gui
import win32con
    

import codecs,time,glob,importlib
curDir=os.path.dirname(__file__)

menu_dir=os.path.dirname(curDir)+'/tray_menu'
LugwitToolDir=os.environ["LugwitToolDir"]
sys.path.append(LugwitToolDir+'/Lib') 
sys.path.append(menu_dir) 

logPath=f'{os.environ["Temp"]}/plugSync_output.log'

import  Lugwit_Module as LM
lprint=LM.lprint
from Lugwit_Module.l_src import insLocation
from Lugwit_Module.l_src import l_subprocess
from Lugwit_Module.l_src.UILib import toggle_ui_visable
if ENABLE_PERFORCE:
    from lperforce import loginP4,p4_baselib
    from lperforce.dataType import login_info as login_info_dataType
from importlib  import reload
from L_Maya import start_maya
from L_Tools.sys_tool import l_admin

import os as _os
iconDir = (LugwitToolDir + '/icons').replace('\\', '/')
_wuwo_icons_dir = _os.environ.get('WUWO_ICONS_DIR', '').replace('\\', '/')
if _wuwo_icons_dir and _os.path.isdir(_wuwo_icons_dir):
    iconDir = _wuwo_icons_dir


oriEnvVarFile=os.getenv('oriEnvVarFile')
lprint(oriEnvVarFile)
with codecs.open(oriEnvVarFile,'r',encoding='utf-8') as f:
    oriEnvVar=json.load(f)

insLocationDict=insLocation.getInsLocationDict()
insLocation.getMayaInsLocationDict()
import winreg
from functools import partial
from multiprocessing import Process 
sys.path.append(os.getenv('LugwitToolDir'))
from tray_menu import  trayMenuFunc
PIPE_NAME = r'\\.\pipe\ChatRoomPipe'



StartUpDir=r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup'

lugwit_ConsolePlugSyncexeFile=fr"{LugwitToolDir}\lugwit_insapp.exe True"
Lugwit_P4CLIENTDIR=r'D:\TD_Depot'



from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

def getDocPath():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Personal")[0]



st=time.time()
if os.path.exists(r"D:\TD_Depot\Software\Lugwit_syncPlug\lugwit_insapp\trayapp\python311.dll"):
    ConEmuCmd=r'D:\TD_Depot\Software\ProgramFilesLocal\ConEmuPack.230724\ConEmu.exe'
    shortcut_path = os.path.join(winshell.programs(), '0lugwit_insapp.lnk')
    ins.createShortCut(
        exe_path =  f"{ConEmuCmd}",
        shortcut_path=shortcut_path,
        name = '0lugwit_insapp',
        icon_path = (iconDir+r'\NiuMatIco.ico',0),
        arguments=fr"/cmd {LugwitToolDir}\lugwit_insapp.exe"
        )
else:
    ConEmuCmd=f"{LugwitToolDir}\lugwit_insapp.exe"
    shortcut_path = os.path.join(winshell.programs(), '0lugwit_insapp.lnk')
    ins.createShortCut(
        exe_path =  f"{ConEmuCmd}",
        shortcut_path=shortcut_path,
        name = '0lugwit_insapp',
        icon_path = (iconDir+r'\NiuMatIco.ico',0),
        )
print("创建方式花费时间",time.time()-st)


# ins.createShortCut(
#     exe_path = LM.Lugwit_publicPath+ r'\Python\PyFile\syncPlugLib\update.bat.lnk',
#     shortcut_path = os.path.join(winshell.programs(), '0lugwit_update.lnk'),
#     name = '0lugwit_update',)

# desktop_path = desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
# ins.createShortCut(
#     exe_path = LM.ProgramFilesLocal+ '\\cgteamwork\\bin\\cgtw\\CgTeamWork.exe',
#     shortcut_path = os.path.join(winshell.programs(), '0cgtw.lnk'),
#     name = '0cgtw',)
# ins.createShortCut(
#     exe_path = LM.ProgramFilesLocal+ '\\cgteamwork\\bin\\cgtw\\CgTeamWork.exe',
#     shortcut_path = os.path.join(desktop_path, 'cgtw.lnk'),
#     name = 'cgtw',)
# sys.exit()

ins.setBoot()
# A:\TD\安装步骤\一键自动安装插件.bat


class HoverButton(QSystemTrayIcon):
    press = pyqtSignal()
    enter = pyqtSignal()
    # def __init__(self):
    #     HoverButton.__init__(self,)
        # self.setMouseTracking(True)
    def mouseMoveEvent(self, evt):
        super().mouseMoveEvent(evt)
        with open ('D:/menu_font.txt','w') as f:
            f.write(str(time.ctime(time.time())))
        os.startfile(LM.Lugwit_publicPath+r'\Lugwit_syncPlug\tray\update.bat')

menu_font=QFont()   
# menu_font.setFamily("Consolas")  # 设置字体为等宽的 Consolas
menu_font.setPointSize(13)
# menu_font.setBold(True)  # 设置为粗体

def get_all_local_ips():
    ip_info = {}
    for interface, addrs in psutil.net_if_addrs().items():
        ip_list = []
        for addr in addrs:
            if addr.family == socket.AF_INET:  # 检查是否为 IPv4 地址
                ip_list.append(addr.address)
        if ip_list:
            ip_info[interface] = ip_list
    return ip_info


from Lugwit_Module.l_src import  insLocation


# 获取P4登录信息
class FindLoginInfoThread(QThread):
    # 定义一个信号，当任务完成时发送信号
    task_finished = pyqtSignal(list)

    def run(self):
        if not ENABLE_PERFORCE:
            return
        # 模拟一个耗时任务
        result_project = p4_baselib.getP4LoginInfo(infoSource='project')
        lprint (f"登录项目成功{result_project}")
        result_plug = p4_baselib.getP4LoginInfo(infoSource='plug')
        lprint (f"登录插件成功{result_plug}")
        result = [result_project,result_plug]
        # 发送任务完成信号
        self.task_finished.emit(result)
        

class ProgramButton(QPushButton):
    def __init__(self, exec_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exec_path = exec_path

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        open_location_action = QAction('打开程序位置', self)
        open_location_action.triggered.connect(self.open_program_location)
        menu.addAction(open_location_action)
        menu.exec_(event.globalPos())
        event.accept()  # 阻止事件继续传播到父级

    def open_program_location(self):
        # 使用 Windows Explorer 打开程序所在目录并选中程序
        explorer_path = f'/select,"{self.exec_path}"'
        subprocess.Popen(['explorer', explorer_path])
    
class TrayIcon(QSystemTrayIcon):
    def __init__(self,MainWindow=None,parent=None):
        super(TrayIcon, self).__init__(parent)
        self.setToolTip("这是托盘图标的提示信息")
        self.installEventFilter(self)
        self.isTD=False
        self.ui = MainWindow

        if self.isStudentHost():
            self.projectPort='192.168.110.61:1999'
        else:
            self.projectPort='192.168.110.26:1666'
        
        self.createMenu()
        # 延后自动启动，避免在构造阶段阻塞托盘图标显示。
        QTimer.singleShot(1200, self.start_scheduler_on_boot)
        
        self.menu.aboutToShow.connect(self.bring_menu_to_front)
        self.activated.connect(self.on_tray_icon_activated)
        
        self.set_CGT_env()
        # self.blink_timer = QTimer(self)
        # self.blink_timer.timeout.connect(self.toggle_overlay)

        # self.overlay_visible = False
        
        # websocet_m.main(self.start_blinking)
        # self.activated.connect(self.on_tray_icon_activated)
        # self.messageClicked.connect(self.on_message_clicked)
    
    def on_message_clicked(self,):
        # 在这里执行某些命令，例如打开记事本
        lprint("data",popui=True)
        self.stop_blinking()

    def bring_menu_to_front(self):
        self.menu.setWindowFlags(self.menu.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.menu.show()
        

    def createMenu(self):
        self.menu = QMenu()
        try:
            exeFile=insLocationDict.get('Maya').get('2018').get('path')+r'\bin\maya.exe'
            self.Maya2018Action = QAction("Maya2018", self, triggered=lambda: self.startProcess(exeFile,""))
            self.Maya2018Action.setIcon(QIcon(iconDir+r'\maya_oldICon.jpg'))
            self.menu.addAction(self.Maya2018Action)
            self.menu.addSeparator()
        except:
            pass

        self.toggleMayaLagMenu = self.menu.addMenu(QIcon(iconDir+r'\maya_oldICon.jpg'),'切换Maya语言')
        self.toggleMayaLagMenu.addAction(QAction("中文", self, \
                    triggered=partial(self.switchMayaLanguage,'zh_CN')))
        self.toggleMayaLagMenu.addAction(QAction("英文", self, \
                    triggered=partial(self.switchMayaLanguage,'en_US')))
        self.ArnoldVersionMenu()
        
        
        # 使用glob.glob()查找匹配的文件
        menu_dir_list = glob.glob(menu_dir+"/*_*Menu.py")
        LM.lprint (menu_dir+"/*_*Menu.py",menu_dir_list)
        for menu_pyFile in menu_dir_list:
            moduleName = os.path.basename(menu_pyFile)[:-3]
            module = importlib.import_module(f"{moduleName}")
            menuFunc = getattr(module, 'menuFunc')
            menuFunc(self, self.menu)
        
        

        
        # 强制注销进程 wmic process where name='maya.exe' delete
        self.TDToolMenu:QMenu = self.menu.addMenu(QIcon(iconDir+r'\insTraycon.jpg'),'TD工具')
        self.TDToolMenu.addAction(QAction(QIcon(iconDir+r'\designer.ico'),\
                "启动PySide6_QTDesigner", \
                self, triggered=\
                partial(l_subprocess.startProcess,\
                LM.Lugwit_PluginPath+r'\Python\Python39\Lib\site-packages\PySide6\designer.exe')))# type: ignore
        
        self.TDToolMenu.addAction(QAction(QIcon(iconDir+r'\designer.ico'),
                "启动PySide2_QTDesigner", self, 
                triggered=
                partial(self.startProcess,
                    r'D:\TD_Depot\plug_in\Python\Python37\Lib\site-packages\PySide2\designer.exe',"")))# type: ignore
        
        self.TDToolMenu.addAction(QAction(QIcon(iconDir+r'\designer.ico'),
                "启动PyQt5_QTDesigner", self, 
                triggered=
                partial(self.startProcess,
                    r'"C:\Program Files (x86)\Qt Designer\designer.exe"',"")))# type: ignore
        
        self.TDToolMenu.addAction(QAction(QIcon(iconDir+r'\designer.ico'),
                "修改hosts", self, 
                triggered=lambda:subprocess.Popen(r'notepad "C:\Windows\System32\drivers\etc\hosts"')))# type: ignore
        
        startConsoleProcess=\
            lambda : subprocess.Popen(f'{lugwit_ConsolePlugSyncexeFile}') 
        
        self.TDToolMenu.addAction(
            QAction(QIcon('/updateAndRestart.jpg'),
            "启动带控制台版本程序", self, 
            triggered=startConsoleProcess))# type: ignore
        
        self.TDToolMenu.addAction( 
            QAction(QIcon('/updateAndRestart.jpg'),
                    "启动代码跟踪窗口", self, 
                    triggered=partial(l_subprocess.startPyFile,
                        fr'{LugwitToolDir}\Lib\appLib\track\trackUI.py',
                        specify_sys_executable='currentPythonJieShiQi', usePythonw=True)))# type: ignore
        self.TDToolMenu.addAction( 
            QAction(QIcon('/updateAndRestart.jpg'),
                    "启动命令GUI工具", self, 
                    triggered=partial(subprocess.Popen, [sys.executable, r'd:\TD_Depot\Software\cmd_tool_gui\run_modern_cmd_tool.py'],cwd=r'd:\TD_Depot\Software\cmd_tool_gui')))
                    # partial(l_subprocess.startPyFile,
                    #     r'd:\TD_Depot\Software\cmd_tool_gui\run_modern_cmd_tool.py',
                    #     specify_sys_executable='currentPythonJieShiQi', usePythonw=False)))# type: ignore

        
        self.insPlugMenu = self.menu.addMenu(QIcon(iconDir+r'\EnvVar.png'),'系统工具')
        self.insPlugMenu.addAction(QAction(QIcon(iconDir+r'\EnvVar.png'),
                        "修改环境变量", self, triggered=partial(
                            self.runSysCmd,"rundll32 sysdm.cpl,EditEnvironmentVariables",False,True)))# type: ignore
        self.insPlugMenu.addAction(QAction(QIcon(iconDir+r'\EnvVar.png'),
                        "系统配置", self, triggered=partial(self.runSysCmd,"cmd /c msconfig")))# type: ignore
        
        self.insPlugMenu.addAction(QAction(QIcon(iconDir+r'\EnvVar.png'),
                        "控制面板", self, triggered=partial(self.runSysCmd,"cmd /c control")))# type: ignore
        
        self.insPlugMenu.addAction(QAction(QIcon(iconDir+r'\EnvVar.png'),
                        "远程控制", self, triggered=partial(self.runSysCmd,"cmd /c mstsc")))# type: ignore
        
        self.insPlugMenu.addAction(QAction(QIcon(iconDir+r'\EnvVar.png'),
                        "任务计划程序", self, triggered=partial(self.runSysCmd,"cmd /c taskschd.msc")))# type: ignore

        pyFile=LM.LugwitLibDir+'/Lugwit_Module/l_src/l_subprocess/showMessage_tk.py'
        self.insPlugMenu.addAction(QAction(QIcon(iconDir+r'\EnvVar.png'),
                        "启动lprint_popui日志查看器", self, triggered=
                                                            partial(l_subprocess.startPyFile ,
                                                            pyFile,
                                                            'main',
                                                            specify_sys_executable='currentPythonJieShiQi',
                                                            usePythonw=False)))# type: ignore
        pyFile=LM.LugwitAppDir+r'\trayapp\src\l_log\showLog.py'
        self.insPlugMenu.addAction(QAction(QIcon(iconDir+r'\EnvVar.png'),
                        "Maya日志查看器", self, triggered=
                                                partial(l_subprocess.startPyFile ,
                                                pyFile,
                                                'main',
                                                specify_sys_executable='currentPythonJieShiQi',
                                                usePythonw=False)))# type: ignore
        self.insPlugMenu.addAction(
            QAction(
                QIcon(iconDir+r'\EnvVar.png'),
                "PKL查看器",
                self,
                triggered=self.start_view_pkl_tool,
            )
        )# type: ignore

        pyFile=LM.LugwitLibDir+r'/L_Tools/sys_tool/setEnvVar.py'
        self.insPlugMenu.addAction(QAction(QIcon(iconDir+r'\EnvVar.png'),
            "设置工具环境变量", self, triggered=partial(l_subprocess.startPyFile,
                                                pyFile,
                                                'main',
                                                specify_sys_executable='currentPythonJieShiQi', 
                                                usePythonw=True)))# type: ignore
        pyFile=curDir+r'\tools\setDiskLink\setDiskLink.py'
        self.insPlugMenu.addAction(QAction(QIcon(iconDir+r'\EnvVar.png'),
            "设置磁盘链接", self, triggered=partial(l_subprocess.startPyFile,
                                            pyFile,
                                            'main',
                                            specify_sys_executable='currentPythonJieShiQi', 
                                            usePythonw=True)))# type: ignore

        # rundll32 sysdm.cpl,EditEnvironmentVariables
        startUPDir=r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp'
        self.insPlugMenu.addAction(QAction("打开StartUp目录", self, 
                                                    triggered=lambda:os.startfile(startUPDir),
                                                    ))# type: ignore
        
        # rundll32 sysdm.cpl,EditEnvironmentVariables
        self.insPlugMenu.addAction(QAction("打开SendTo目录", self, 
                                                    triggered=lambda:os.startfile("shell:sendto"),
                                                    ))# type: ignore

        self.insPlugMenu.addAction(QAction("更新解释器", self, 
                                                    triggered=lambda:os.startfile("shell:sendto"),
                                                    ))# type: ignore

        # self.insPlugMenu.addAction(QAction("同步Lugwit_Module模块", self, triggered=self.sync_Lugwit_Module))
        unrealEngineInsDict=insLocationDict.get('Unreal Engine')
        if unrealEngineInsDict:
            self.UEMenu = self.menu.addMenu(QIcon(iconDir+r'\UE.ico'),'启动UE')
            for key,val in unrealEngineInsDict.items():
                EditorFile=val['exeFile']
                lprint (os.path.exists(EditorFile),EditorFile)
                action=QAction(QIcon(iconDir+r'\UE.ico'),
                        f"启动{key}", self, triggered=partial(self.startProcess,f'"{EditorFile}"',"",),toolTip=EditorFile)
                action.setStatusTip(EditorFile)
                self.UEMenu.addAction(action)
                
        NukeInsLocation=insLocation.getNukeInsLocation()
        if NukeInsLocation:
            self.NukeMenu = self.menu.addMenu(QIcon(iconDir+r'\nuke.png'),'启动Nuke')
            # 设置Nuke环境变量
            nuke_env = {
                "NUKE_PATH": r"D:\TD_Depot\Software\dccData\NukePlug;C:\ProgramData\Thinkbox\Deadline10/submitters/Nuke"
            }
            for key,val in NukeInsLocation.items():
                EditorFile=val['exeFile']
                self.NukeMenu.addAction(QAction(QIcon(iconDir+r'\nuke.png'),
                        f"启动{key}", self, triggered=partial(self.startProcess,
                                                            ExeFile = f'"{EditorFile}"',
                                                            startParm = '--nukex',
                                                            env = nuke_env)))
        

        MayaInsLocation=insLocation.getMayaInsLocationDict()
        if MayaInsLocation:
            self.MayaMenu = self.menu.addMenu(QIcon(iconDir+r'\maya_oldICon.jpg'),'启动maya')
            pyFile=f'{LugwitToolDir}\\MayaLib\\MayaStarter.py'
            path_env=os.environ.get("PATH")
            append_env={"PATH":fr"{path_env};D:\TD_Depot\plug_in\Lugwit_plug\mayaPlug\plug-ins"}
            self.MayaMenu.addAction(
                    QAction(QIcon(iconDir+r'\maya_oldICon.jpg'),
                    f"Maya启动器_打开控制台", 
                    self, 
                triggered=partial(l_subprocess.startPyFile,
                                  pyFile,
                                  'main',
                                  specify_sys_executable='currentPythonJieShiQi', 
                                  usePythonw=False,
                                  apppend_env=append_env)))
            
            self.MayaMenu.addAction(
                    QAction(QIcon(iconDir+r'\maya_oldICon.jpg'),
                    f"Maya启动器_没有控制台", 
                    self, 
                triggered=partial(l_subprocess.startPyFile,
                                  pyFile,
                                  'main',
                                  specify_sys_executable='currentPythonJieShiQi', 
                                  usePythonw=True,
                                  apppend_env=append_env)))

                
            import locale
            codepage_encoding = locale.getpreferredencoding()
            LM.lprint("代码页编码信息 Codepage encoding:", codepage_encoding)
            
            self.MayaMenu.addSeparator()
            for key,val in MayaInsLocation.items():
                exeFile=val['exeFile']
                self.MayaMenu.addAction( # type: ignore
                    QAction(QIcon(iconDir+r'\maya_oldICon.jpg'),
                    f"启动{key}", 
                    self, 
                    triggered=partial(self.startMaya,exeFile)))# type: ignore
        if self.check_td_user():
            if MayaInsLocation:
                for key,val in MayaInsLocation.items():
                    exeFile=val['exeFile']
                    self.MayaMenu.addAction(
                        QAction(QIcon(iconDir+r'\maya_oldICon.jpg'),
                        f"启动{key}_开发版", 
                        self, 
                        triggered=partial(self.startMaya,exeFile,True )))  # type: ignore

        # Houdini启动菜单
        HoudiniInsLocation=insLocation.getHoudiniInsLocationDict()
        if HoudiniInsLocation:
            self.HoudiniMenu = self.menu.addMenu(QIcon(iconDir+r'\Houdini.png'),'启动Houdini')
            for key,val in HoudiniInsLocation.items():
                exeFile=val['exeFile']
                self.HoudiniMenu.addAction(
                    QAction(QIcon(iconDir+r'\Houdini.png'),
                    f"启动{key}", 
                    self, 
                    triggered=partial(self.startProcess,f'"{exeFile}"',"")))

        
        self.lnkMenu = self.menu.addMenu(QIcon(iconDir+r'\shortcut.png'),'快捷方式')
        lnkDir=Lugwit_P4CLIENTDIR+'/Software/lnk'
        self.lnkMenu.aboutToShow.connect(partial(self.onMenuShow,lnkDir))
        
        
        self.menu.addSeparator()
        
        if ENABLE_PERFORCE:
            env = {'PATH':';'.join([
                                LM.perforceInsDir,
                                oriEnvVar.get('PATH',""),
                                LM.LugwitAppDir+'\\python_env'])}
            p4v_exe=LM.perforceInsDir+'\\p4v.exe'
            p4Admin = LM.perforceInsDir+'\\p4Admin.exe'
            p4_env_var=copy.deepcopy(env)
            p4_env_var['PATH']+=';'+LM.LugwitAppDir+'\\python_env'
            self.P4VAction = QAction(QIcon(iconDir+r'\p4v.png'),
                "启动P4V-插件", self, 
                triggered=partial(ins.startP4V_Plug))
            self.menu.addAction(self.P4VAction)

            pyFile =  LM.LugwitToolDir+r'\src\ins.py'
            self.P4VAction_project = QAction(QIcon(iconDir+r'\p4v.png'),
                "启动P4V-项目", self, 
                triggered=partial(ins.startP4V_H_Project))
            
            self.menu.addAction(self.P4VAction_project)
            
            self.P4AdminAction = QAction(QIcon(iconDir+r'\p4Admin.png'),
                        "启动P4Admin", self, 
                        # triggered=lambda:os.startfile(fr"{LM.perforceInsDir}\p4Admin.exe"))
                        triggered=partial(l_subprocess.startProcess,p4Admin,p4_env_var))
            self.menu.addAction(self.P4AdminAction)

            pyFile = LM.LugwitLibDir+r'\LPERFORCE\modifyClient\main.py'
            self.move_client_Action = QAction(QIcon(iconDir+r'\迁移工作区.webp'),
                        "账号注册,建立工作区", self, 
                        # triggered=lambda:os.startfile(fr"{LM.perforceInsDir}\p4Admin.exe"))
                        triggered=partial(l_subprocess.startPyFile,
                                        pyFile,
                                        'main',
                                        specify_sys_executable='currentPythonJieShiQi', 
                                        usePythonw=False))
            self.menu.addAction(self.move_client_Action)
        

        
        self.DocAction = QAction(QIcon(iconDir+r'\doc.jfif'),
                        "公司插件文档资料", self, triggered=self.openDocAction)
        self.menu.addAction(self.DocAction)
        self.menu.addSeparator()
        self.menu.addAction(self.smallCmdMenuItemsA(iconDir+r'\persion_info.png'))
        self.menu.addAction(self.smallCmdMenuItemsB(iconDir+r'\persion_info.png'))
        
        self.menu.addSeparator()

        self.taskManageAction = QAction(QIcon(iconDir+r'\task.jpg'),
                "任务管理器",   self,  triggered=self.runFunc(trayMenuFunc.taskManage)) # type: ignore
        self.menu.addAction(self.taskManageAction)

        self.startSchedulerAction = QAction(
            QIcon(iconDir+r'\task.jpg'),
            "启动定时任务调度器",
            self,
            triggered=self.start_l_scheduler,
        )
        self.menu.addAction(self.startSchedulerAction)
        
        
        self.toggleConsoleVisAction = QAction(QIcon(iconDir+r'\inform.png'),
                "显示隐藏控制台", self,
                triggered=tray_toggle_win_vis_by_hwnd) # type: ignore
        
        self.menu.addAction(self.toggleConsoleVisAction)
        if LM.hostName in ['PC-20240202CTEU','TD']:
            self.syncPlugMannualAction = QAction(QIcon(iconDir+r'\restart.png'),
                                    "同步托盘工具代码到A盘", self,triggered=self.trayToolCodeToADisk) # type: ignore
            self.menu.addAction(self.syncPlugMannualAction)
        
        self.menu.addSeparator()
        self.menu.addAction(self.loginMenuItems())
        self.menu.addAction(self.userInfoMenuItems(iconDir+r'\persion_info.png'))
        self.menu.addSeparator()
        
        self.menu.addAction(self.p4Tools())
        
        self.insP4AndDownloadDataAction = QAction(QIcon(iconDir+r'\tool.png'),
                    "设置p4v并下载数据", 
                    self,triggered=partial(os.system,
                fr'cmd/K {LM.Lugwit_publicPath}\安装步骤\设置p4v并下载数据.bat')) # type: ignore
                
        self.menu.addAction(self.insP4AndDownloadDataAction)

        
        
        pyFile = LM.LugwitPath+r'\ProjectManageSoftware\main_ui.py'
        self.startProjectManageSoftware_Action = \
                    QAction(QIcon(iconDir+r'\updateAndRestart.jpg'),
                            "打开项目管理软件", self,triggered=partial(l_subprocess.startPyFile,
                                  pyFile,
                                  'main',
                                  usePythonw=True))  # type: ignore
        self.menu.addAction(self.startProjectManageSoftware_Action)
                            
        self.updateAction = QAction(QIcon(iconDir+r'\updateAndRestart.jpg'),
                                            "更新并重启插件", self,triggered=self.updateAndRestart)
        self.menu.addAction(self.updateAction)
 
        self.restartAction = QAction(QIcon(iconDir+r'\updateAndRestart.jpg'),
                                            "重启", self,triggered=self.restart)
        self.menu.addAction(self.restartAction)
        self.quitAction = QAction(QIcon(iconDir+r'\exit.png'),
                                            "退出", self, triggered=self.quit)
        self.menu.addAction(self.quitAction)

        # 创建工作线程
        # if LM.hostName!='DESKTOP-LDSM1H1':
        #     self.thread = FindLoginInfoThread()
        #     # 连接工作线程的任务完成信号到更新UI的槽函数
        #     self.thread.task_finished.connect(self.writeLoginInfo)
        #     self.thread.start()
        #     self.menu.addAction(self.versionInfo())

        #设置图标\
        self.new_message_icon_path=f"{iconDir}/mail-message-new.png"
        self.tray_icon_path=f"{iconDir}/NiuMatIco.png"
        print(self.tray_icon_path,os.path.exists(self.tray_icon_path))
        self.setIcon(QIcon(self.tray_icon_path))
        self.icon = self.MessageIcon()
 
        #把鼠标点击图标的信号和槽连接
        self.activated.connect(self.onIconClicked)
        
        for x in self.menu.actions():
            x.setFont(menu_font)
            
        self.setContextMenu(self.menu)

    def is_l_scheduler_running(self) -> bool:
        instance_tag = "l_tray_scheduler"
        for process in psutil.process_iter(["name", "cmdline"]):
            try:
                cmdline = process.info.get("cmdline") or []
                cmdline_text = " ".join(cmdline).lower()
                if "--instance-tag" in cmdline_text and instance_tag in cmdline_text:
                    return True
                # 兼容旧进程：没有 instance-tag 的历史版本
                if "l_scheduler.main" in cmdline_text:
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return False

    def _iter_l_scheduler_processes(self):
        """迭代所有 l_scheduler 相关进程（用于显示窗口/重启）。"""
        instance_tag = "l_tray_scheduler"
        for process in psutil.process_iter(["pid", "name", "cmdline"]):
            try:
                cmdline = process.info.get("cmdline") or []
                cmdline_text = " ".join(cmdline).lower()
                if "--instance-tag" in cmdline_text and instance_tag in cmdline_text:
                    yield process
                    continue
                if "l_scheduler.main" in cmdline_text and "--ui" in cmdline_text:
                    yield process
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

    def _show_l_scheduler_window(self) -> bool:
        """尝试把已运行的 l_scheduler 窗口置前显示。"""
        try:
            pids: list[int] = []
            for p in self._iter_l_scheduler_processes():
                try:
                    pids.append(int(p.pid))
                    try:
                        for ch in p.children(recursive=True):
                            try:
                                pids.append(int(ch.pid))
                            except Exception:
                                continue
                    except Exception:
                        pass
                except Exception:
                    continue
            if pids:
                seen = set()
                pids = [x for x in pids if not (x in seen or seen.add(x))]

            hwnd = console.bring_top_level_window_to_front_by_pids(pids)
            if hwnd:
                try:
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
                except Exception:
                    pass
                try:
                    win32gui.PostMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
                except Exception:
                    pass
                try:
                    win32gui.BringWindowToTop(hwnd)
                except Exception:
                    pass
                try:
                    win32gui.SetForegroundWindow(hwnd)
                except Exception:
                    pass
                return True

            # 退化：按标题关键词匹配
            keywords = ["l scheduler", "任务管理", "l_scheduler"]
            found_hwnds = []

            def _enum2(hwnd, _):
                try:
                    title = win32gui.GetWindowText(hwnd) or ""
                    t = title.lower()
                    if any(k in t for k in keywords):
                        found_hwnds.append(hwnd)
                except Exception:
                    pass

            win32gui.EnumWindows(_enum2, None)
            if not found_hwnds:
                return False
            hwnd = found_hwnds[0]
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            try:
                win32gui.SetForegroundWindow(hwnd)
            except Exception:
                pass
            return True
        except Exception:
            return False

    def _restart_l_scheduler(self) -> None:
        """结束已有实例后重新启动。"""
        killed = 0
        for p in list(self._iter_l_scheduler_processes()):
            try:
                p.terminate()
                killed += 1
            except Exception:
                continue
        # 给一点时间退出，必要时强杀
        deadline = time.time() + 3.0
        while time.time() < deadline:
            alive = False
            for p in list(self._iter_l_scheduler_processes()):
                alive = True
                try:
                    if p.is_running():
                        pass
                except Exception:
                    pass
            if not alive:
                break
            time.sleep(0.1)
        for p in list(self._iter_l_scheduler_processes()):
            try:
                p.kill()
            except Exception:
                pass
        self.showMessage("提示", f"已结束 {killed} 个调度器进程，正在重启…", self.icon)
        self.start_rez_package(
            packages=["python-3.12", "Lugwit_Module", "l_scheduler"],
            run_args=[
                "pythonw",
                "-m",
                "l_scheduler.main",
                "--ui",
                "--instance-tag",
                "l_tray_scheduler",
            ],
            action_name="l_scheduler",
        )

    def is_start_multi_app_running(self) -> bool:
        for process in psutil.process_iter(["name", "cmdline"]):
            try:
                cmdline = process.info.get("cmdline") or []
                cmdline_text = " ".join(cmdline).lower()
                if "start_multi_app" in cmdline_text and (
                    "main.py" in cmdline_text or "-m start_multi_app.main" in cmdline_text
                ):
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return False

    @staticmethod
    def _read_log_tail(log_file: str, max_chars: int = 3000) -> str:
        if not log_file:
            return "(no log file)"
        try:
            with open(log_file, "r", encoding="utf-8", errors="replace") as f:
                text = f.read()
            return text[-max_chars:] if text else "(empty log)"
        except Exception as exc:
            return f"读取日志失败: {exc}"

    def _notify_launch_issue(self, title: str, message: str):
        """统一通知：Qt 消息框优先，避免静默失败。"""
        try:
            self.showMessage(title, message[:220], self.icon)
        except Exception:
            pass
        try:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle(title)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText(message if len(message) <= 1800 else message[:1800] + "\n...(truncated)")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setWindowModality(Qt.ApplicationModal)
            msg_box.setWindowFlag(Qt.WindowStaysOnTopHint, True)
            msg_box.raise_()
            msg_box.activateWindow()
            msg_box.exec_()
        except Exception:
            LM.lprint(f"[l_tray] {title}: {message}")

    def _schedule_launch_probe(self, action_name: str, proc, log_file: str):
        """异步探测启动是否快速退出，适用于任何 rez 包启动。"""
        if not hasattr(self, "_rez_launch_probe"):
            self._rez_launch_probe = {}
        probe_id = f"{action_name}_{int(time.time() * 1000)}"
        self._rez_launch_probe[probe_id] = {"proc": proc, "checks": 0, "log_file": log_file, "action": action_name}

        def _tick():
            item = self._rez_launch_probe.get(probe_id)
            if not item:
                return
            item["checks"] += 1
            p = item["proc"]
            exit_code = p.poll()
            if exit_code is not None:
                detail = self._read_log_tail(item["log_file"])
                msg = (
                    f"{item['action']} 进程已退出，exit_code={exit_code}\n"
                    f"日志: {item['log_file']}\n\n最近输出:\n{detail}"
                )
                self._notify_launch_issue("启动失败", msg)
                LM.lprint(
                    f"[l_tray] {item['action']} exited, code={exit_code}, log={item['log_file']}"
                )
                self._rez_launch_probe.pop(probe_id, None)
                return
            if item["checks"] >= 10:
                # 连续探测约 5 秒仍存活，认为启动成功。
                self._rez_launch_probe.pop(probe_id, None)
                return
            QTimer.singleShot(500, _tick)

        QTimer.singleShot(500, _tick)

    def start_rez_package(self, packages: list[str], run_args: list[str], action_name: str) -> bool:
        """公共启动入口：在 rez 环境中静默启动指定命令。"""
        wuwo_dir = os.path.normpath(os.path.join(LugwitToolDir, "wuwo"))
        rez_exe = os.path.join(wuwo_dir, "py_312", "Scripts", "rez.exe")
        if not os.path.exists(rez_exe):
            self._notify_launch_issue("启动失败", f"未找到 rez.exe: {rez_exe}")
            return False

        cmd = [rez_exe, "env", *packages, "--", *run_args]
        LM.lprint(f"[l_tray] {action_name} cmd: {' '.join(cmd)}")

        launch_env = os.environ.copy()
        source_packages = os.path.join(wuwo_dir, "..", "rez-package-source")
        local_packages = os.path.join(wuwo_dir, "packages")
        build_packages = os.path.join(LugwitToolDir, "rez-package-build")
        release_packages = os.path.join(LugwitToolDir, "rez-package-release")
        launch_env["REZ_PACKAGES_PATH"] = ";".join(
            [source_packages, local_packages, build_packages, release_packages]
        )
        launch_env["REZ_CONFIG_FILE"] = os.path.join(wuwo_dir, "rezconfig.py")

        log_dir = os.path.join(os.environ.get("Temp", r"D:\Temp"), "lugwit_start_logs")
        try:
            os.makedirs(log_dir, exist_ok=True)
        except Exception:
            log_dir = os.environ.get("Temp", r"D:\Temp")
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        safe_action = re.sub(r"[^0-9A-Za-z._-]+", "_", action_name)
        log_file = os.path.join(log_dir, f"{safe_action}_{timestamp}.log")
        if not hasattr(self, "_last_rez_launch_logs"):
            self._last_rez_launch_logs = {}
        self._last_rez_launch_logs[action_name] = log_file

        DETACHED_PROCESS = 0x00000008
        CREATE_NEW_PROCESS_GROUP = 0x00000200
        CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = 0
        log_fp = None
        try:
            log_fp = open(log_file, "w", encoding="utf-8", errors="replace")
            log_fp.write(f"[cmd] {' '.join(cmd)}\n")
            log_fp.write(f"[cwd] {wuwo_dir}\n")
            log_fp.write(f"[REZ_PACKAGES_PATH] {launch_env.get('REZ_PACKAGES_PATH', '')}\n")
            log_fp.flush()
            proc = subprocess.Popen(
                cmd,
                shell=False,
                creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW,
                cwd=wuwo_dir,
                env=launch_env,
                startupinfo=startupinfo,
                stdin=subprocess.DEVNULL,
                stdout=log_fp,
                stderr=log_fp,
            )
            # 首次快速探测：抓秒退
            time.sleep(0.8)
            exit_code = proc.poll()
            if exit_code is not None:
                try:
                    log_fp.flush()
                except Exception:
                    pass
                detail = self._read_log_tail(log_file)
                self._notify_launch_issue(
                    "启动失败",
                    f"{action_name} 进程已退出，exit_code={exit_code}\n"
                    f"日志: {log_file}\n\n最近输出:\n{detail}",
                )
                LM.lprint(f"[l_tray] {action_name} exited quickly, code={exit_code}, log={log_file}")
                return False
            # 二次异步探测：抓 1~5 秒内退出
            self._schedule_launch_probe(action_name, proc, log_file)
            LM.lprint(f"[l_tray] {action_name} launched, log={log_file}")
        except Exception as exc:
            self._notify_launch_issue(
                "启动失败",
                f"启动 {action_name} 失败:\n{exc}\n日志: {log_file}",
            )
            return False
        finally:
            if log_fp:
                try:
                    log_fp.close()
                except Exception:
                    pass
        return True

    def start_l_scheduler(self):
        if self.is_l_scheduler_running():
            msg_box = QMessageBox()
            msg_box.setWindowTitle("提示")
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText("定时任务调度器已在运行。")
            btn_show = msg_box.addButton("显示窗口", QMessageBox.AcceptRole)
            btn_restart = msg_box.addButton("重启", QMessageBox.DestructiveRole)
            msg_box.addButton("取消", QMessageBox.RejectRole)
            msg_box.exec_()
            clicked = msg_box.clickedButton()
            if clicked == btn_show:
                ok = self._show_l_scheduler_window()
                if not ok:
                    self._notify_launch_issue(
                        "提示",
                        "检测到调度器在运行，但未找到可显示的窗口（可能已最小化到托盘或窗口标题不同）。",
                    )
                return
            if clicked == btn_restart:
                self._restart_l_scheduler()
                return
            return

        started = self.start_rez_package(
            packages=["python-3.12", "Lugwit_Module", "l_scheduler"],
            run_args=["pythonw", "-m", "l_scheduler.main", "--ui", "--instance-tag", "l_tray_scheduler"],
            action_name="l_scheduler",
        )
        if not started:
            return

        # 异步复核，避免 sleep 阻塞托盘 UI 主线程。
        def _verify_scheduler_started():
            if not self.is_l_scheduler_running():
                QMessageBox.information(None, "提示", "调度器启动命令已发送，但未检测到运行实例。")
                return
            self.showMessage("提示", "已启动定时任务调度器。", self.icon)

        QTimer.singleShot(2000, _verify_scheduler_started)

    def start_scheduler_on_boot(self) -> None:
        """l_tray 启动后自动尝试拉起 l_scheduler。"""
        try:
            self.start_l_scheduler()
        except Exception as exc:
            LM.lprint(f"启动 l_scheduler 失败: {exc}")

    # def writeLoginInfo(self,loginInfoList:Tuple[login_info_dataType.P4LoginInfo,
    #                                          login_info_dataType.P4LoginInfo]):# NOTE 写入登录信息
    #     print ("写入登录信息",'loginInfo',loginInfoList)
    #     if not loginInfoList:
    #         return
    #     from qss_style import qss_style
    #     toolTipList_str = ""
    #     clientTypeEnZhType={'project':'项目','plug':'插件'}
    #     login_info_dataType.write_p4login_info(loginInfoList)
    #     for loginInfo in loginInfoList:
    #         if not loginInfo:
    #             continue
    #         #self.writeDepartInfo(loginInfo)
    #         clientType = loginInfo.clientType
    #         port = loginInfo.port
    #         clientType_zh=clientTypeEnZhType.get(clientType)
    #         FullName = loginInfo.FullName
    #         username = loginInfo.User
    #         clientName = loginInfo.clientName
    #         clientRoot = loginInfo.clientRoot
    #         userGroups = loginInfo.userGroups
    #         departEnList = [] # 添加部门UI
    #         departZhList = [] # 添加部门UI
    #         for userGroup in userGroups:
    #             departEnName=userGroup.name
    #             departZhName=userGroup.description
    #             departEnList.append(departEnName)
    #             departZhList.append(departZhName)
    #         if clientType == "project":
    #             self.userNameWgt.setText(f'用户名 : {FullName}')
    #             btn = QPushButton(str(departZhList))
    #             btn.departEnName=str(departEnList)
    #             size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
    #             btn.setSizePolicy(size_policy)
    #             self.departBtnGrp_lay.addWidget(btn)
    #             btn.setStyleSheet(qss_style.loginWidget_style)
    #             btn.setCheckable(True)  # 使按钮可选中
    #             self.departBtnGrp.addButton(btn)
    #             btn.setChecked(True)
    #             if 'TD' not in departEnList:
    #                 self.customDepartBtn.setEnabled(False)
    #             else:
    #                 self.isTD=True
    #         toolTipList_str+=(
    #             (f'{clientType_zh}用户      : {username}<br>'+
    #             f'{clientType_zh}用户全名  : {FullName}<br>'+
    #             f'{clientType_zh}工作区    : {clientName}<br>'+
    #             f'{clientType_zh}工作区目录    : {clientRoot}<br>'+
    #             f'{clientType_zh}部门      : {departEnList}<br>'+
    #             f'{clientType_zh}P4端口    : {port}<br><br>')
    #         )
            



    #     local_ips = get_all_local_ips()
    #     ip_list = []
    #     for interface, ips in local_ips.items():
    #         ip_list.append(f"{interface}: {', '.join(ips)}")

    #     self.userNameWgt.setToolTip(toolTipList_str+'<br>'.join(ip_list))

    #     self.depart_layout.addStretch(1)
    #     if  self.isTD:
    #         return
    #         print("启动聊天室")
    #         l_subprocess.startPyFile(
    #                     LM.LugwitLibDir+r'/ChatRoom/localend/local_app.py',
    #                     'main',
    #                     specify_sys_executable='currentPythonJieShiQi', 
    #                     usePythonw=True)# type: ignore

        
    def onMenuShow(self,lnkDir):
        lnkMenu=self.sender()
        lnkMenu.clear()
        if os.path.exists(lnkDir):
            lnkList=os.listdir(lnkDir)
            icon_provider = QFileIconProvider()
            for item in lnkList:
                item=Lugwit_P4CLIENTDIR+'/Software/lnk/'+item
                if not os.path.isfile(item):
                    continue
                itemBaseName=os.path.basename(item)
                # LM.lprint(itemBaseName)
                item_icon=icon_provider.icon(QFileInfo(item))
                # LM.lprint(QFileInfo(item),item_icon)
                shortcut_icon = QIcon(item_icon)
                out_file=f'{LugwitToolDir}\\icons\\{itemBaseName}.png'
                # LM.lprint (shortcut_icon,out_file)
                if not os.path.exists(out_file):
                    saveQCionToFile(shortcut_icon,out_file)
                # LM.lprint(shortcut_icon)
                lnkMenu.addAction(QAction(QIcon(out_file),
                                    itemBaseName,self, triggered= partial(os.startfile,item ))
                                    )
                
    def set_CGT_env(self):
        # 设置CGT环境变量
        cgt_ini_path = r"D:\TD_Depot\Software\ProgramFilesLocal\cgteamwork\bin\cgtw\config.ini"
        if not os.path.exists(cgt_ini_path):
            lprint(f'CGT配置文件{cgt_ini_path}不存在')
            return
        with open(cgt_ini_path, 'r') as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith('TRUST_DEFINE_URL'):
                lines[i] = 'TRUST_DEFINE_URL=Y\n'
                break
        else:
            lines.append('[Environs]\n')
            lines.append('TRUST_DEFINE_URL=Y\n')
        with open(cgt_ini_path, 'w') as f:
            f.writelines(lines)
            lprint(f'设置CGT环境变量成功')

    def startMaya(self,exeFile="",checked=False,is_dev=False):
         start_maya.startMaya(exeFile,is_dev=is_dev)       
         
           
    def startLogVersionProcess(self):
        pass
    
    def smallCmdMenuItemsA(self,jsonConfigPath='programs.json'):
        # 读取 JSON 配置文件
        jsonConfigPath=LugwitToolDir+'/config/smallProgramList.json'
        lprint (os.path.abspath(jsonConfigPath))
        with open(jsonConfigPath, 'r', encoding='utf-8') as f:
            programs = json.load(f)
        
        widgetAction = QWidgetAction(self)
        widget = QWidget()
        layout = QGridLayout()
        layout.setContentsMargins(5, 3, 0, 2)
        layout.setSpacing(0)
        
        # 创建并添加复选框
        runas = QCheckBox('runas')
        layout.addWidget(runas,0,0)
        grid_params = [(row, col) for row in range(3) for col in range(12)]
        for index,program in enumerate(programs):
            # 设置图标
            exec_full_path = os.path.join(Lugwit_P4CLIENTDIR, program['exec_path'])
            exe_dir=os.path.dirname(exec_full_path)
            icon_name = program.get('icon', '')
            if "./" in  program['icon']:
                icon_full_path = program['icon'].replace("./", exe_dir+"/")
            else:
                icon_full_path = os.path.join(iconDir, program['icon'])
            icon_full_path = os.path.normpath(icon_full_path)
            if not os.path.exists(icon_full_path):
                fallback_icon = os.path.normpath(os.path.join(iconDir, "EnvVar.png"))
                if os.path.exists(fallback_icon):
                    icon_full_path = fallback_icon
                else:
                    icon_full_path = ""
                lprint(f"[smallProgramList] icon not found, fallback used: {icon_name}")
            # 设置按钮点击事件
            btn = ProgramButton(exec_full_path)
            if icon_full_path:
                btn.setIcon(QIcon(icon_full_path))
            
            if runas.isChecked() or program.get('use_runas', False):
                # 如果需要以管理员身份运行
                btn.clicked.connect(partial(
                    subprocess.Popen,
                    f'start {exec_full_path} {program.get("args", "")}',
                    shell=True,
                    env=oriEnvVar
                ))
            else:
                # 普通启动
                btn.clicked.connect(lambda checked, path=exec_full_path: os.startfile(path))
            
            layout.addWidget(btn,*grid_params[index+1])
        

        widget.setLayout(layout)

        widgetAction.setDefaultWidget(widget)
        widget.setStyleSheet('''
            QPushButton {
                max-width: 32px;
                max-height: 29px;
                font-size: 14px;
                color: red;
            }
        ''')

        return widgetAction  
    
    def smallCmdMenuItemsB(self,iconPath=''):
        
        widgetAction = QWidgetAction(self)
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 3, 0, 2)
        layout.setSpacing(0)

        # 创建并添加按钮
        # layout.addWidget(QLabel('常用命令'))
        btn1 = QPushButton("启动多个程序")
        btn1.clicked.connect(self.start_multi_app)
        
        btn2 = QPushButton("强制结束程序")


        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addStretch()
        widget.setLayout(layout)

        widgetAction.setDefaultWidget(widget)
        widget.setStyleSheet('''
                            QPushButton {
                                font-size: 14px;

                            }
                             ''')

        # 添加自定义菜单项到菜单中
        return widgetAction    

    def start_multi_app(self):
        started = self.start_rez_package(
            packages=["python-3.12", "Lugwit_Module", "start_multi_app"],
            run_args=["start_multi_app"],
            action_name="start_multi_app",
        )
        if not started:
            return

        def _verify_multi_app_started():
            if self.is_start_multi_app_running():
                self.showMessage("提示", "已启动启动多个程序。", self.icon)
                return
            log_file = ""
            if hasattr(self, "_last_rez_launch_logs"):
                log_file = self._last_rez_launch_logs.get("start_multi_app", "")
            detail = self._read_log_tail(log_file)
            QMessageBox.information(
                None,
                "启动失败",
                "已发送启动命令，但未检测到 start_multi_app 运行。\n"
                f"日志: {log_file}\n\n最近输出:\n{detail}",
            )

        QTimer.singleShot(2500, _verify_multi_app_started)

    def start_view_pkl_tool(self):
        started = self.start_rez_package(
            packages=["python-3.12", "view_pkl_tool"],
            run_args=["view_pkl_tool"],
            action_name="view_pkl_tool",
        )
        if not started:
            return

        self.showMessage("提示", "已发送 PKL查看器 启动命令。", self.icon)

    @staticmethod
    def get_plug_varsion():
        p4=loginP4.p4_login(port='192.168.110.61:1666',wsDir=r'D:/TD_Depot',)
        if not p4:
            return None
        syncPLugDir=f'{LM.Lugwit_publicDisc}/Temp/同步历史/{p4.client}'
        syncVersion_txt=f'{syncPLugDir}/niubility.txt'
        if os.path.exists(syncVersion_txt):
            with open(syncVersion_txt,'r') as f:
                current_version = f.read()
        else:
            current_version = '未知'

        latest_change = p4.run("changes", "-m", "1")

        latest_change_number = latest_change[0]['change']
        print(f"Latest Change List Number: {latest_change_number}")
        return current_version,latest_change_number


    def checkNewVersion(self,btn1,current_version_wgt,latest_version_label):
        plug_varsion = self.get_plug_varsion()
        current_version_wgt.setText(f'当前版本: {plug_varsion[0]}')
        latest_version_label.setText(f'最新版: {plug_varsion[1]}')
        btn1.setText("检查成功")
        QTimer.singleShot(1000, lambda:btn1.setText('检查更新'))


    def versionInfo(self,iconPath=''):
        widgetAction = QWidgetAction(self)
        widget = QWidget()
        widget.setFixedHeight(50)
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 3, 0, 2)
        layout.setSpacing(0)

        plug_varsion = self.get_plug_varsion()
        
        current_version_wgt = QLabel(f'当前版本: {plug_varsion[0]}')
        layout.addWidget(current_version_wgt)

        layout.addSpacing(20)

        latest_version_label = QLabel(f'最新版: 待检查')
        layout.addWidget(latest_version_label)

        layout.addSpacing(20)
        btn1 = QPushButton("检查更新")
        btn1.clicked.connect(
            lambda: self.checkNewVersion(btn1,current_version_wgt, latest_version_label))

        layout.addWidget(btn1)
        layout.addStretch()
        widget.setLayout(layout)

        widgetAction.setDefaultWidget(widget)


        # 添加自定义菜单项到菜单中
        return widgetAction    
    def loginMenuItems(self):
        widgetAction = QWidgetAction(self)
        widget = QWidget()
        layout = QHBoxLayout()
        widget.setLayout(layout)
        layout.setContentsMargins(0, 3, 0, 2)
        iconPath=iconDir+r'\persion_info.png'
        # 创建并添加按钮
        icon_label = QLabel("用户名 : XXX")
        set_ptn = QPushButton ("设置")
        pixmap = QPixmap(iconPath)  # 替换为你的图标文件路径
        scaled_pixmap = pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # 调整尺寸
        icon_label.setPixmap(scaled_pixmap)
        layout.addWidget(icon_label)
        self.userNameWgt = QLabel("用户名:XXX")
        layout.addWidget(self.userNameWgt)
        layout.addStretch()
        layout.addWidget(set_ptn)
        
        

        widgetAction.setDefaultWidget(widget)

        # 添加自定义菜单项到菜单中
        return widgetAction 
    
    # 显示用户信息,自定义部门从文件读取,其他信息实时获取
    def userInfoMenuItems(self,iconPath=''):
        return
        widgetAction = QWidgetAction(self)
        widget = QWidget()
        self.depart_layout = QHBoxLayout()
        widget.setLayout(self.depart_layout)
        self.depart_layout.setContentsMargins(0, 3, 0, 2)

        departLable = QLabel("部门:")
        

        self.departBtnGrp=QButtonGroup(self)
        self.departBtnGrp.setExclusive(True)  # 设置为互斥模式
        
        self.departBtnGrp_lay = QHBoxLayout()


        self.depart_layout.addWidget(departLable)
        self.depart_layout.addLayout(self.departBtnGrp_lay)

        self.depart_layout.addSpacing(10)
        self.depart_layout.addWidget(QLabel("自定义:"))
        customGroups=login_info_dataType.get_p4login_info_value(
                        'project',
                        'customGroups')
        lprint(customGroups)
        self.customDepartBtn = QComboBox()
        self.customDepartBtn.addItems(["None",'灯光实习生组','灯光组','解算组','TD','动画组'])
        if customGroups:
            self.customDepartBtn.setCurrentText(customGroups[0])
        self.customDepartBtn.currentTextChanged.connect(self.departButtonChange)
        self.depart_layout.addWidget(self.customDepartBtn)

        widgetAction.setDefaultWidget(widget)

        # 添加自定义菜单项到菜单中
        return widgetAction 
    
    @LM.try_exp
    def check_td_user(self):
        from lperforce.P4LoginInfoModule import p4_loginInfo
        project_info = p4_loginInfo.get("project") if isinstance(p4_loginInfo, dict) else None
        if not isinstance(project_info, dict):
            return False
        user_groups = project_info.get("userGroups") or []
        for group in user_groups:
            if not isinstance(group, dict):
                continue
            group_name=group.get('name')
            lprint(group_name)
            if group_name == 'TD':
                return True
        return False
            
    def departButtonChange(self,text : str = ''):
        login_info_dataType.update_p4login_info('project',
                                                'customGroups',
                                                [text])
        

    @staticmethod
    def isStudentHost():
        return re.search('^DB|^An\d+',LM.hostName)
    



    def p4Tools(self,iconPath=iconDir+'/p4v.png'):
        widgetAction = QWidgetAction(self)
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 3, 0, 2)

        # 创建并添加按钮
        icon_label = QLabel()
        pixmap = QPixmap(iconPath)  # 替换为你的图标文件路径
        scaled_pixmap = pixmap.scaled(15, 15, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # 调整尺寸
        icon_label.setPixmap(scaled_pixmap)
        btn1 = QPushButton("清理P4工作区")
        btn1.clicked.connect(partial(l_subprocess.startPyFile,ins.__file__,
                                            sys_argv=['cleanWorkSpace'],
                                            usePythonw=False
                                            ))
        
        layout.addWidget(icon_label)
        layout.addWidget(btn1)

        btn2 = QPushButton("下载常用软件到本地")
        btn2.clicked.connect(
            partial(l_subprocess.startPyFile,ins.__file__,
                                            sys_argv=['copyProgramFilesLocal'],
                                            usePythonw=False
                                            )
                        )
        layout.addWidget(icon_label)
        layout.addWidget(btn2)

        layout.addStretch()
        widget.setLayout(layout)

        widgetAction.setDefaultWidget(widget)

        # 添加自定义菜单项到菜单中
        return widgetAction 

    
    def showMsg(self):
        self.showMessage("Message", "skr at here", self.icon)
    
    
    def switchMayaLanguage(self, language):
        u"""切换Maya语言设置
        
        Args:
            language (str): 语言代码，支持 'zh_CN' 或 'en_US'
        """
        try:
            import os
            import subprocess

            if language not in ['zh_CN', 'en_US']:
                lprint(f"不支持的语言代码: {language}")
                return

            lprint(f"切换Maya语言前: {os.getenv('MAYA_UI_LANGUAGE')}")
            
            # 构建设置命令
            cmd = f'cmd /k echo setx MAYA_UI_LANGUAGE {language} && set MAYA_UI_LANGUAGE {language} && setx MAYA_UI_LANGUAGE {language} && timeout /t 2'
            
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            # 执行命令并等待完成
            process = subprocess.Popen(cmd, startupinfo=None)  # 显示命令窗口以便用户看到执行过程

            # 同步环境变量到当前进程
            os.environ["MAYA_UI_LANGUAGE"] = language
            
            lprint(f"切换Maya语言后: {os.getenv('MAYA_UI_LANGUAGE')}")
            lprint(f"Maya语言已成功切换为: {'中文' if language == 'zh_CN' else '英文'}")
            
        except Exception as e:
            error_msg = f'切换Maya语言失败，原因: {e}'
            lprint(error_msg)
            import win32con, win32gui
            win32gui.MessageBox(0, error_msg, "错误", win32con.MB_OK | win32con.MB_ICONWARNING)

    def runSysCmd(self,command,showCommandWin=False,admin_run=False):
        try:
            import os
            import subprocess


            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            if showCommandWin:
                startupinfo = None

            lprint(command,os.getenv("MAYA_UI_LANGUAGE"))
            
            if admin_run:
                # 使用 l_admin 以管理员权限运行命令
                l_admin.runAsAdmin(pyexe='cmd.exe', pyfile='', args=['/c', command])
            else:
                # 使用 Popen 运行命令，不弹出命令提示符窗口，且不阻塞进程
                process = subprocess.Popen(command, startupinfo=startupinfo)
            lprint(command,os.getenv("MAYA_UI_LANGUAGE"))
            # 在此处执行其他任务
            LM.lprint("Other tasks can continue while the command is running.")

            # 若要在稍后的某个时间点等待命令完成，可以使用 process.wait()
            # process.wait()
        except Exception as e:
            QMessageBoxinfo=f'你要运行的命令\n{command}\n出错,原因是{e}'
            LM.lprint (QMessageBoxinfo)
            import win32con, win32gui
            response = win32gui.MessageBox(0, QMessageBoxinfo, "Confirm", win32con.MB_OK | win32con.MB_ICONWARNING)


        
    def startProcess(self,ExeFile,startParm="",env={}):
        lprint(locals())
        if not startParm:
            startParm=""
        print ("startParm",startParm)
        print (f'启动程序{ExeFile}')
        filePath=re.search(r'"(.+)"',ExeFile)
        ExeFile = os.path.normpath(ExeFile)
        ExeFile=ExeFile.replace('"','')
        if isinstance(env,bool):
            env= {}
        oriEnvVar.update(env)
        if filePath:
            filePath=filePath.group(1)
        else:
            filePath=ExeFile
            
        if not os.path.exists(filePath):
            MessageBoxinfo=f'你要启动的程序\n{filePath}\n不存在'
            import win32con, win32gui
            response = win32gui.MessageBox(
                    0, MessageBoxinfo, "Confirm", 
                    win32con.MB_OK | win32con.MB_ICONWARNING)
            return


        # 使用subprocess.run启动子进程并等待其完成，同时捕获输出
        
        cmd = [ExeFile.replace('\\','/'),startParm]
        print ('启动命令的cmd',cmd)
        DETACHED_PROCESS = 0x00000008
        CREATE_NEW_PROCESS_GROUP = 0x00000200
        process = subprocess.Popen(cmd, 
                                text=True, 
                                shell=True,
                                encoding='gbk',
                                env=oriEnvVar,
                                stderr=subprocess.PIPE,
                                creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,
                                cwd=os.path.dirname(ExeFile))
        
        # 检查进程是否成功执行
        time.sleep(1)
        # 等待进程结束并获取输出
        lprint (process.pid,psutil.pid_exists(process.pid))
        if psutil.pid_exists(process.pid):
            print("子进程成功执行---")
        else:
            # 等待进程结束并获取输出
            stdout, stderr = process.communicate()
            print("stderr",stderr)
            l_subprocess.ps_win.showMessageWin(title='Error',text=stderr)
            #QMessageBox.information(None,'提示',result.stderr,QMessageBox.StandardButton.Yes)


 
    def show_window(self):
        #若是最小化，则先正常显示窗口，再变为活动窗口（暂时显示在最前面）
        return
        self.ui.showNormal()
        self.ui.activateWindow()

    def sync_Lugwit_Module(self):
        os.system(r'python37 D:\plug_in\Lugwit_plug\Python\PythonLib\Lugwit_rightMenuLib.py sync_Lugwit_Module')

    def openDocAction(self):
        try:
            webbrowser.open(r'https://www.kdocs.cn/l/cpJPm0FHD1lg')
        except:
            l_subprocess.ps_win.showMessageWin(title='Error',text=traceback.format_exc())
        
    
    def runFuncA(self,func):
        try:
            func()
        except:
            l_subprocess.ps_win.showMessageWin(title='Error',text=traceback.format_exc())
            #QMessageBox.information(None,'提示',traceback.format_exc(),QMessageBox.StandardButton.Yes)

    def runFunc(self,func):
        return partial(self.runFuncA,func)
    def quit(self):
        parentProcID=os.environ.get('parentProcID')
        # current_process_id = os.getpid()
        # get_child_processes(current_process_id)
        os.system(f'taskkill /F /IM lugwit_insapp.exe')
        os.system(f'taskkill /F /IM /PID {parentProcID}')
        # for child_process in range(child_processes):
        #     os.system(f'taskkill /F /IM /PID {child_process}')
        os.system(f'taskkill /F /IM lugwit_pythonw.exe')
        sys.exit()
        
    def trayToolCodeToADisk(self):
        os.startfile(LM.LugwitAppDir+r'\同步Lugwit托盘工具到A盘.bat')
    
    def restart(self):
        wuwo_bat = os.path.normpath(os.path.join(LugwitToolDir, "wuwo", "wuwo.bat"))
        if not os.path.exists(wuwo_bat):
            QMessageBox.information(None, "提示", f"未找到 wuwo.bat: {wuwo_bat}")
            return

        cmd = [
            "cmd",
            "/c",
            wuwo_bat,
            "rez",
            "env",
            "python-3.12",
            "Lugwit_Module",
            "l_tray",
            "--",
            "start_tray",
        ]
        DETACHED_PROCESS = 0x00000008
        CREATE_NEW_PROCESS_GROUP = 0x00000200
        try:
            subprocess.Popen(
                cmd,
                shell=False,
                cwd=os.path.dirname(wuwo_bat),
                creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,
                env=os.environ.copy(),
            )
        except Exception as exc:
            QMessageBox.information(None, "提示", f"重启启动失败:\n{exc}")
            return

        sys.exit()
        
    
    def login(self):
        pass
        l_subprocess.startPyFile( LugwitToolDir +r"\src\lugwit_login\loginUI.py",
                                sys_argv=['main'],
                                usePythonw=True
                                )

    
    @staticmethod
    def updateAndRestart():
        titleList=[u"管理员: 0lugwit_insapp (Admin)",u"0lugwit_insapp"]
        hwnd = console.find_window_by_title(titleList)
        vis = console.is_window_visible(hwnd)
        if  not vis:
            console.hide_taskbar_icon()
        path=LM.Lugwit_publicPath+r'\Python\PyFile\syncPlugLib\update.bat'
        if not os.path.exists(path):
            msg = f"未找到更新脚本: {path}"
            LM.lprint(msg)
            QMessageBox.information(None, "提示", msg)
            return
        try:
            subprocess.Popen(path,env=oriEnvVar)
        except Exception as e:
            LM.lprint(e)
            QMessageBox.information(None, "提示", f"启动更新失败:\n{e}")

    #鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
    def onIconClicked(self, reason):
        self.stop_blinking()
        from Lugwit_Module.l_src.UILib import toggle_ui_visable
        if not os.path.exists('D:/TD_Depot/Temp/chatroom.txt'):
            return
        with open('D:/TD_Depot/Temp/chatroom.txt','r') as f:
            hwnd=int(f.read())
        
        if reason == QSystemTrayIcon.Trigger:  # 单击图标
            try:
                toggle_ui_visable.toggle_win_vis_by_hwnd(hwnd)
            except:
                pass
        # if reason == 2 or reason == 3:
        #     # self.showMessage("Message", "skr at here", self.icon)
        #     if self.ui.isMinimized() or not self.ui.isVisible():
        #         #若是最小化，则先正常显示窗口，再变为活动窗口（暂时显示在最前面）
        #         self.ui.showNormal()
        #         self.ui.activateWindow()
        #         self.ui.setWindowFlags(Qt.Window)
        #         self.ui.show()
        #     else:
        #         #若不是最小化，则最小化
        #         self.ui.showMinimized()
        #         self.ui.setWindowFlags(Qt.SplashScreen)
        #         self.ui.show()
        #         # self.ui.show()

    def ArnoldVersionMenu(self):
        ArnoldMenu = self.menu.addMenu(QIcon(iconDir+r'\arnold.png'),'切换Arnold版本')
        arnoldVersionDir=os.getenv('ArnoldVersionDir')
        if not arnoldVersionDir:
            return
        if not os.path.exists(arnoldVersionDir):
            return

        for x in os.listdir(arnoldVersionDir):
            absPath=arnoldVersionDir+'\\'+x
            if os.path.isdir(absPath):
                mayaVersion,arnoldVersion=x.split('_')
                ArnoldMenu.addAction(QAction(QIcon(iconDir+r'\arnold.png'),
                    f'Maya{mayaVersion}_mtoa{arnoldVersion}', self, triggered=partial(toggleArnoldVersion,mayaVersion,arnoldVersion)))
                


    def toggle_overlay(self):
        """
        切换叠加字符的显示与隐藏，以实现闪动效果。
        """
        if self.overlay_visible:
            # 隐藏叠加符号，恢复原图标
            self.setIcon(QIcon(self.tray_icon_path))
            self.overlay_visible = False
        else:
            # 显示叠加符号
            # overlay_icon = self.draw_overlay_icon(self.tray_icon_path, text="!")
            self.setIcon(QIcon(self.new_message_icon_path))
            self.overlay_visible = True

    def start_blinking(self,date='',interval=500,*args,**kwargs):
        return 1111
        """
        启动叠加字符闪动效果。
        """
        # self.showMessage("提示标题", json.dumps(date,indent=4), 
        #                  QSystemTrayIcon.Information, 4000)
        lprint(locals())
        self.overlay_visible = False
        self.blink_timer.start(interval)
        return 1111

    def stop_blinking(self):
        return
        self.blink_timer.stop()
        print("停止闪烁")
        self.setIcon(QIcon(self.tray_icon_path))
        self.overlay_visible = False

    def on_tray_icon_activated(self,reason):
        if reason == QSystemTrayIcon.Trigger:
            import subprocess
            python_exe=sys.executable
            script_path = r"D:\TD_Depot\Software\PiplineTool\main.py"
            script_dir = os.path.dirname(os.path.abspath(script_path))
            subprocess.Popen([python_exe, script_path,"--noprint","1"], cwd=script_dir)
            
        elif reason == QSystemTrayIcon.Context:
            print("右键单击")
        elif reason == QSystemTrayIcon.DoubleClick:
            print("双击")
        elif reason == QSystemTrayIcon.MiddleClick:
            print("中键单击")


def toggleArnoldVersion(mayaVersion='2018',arnoldVersion='402'):
    # C:\Program Files\Common Files\Autodesk Shared\Modules\Maya\2018
    ArnoldVersionDir=os.getenv('ArnoldVersionDir')
    LM.lprint ('ArnoldVersionDir',ArnoldVersionDir)
    if not ArnoldVersionDir:
        return
    arnoldVerMtoaFile=f'{ArnoldVersionDir}\\{mayaVersion}_{arnoldVersion}\\mtoa.mod'

    #mtoaFileInAutodesk_Shared=f'"C:\\Program Files\\Common Files\\Autodesk Shared\\Modules\\Maya\\{mayaVersion}\\mtoa.mod"'
    mtoaFileInDocPath=f'{getDocPath()}\\maya\\{mayaVersion}\\modules\\mtoa.mod'
    os.system(f'echo F| xcopy/y/r {arnoldVerMtoaFile} {mtoaFileInDocPath}')
    LM.lprint (f'echo F| xcopy/y/r {arnoldVerMtoaFile} {mtoaFileInDocPath}')
    QMessageBoxinfo=f'arnold版本已为你切换到{arnoldVersion},是否立即启动Maya'
    import win32con, win32gui
    response = win32gui.MessageBox(0, QMessageBoxinfo, "Confirm", win32con.MB_YESNO | win32con.MB_ICONWARNING)
    if response == win32con.IDYES:
        os.startfile(eval(f'maya{mayaVersion}InsPath')+'/bin/Maya.exe')


def tray_toggle_win_vis_by_hwnd():
    LM.lprint('comenu_hwnd',os.environ['comenu_hwnd'])
    comenu_hwnd = os.getenv('comenu_hwnd')
    toggle_ui_visable.toggle_win_vis_by_hwnd(int(comenu_hwnd))


def remove_unicode_invisible_chars(s):
    invisible_chars = [
        '\u200C',  # 零宽非连字符
        '\u200B',  # 零宽空格
        '\u200D',  # 零宽连字符
        '\uFEFF',  # 字节顺序标记
        '\u2060',  # 单词连接符
        # 根据需要添加更多
    ]
    # 创建正则表达式，匹配所有定义的不可见字符
    regex_pattern = '[' + ''.join(invisible_chars) + ']'
    
    # 使用正则表达式替换掉这些字符
    cleaned_string = re.sub(regex_pattern, '', s)
    
    return cleaned_string
       
def saveQCionToFile(qcion, output_file):
    # 设置想要保存的图标尺寸
    size = (64, 64)
    # 从QIcon获取QPixmap对象
    pixmap = qcion.pixmap(*size)
    # 将QPixmap对象保存为PNG格式
    byte_array = QByteArray()
    buffer = QBuffer(byte_array)
    buffer.open(QIODevice.WriteOnly)
    pixmap.save(buffer, 'PNG')
    # 将字节数据写入文件
    with open(output_file, 'wb') as f:
        f.write(byte_array.data())



# 获取当前进程的所有子进程
def get_child_processes(parent_pid):
    child_processes = []
    for process in psutil.process_iter(attrs=['pid', 'ppid']):
        if process.info['ppid'] == parent_pid:
            child_processes.append(process)
    return child_processes









if __name__ == "__main__":
    app = QApplication(sys.argv)
    win=TrayIcon()
    # win.updateNukePlug()
    win.show()
    sys.exit(app.exec_())
    
