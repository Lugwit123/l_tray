# coding:utf-8
# from Lugwit_Module import *
import random
import traceback,time,json,re,os
from collections import OrderedDict
import threading
import atexit
st=time.time()
import ctypes

# Perforce 功能开关（与 ins.py 中的 ENABLE_PERFORCE 保持一致）
ENABLE_PERFORCE = False

import winreg as reg
from importlib  import reload
from multiprocessing import Process 

import subprocess
import sys, psutil, os, datetime, time,re,codecs


# Try to import L_Tools (optional)
try:
    from L_Tools.sys_tool import l_window
    L_TOOLS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: L_Tools not available: {e}")
    L_TOOLS_AVAILABLE = False
    l_window = None
oriEnvVarFile=os.path.expandvars("%USERPROFILE%")+r'/.Lugwit/config/oriEnvVar.json'
LugwitToolDir=re.search('.+trayapp',__file__).group()
os.environ["LugwitToolDir"]=LugwitToolDir
if not os.path.exists(oriEnvVarFile):
    oriEnvVarFile_Dir=os.path.dirname(oriEnvVarFile)
    os.makedirs(oriEnvVarFile_Dir,exist_ok=True)
    os.environ['oriEnvVarFile']=oriEnvVarFile
    oriEnvVar=os.environ.copy()
    sys.path.append(LugwitToolDir+'/Lib')

    sys_executable_dir=os.path.dirname(sys.executable)
    sys_executable_dir =os.path.realpath(sys_executable_dir)
    path=os.getenv('PATH')
    # 分割PATH，过滤掉包含Python解释器目录的路径
    filtered_path = []
    userName=os.getenv('USERNAME')
    print ('sys_executable_dir',sys_executable_dir)
    for x in path.split(';'):
        x = os.path.realpath(x)
        if  os.path.dirname(sys_executable_dir) not in x and 'conda' not in x:
            filtered_path.append(x) 
        else:
            print('x',x)
    path=';'.join(filtered_path)
    oriEnvVar['PATH'] =path
    print("PYTHONPATH",os.getenv("PYTHONPATH"))
    oriEnvVar.pop('PYTHONHOME',None)
    # oriEnvVar.pop('PYTHONPATH',None)

    with codecs.open(oriEnvVarFile,'w',encoding='utf-8') as f:
        json.dump(oriEnvVar,f,ensure_ascii=False,indent=4)



insapp_path=__file__
curDir=os.path.dirname(insapp_path)
os.environ['insapp_path']=insapp_path

LugwitToolDir=re.search('.+trayapp',__file__).group().capitalize()
LugwitToolDir = os.path.realpath(LugwitToolDir)
# Use temp directory as fallback instead of hardcoded path
LugwitToolDir_env=os.path.realpath(os.environ.get('LugwitToolDir', os.path.join(os.path.expanduser("~"), '.lugwit')))
print ('LugwitToolDir_env,LugwitToolDir',LugwitToolDir_env,LugwitToolDir)
if  LugwitToolDir_env.lower()!=LugwitToolDir.lower():
    print("set env var LugwitToolDir")
    os.system(f'cmd/c setx LugwitToolDir {LugwitToolDir}')


sys.path.append(LugwitToolDir+'/Lib')    
env_var_jsonFile=curDir+'/env_var.json'

# Try to import Lugwit_Module (optional)
try:
    from Lugwit_Module import *
    from Lugwit_Module.l_src import l_os
    from Lugwit_Module.l_src import l_subprocess
    import Lugwit_Module as LM
    
    # Check if required attributes exist
    if hasattr(LM, 'Lugwit_publicDisc') and hasattr(LM, 'hostName') and hasattr(LM, 'userName'):
        LUGWIT_MODULE_AVAILABLE = True
    else:
        print("Warning: Lugwit_Module imported but missing required attributes")
        LUGWIT_MODULE_AVAILABLE = False
        LM = None
except ImportError as e:
    print(f"Warning: Lugwit_Module not available: {e}")
    LUGWIT_MODULE_AVAILABLE = False
    LM = None
    l_os = None
    l_subprocess = None

# 获取ConEmu64_lugwit.exe的主窗口句柄（仅在 L_Tools 和 Lugwit_Module 可用时）
if L_TOOLS_AVAILABLE and LUGWIT_MODULE_AVAILABLE:
    main_window = l_window.get_main_window_by_process_name('ConEmu64_lugwit.exe')
    if main_window:
        hwnd = main_window.hwnd
        os.environ['comenu_hwnd'] = str(hwnd)
        print(f"ConEmu主窗口句柄: {hwnd}, 已设置环境变量")
    else:
        # 如果没有主窗口，尝试获取所有窗口的第一个
        windows = l_window.get_windows_by_process_name('ConEmu64_lugwit.exe', include_invisible=True)
        if windows:
            hwnd = windows[0].hwnd
            os.environ['comenu_hwnd'] = str(hwnd)
            print(f"ConEmu窗口句柄: {hwnd}, 已设置环境变量")
    if LM.hostName not in ['DESKTOP-LDSM1H1','TD','PC-20240202CTEU',"TD2","TD3"]:
        # 直接获取ConEmu窗口句柄并立即隐藏
        try:
            # 立即隐藏ConEmu64_lugwit.exe的所有窗口
            hidden_count = l_window.hide_process_windows('ConEmu64_lugwit.exe', hide_main_only=False)
            if hidden_count > 0:
                print(f"成功隐藏 {hidden_count} 个 ConEmu64_lugwit.exe 窗口")
            else:
                print("未找到需要隐藏的 ConEmu64_lugwit.exe 窗口")
        except Exception as e:
            print(f"处理 ConEmu64_lugwit.exe 窗口时出错: {e}")
else:
    print("Warning: L_Tools or Lugwit_Module not available, skipping ConEmu window management")


# Setup log path (only if Lugwit_Module is available)
if LUGWIT_MODULE_AVAILABLE:
    logPath=f"{LM.Lugwit_publicDisc}/Temp/Log/tray/{LM.hostName}_{LM.userName}/{LM.getCurrentTimeAsLogName()}.log"
    if not os.path.exists(os.path.dirname(logPath)):
        os.makedirs(os.path.dirname(logPath))
else:
    # Use fallback log path
    logPath = os.path.join(os.path.expanduser("~"), ".lugwit", "tray.log")
    os.makedirs(os.path.dirname(logPath), exist_ok=True)
    print(f"Warning: Using fallback log path: {logPath}")




from mainUI import Ui_MainWindow as Main_Ui  # 导入利用Qt设计的界面代码


from Tray import TrayIcon



from PyQt5.QtWidgets import QMessageBox, QMainWindow, QApplication, QWidget
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
DeadlineWorkder_file=fr'{LM.LugwitLibDir}\L_Scheduled_Task\start_DeadlineWorkder.py'


app = QApplication(sys.argv)

# 托盘入口：关闭所有窗口也不应退出进程（否则 QMessageBox 等会误杀托盘）。
try:
    app.setQuitOnLastWindowClosed(False)
except Exception:
    pass

from ctypes import windll
import time
import win32file
from win32file import *

os.makedirs(r'D:\TD_Depot\Temp',exist_ok=True)

# 逻辑代码
class main_logic(QMainWindow, Main_Ui):

    def __init__(self):
        super(main_logic, self).__init__()
        self.setupUi(self)


def is_open(filename):
    try:
        #首先获得句柄
        vHandle =win32file.CreateFile(filename, GENERIC_READ, 0, None, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, None)
        #判断句柄是否等于INVALID_HANDLE_VALUE
        if int(vHandle)==INVALID_HANDLE_VALUE:
            print("# file is already open")
            return True # file is already open
        win32file.CloseHandle(vHandle)
    except Exception as e:
        print(e)
        return True

ct=time.time()
Lugwit_publicDisc='A:\\'
syncLogFile=f'{Lugwit_publicDisc}\\temp\\syncLog.txt'


def syncInfo():
    waitTime= 0.1  if time.time()-ct<0.5 else 10
    print ('waitTime',waitTime)
    while True:
        time.sleep(waitTime)
        receiveSyncPlugInfo_newFile=Lugwit_publicPath+r'\Lugwit_syncPlug\receiveSyncPlugInfo_new.py'
        printcontent = subprocess.run(f"{lugwit_PluginPath}\\Python\\Python37\\python.exe {receiveSyncPlugInfo_newFile}",
                                    stdout=subprocess.PIPE,shell=True)
        print (printcontent,type(printcontent))
        syncSsuccess=False
        while True:
            while not is_open(syncLogFile):
                with open(syncLogFile,'a+') as f:
                    try:
                        print (printcontent,type(printcontent))
                        try:
                            printcontent_str=printcontent.stdout.decode("gbk")
                        except:
                            printcontent_str=printcontent
                        print (printcontent_str)
                        printcontent=printcontent_str.replace('\r\n', '\n')
                        printcontent=re.search('更新结果:.+',printcontent,flags=re.S|re.M).group()
                        print(repr(printcontent))
                        f.write(printcontent+'\n')
                    except Exception as e:
                        traceback.print_exc()
                syncSsuccess=True
            if syncSsuccess:
                break
                #break
# syncInfo()
# sys.exit(0)


def cleanFileP4():
    if not ENABLE_PERFORCE:
        return
    import ins
    while True:
        sys.path.insert(0,Lugwit_publicPath+r'\Python\PyFile\ins.py')
        p4=ins.cleanWorkSpace()
        time.sleep(36000)

def checkSymbel():
    check_path = LugwitPath+ '/Python/Lugwit_Module'
    check_path = os.path.normpath(check_path)
    sorceDir=LugwitToolDir+'/Lib/Lugwit_Module'
    sorceDir = os.path.normpath(sorceDir)
    while True:
        time.sleep(6)
        aa=l_os.check_path (check_path)
        if aa=='symLink':
            continue
        if aa=='realDir':
            os.rmdir(check_path)
        os.system(fr'mklink /J {check_path} {sorceDir}')
        time.sleep(6)

def mulProcess():
    global checkSymbel_Process
    # p = Process(target=syncInfo)
    checkSymbel_Process = Process(target=checkSymbel)
    checkSymbel_Process.daemon = True  # 设置子进程为守护进程
    checkSymbel_Process.start()
    os.environ['checkSymbelProcess']=str(checkSymbel_Process.pid)
    # atexit.register(lambda : checkSymbel_Process.terminate())  # 显式终止子进程) 

        
    # p = Process(target=cleanFileP4)
    # p.start()
    # print (f'启动多进程{p}清理数据')
    
def mulThread_syncFile():
    #time.sleep(300)
    return
    subprocess.Popen(f'python.exe {DeadlineWorkder_file}',shell=True)
    os.system("timeout /t 200")
    while True:
        try:
            MulTread_plug=dynamic_import(module_path=r"A:\TD\Lugwit_syncPlug\lugwit_insapp\trayapp\src\MulTread_plug.py")
            MulTread_plug.main()
        except:
            print (traceback.print_exc())
        subprocess.Popen(f'python.exe {DeadlineWorkder_file}',shell=True)
        time.sleep(5600*random.uniform(1.0, 1.5))
        #start_DeadlineWorkder.create_task()
        
        
def start_p4v_embed_win():
    if not ENABLE_PERFORCE:
        return

    python_exe_path=LM.LugwitAppDir+r'\python_env\pythonw_p4v_embed_win.exe'
    if is_process_running('pythonw_p4v_embed_win.exe'):
        os.system(f'taskkill /f /im pythonw_p4v_embed_win.exe')
    with codecs.open(LM.oriEnvVarFile,'r',encoding='utf-8') as f:
        env_var=json.load(f)
    DETACHED_PROCESS = 0x00000008
    CREATE_NEW_PROCESS_GROUP = 0x00000200

    subprocess.Popen(f'{python_exe_path} {LM.LugwitLibDir}\\controlP4V\\main.py',
                    shell=False,
                    creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,
                    env=env_var)
# 定义一个函数来获取特定进程的启动时间
def getCreateTimeDict(process_name):
    createTimeDict={}
    for proc in psutil.process_iter():
        try:
            # 检查进程名称是否匹配
            if process_name.lower() in proc.name().lower():
                createTimeDict[str(proc.create_time())]=proc
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    # print ('CreateTimeDict:',createTimeDict)
    return createTimeDict

CreateTimeDict=getCreateTimeDict('lugwit_insapp.exe')
CreateTimeDict=OrderedDict(sorted(CreateTimeDict.items()))
# print ('CreateTimeDict:',CreateTimeDict)

_len=len(CreateTimeDict.items())
if CreateTimeDict and _len>1:
    for index,(createTime,proc) in enumerate(CreateTimeDict.items()):
        if index != _len-1:
            # 创建置顶的消息框
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle('程序已经在运行')
            msg_box.setText(f"关闭已经存在的lugwit_insapp.exe pid-{proc.pid} -len{_len}")
            msg_box.setStandardButtons(QMessageBox.Ok)
            # 设置窗口置顶
            msg_box.setWindowFlags(msg_box.windowFlags() | QtCore.Qt.WindowType.WindowStaysOnTopHint)
            msg_box.exec_()
            try:
                proc.kill()
            except:
                pass

def monitorParentProcIsRunning():
    parentProcID=os.environ.get('parentProcID')
    if parentProcID:
        parentProcID=int(parentProcID)
        while True:
            time.sleep(2)
            if not psutil.pid_exists(parentProcID):
                try:
                    checkSymbel_Process.terminate()
                except:
                    pass
                os._exit(0)



def add_to_startup(file_path=None):
    # 如果没有提供路径，则默认使用当前脚本的路径
    if file_path is None:
        file_path = os.path.realpath(__file__)
    
    # 打开注册表项
    key = reg.HKEY_CURRENT_USER
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    
    try:
        reg_key = reg.OpenKey(key, key_path, 0, reg.KEY_ALL_ACCESS)
    except FileNotFoundError:
        reg_key = reg.CreateKey(key, key_path)
    
    # 检查启动项是否已存在
    try:
        existing_value, reg_type = reg.QueryValueEx(reg_key, "Snipaste")
        print ('existing_value',existing_value)
        if existing_value == file_path:
            print(f"{file_path} 已存在于开机启动项中。")
        else:
            reg.SetValueEx(reg_key, "Snipaste", 0, reg.REG_SZ, file_path)
            print(f"{file_path} 已更新到开机启动项中。")
    except FileNotFoundError:
        reg.SetValueEx(reg_key, "Snipaste", 0, reg.REG_SZ, file_path)
        print(f"{file_path} 已成功添加到开机启动项中。")
    
    reg.CloseKey(reg_key)

def check_icon_visibility(tray:TrayIcon):
    while True:
        print("tray.tray_icon.isVisible()",tray.isVisible())
        if not tray.isVisible():
            with open(logPath,'w') as f:
                f.write(f'{time.time()}-Visible change')
            tray.show()  # 重新显示托盘图标
        time.sleep(3600)  # 每小时检查一次
    
    
# 调用函数
add_to_startup(LM.ProgramFilesLocal+r"\Snipaste\Snipaste.exe")

def is_process_running(process_name: str) -> bool:
    for process in psutil.process_iter(['name']):
        if process.info['name'] == process_name:
            return True
    return False

def main():

    # sys.exit(1)
    main_ = QWidget()
    thread = threading.Thread(target=monitorParentProcIsRunning)
    # 不添加这一句的话当main_显示以后关闭之后托盘程序的右键或者左键单击就会失效
    main_.setWindowFlags(QtCore.Qt.SplashScreen)
    tray = TrayIcon(main_) 
    check_thread = threading.Thread(target=check_icon_visibility, args=(tray,),daemon=True)
    print ('显示托盘')

    tray.show()
    check_thread.start()
    thread.start()

def start_deadlineworker_thread():
    start_DeadlineWorkder.create_task()

if __name__ == '__main__':

    #create_shotcut()
    
    userName=os.environ['USERNAME']
    lprint ("os.environ.get('parentProcID')",os.environ.get('parentProcID'))

    if userName=='qqfeng':
        pass
        # mulProcess() # 不在需要磁盘链接
    # main_.show()
    #main_.showMinimized()
    st_tray_time=time.time()
    if ENABLE_PERFORCE:
        start_p4v_embed_win()
    main()
    print (f"启动托盘花费时间{time.time()-st_tray_time}")
    lprint (userName!='qqfeng',hostName!='DESKTOP-LDSM1H1')
    if hostName not in ['DESKTOP-LDSM1H1','TD','PC-20240202CTEU',"TD2","TD3"]:
        syncFile_thread = threading.Thread(target=mulThread_syncFile) 
        syncFile_thread.start()
    # subprocess.Popen(f'{sys.executable} {DeadlineWorkder_file}',shell=True)
    app.setStyle('Fusion')
    sys.exit(app.exec_())

