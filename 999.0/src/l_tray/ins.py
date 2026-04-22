# coding:utf-8
import winreg,os,sys,traceback
import shutil
from typing import Literal

# Perforce 功能开关（与 l_tray/__init__.py 中的 ENABLE_PERFORCE 保持一致）
# 注意：不能导入 l_tray.ENABLE_PERFORCE（循环导入），此处直接定义
ENABLE_PERFORCE = False

# Try to import winshell (optional)
try:
    import winshell
    WINSHELL_AVAILABLE = True
except ImportError as e:
    print(f"Warning: winshell not available: {e}")
    WINSHELL_AVAILABLE = False
    winshell = None

# Use dynamic path instead of hardcoded
curDir=os.path.dirname(os.path.abspath(__file__))
if "LugwitToolDir" not in os.environ:
    # Try to find trayapp directory from current file path
    import re
    match = re.search(r'.+trayapp', curDir, re.IGNORECASE)
    if match:
        os.environ["LugwitToolDir"] = match.group()
    else:
        os.environ["LugwitToolDir"] = os.path.dirname(curDir)

LugwitToolDir = os.environ.get('LugwitToolDir')

sys.path.append(LugwitToolDir+'/Lib')

# Try to import Lugwit_Module (optional)
try:
    from Lugwit_Module import *
    LUGWIT_MODULE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Lugwit_Module not available in ins.py: {e}")
    LUGWIT_MODULE_AVAILABLE = False
import Lugwit_Module as LM
print("LM---------------------------->",LM)


# Try to import lperforce (optional)
if ENABLE_PERFORCE:
    try:
        from lperforce import p4_baselib,loginP4
        LPERFORCE_AVAILABLE = True
    except ImportError as e:
        print(f"Warning: LPerforce not available: {e}")
        LPERFORCE_AVAILABLE = False
        p4_baselib = None
        loginP4 = None
else:
    LPERFORCE_AVAILABLE = False
    p4_baselib = None
    loginP4 = None


tempDir=os.environ['Temp']
sys.path.append(curDir)
StartUp_shortcut = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\0lugwit_insapp.lnk'
# 获取开始菜单的目录路径
programs_path = winshell.programs() if WINSHELL_AVAILABLE else os.path.join(os.environ.get('APPDATA', ''), 'Microsoft', 'Windows', 'Start Menu', 'Programs')
# 创建一个 Shortcut 对象，表示要固定的快捷方式
Programs_shortcut = os.path.join(programs_path, '0lugwit_insapp.lnk')

from  Lugwit_Module.l_src import l_admin
from  Lugwit_Module.l_src.l_subprocess import showMessage_ps
from  Lugwit_Module.l_src import l_subprocess
import  Lugwit_Module as LM

if ENABLE_PERFORCE:
    from controlP4V.findP4vWindows import find_all_p4v_windows
import win32gui
import win32con

from tool_env import *

import ctypes
from ctypes import windll
import time
import win32file
from win32file import *
import codecs

import logging,traceback,re
import  getpass
import subprocess
import  socket
import copy

import winreg
# 添加模块所在路径
st=time.time()
USERPROFILE=os.environ['USERPROFILE']



# 安装插件时从文件读取变量


ip = socket.gethostbyname(socket.gethostname())


# os.system(f'cmd/c md {USERPROFILE}\\.p4qt')
if ENABLE_PERFORCE:
    os.makedirs(fr'{USERPROFILE}\.p4qt',exist_ok=True)


try:
    userName=os.getlogin()
except:
    userName=getpass.getuser()
print ('userName:',userName,__file__)
hostName=socket.gethostname()
insLogFile=  f'A:\\安装记录\\{userName}_{hostName}_log.md'


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

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def getAdminPermission():
    if is_admin():
        pass
    else:
        print ("您不是管理员")
        if sys.version_info[0] == 3:
            print ('重新运行并传递系统变量',' '.join(sys.argv))
            #ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable,' '.join(sys.argv), None, 1)
            print (f'--{is_admin()}--')
        else:#in python2.x
            ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 1)
        print (f'获取管理员权限执行{__file__}')

        
def setPathEnvironmentVariable():
    # 环境变量系统路径 HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Session Manager\Environment
    getAdminPermission()
    if is_admin():
        def setPathEnvironmentVariableFucn(key):
            print (winreg.QueryValueEx(key, "path"),'修改之前')
            pathValue= winreg.QueryValueEx(key, "path")[0]
            pathValue=pathValue.split(';')
            for x in copy.deepcopy(pathValue):
                if 'D:\\plug_in' in x:
                    pathValue.remove(x)
                if ENABLE_PERFORCE and 'Perforce' in x:
                        pathValue.remove(x)
                        
            if f'{lugwit_PluginPath}\\Python\\Python37' not in pathValue:
                pathValue+=[f'{lugwit_PluginPath}\\Python\\Python37']
            if f'{lugwit_PluginPath}\\Python\\Python27' not in pathValue:
                pathValue+=[f'{lugwit_PluginPath}\\Python\\Python27']
            if f'{lugwit_PluginPath}\\Python\\Python27\Scripts' not in pathValue:
                pathValue+=[f'{lugwit_PluginPath}\\Python\\Python27\Scripts']
            if f'{lugwit_PluginPath}\\Python\\Python37\Scripts' not in pathValue:
                pathValue+=[f'{lugwit_PluginPath}\\Python\\Python37\Scripts']
            if r'C:\Program Files\Perforce\\' not in pathValue:
                if ENABLE_PERFORCE:
                    pathValue+=['D:\Program Files\Perforce\\']
            if r'C:\Program Files\Perforce\Server\\' not in pathValue:
                if ENABLE_PERFORCE:
                    pathValue+=['D:\Program Files\Perforce\Server\\']
            pathValue=[r'C:\windows\system32']+pathValue
            pathValue=sorted(list(set(pathValue)),key=pathValue.index)
            #pathValue=sorted(pathValue,key=lambda x: len(x))
            # aa=sorted(['aaaaa','bbbb','ccc','ffff'],key=lambda x: len(x))
            pathValue=';'.join(pathValue).replace(';;',';')
            if pathValue.startswith(';'):
                pathValue=pathValue[1:]
            winreg.SetValueEx(key,'path',1,winreg.REG_SZ,pathValue)
            print (winreg.QueryValueEx(key, "path"))
        key = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER,'Environment',access=winreg.KEY_ALL_ACCESS)
        setPathEnvironmentVariableFucn(key)
        
        key = winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE,
                            'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
                            access=winreg.KEY_ALL_ACCESS)
        
        setPathEnvironmentVariableFucn(key)
        os.system('timeout /t 5')

# print (setPathEnvironmentVariable())
# sys.exit()

def setEnvVariable():
    getAdminPermission()
    if is_admin():
        print (u'现在你是管理员了')
        def setEnvironmentVariableFucn():
            with codecs.open(oriEnvVarJsonFile,'r',encoding='utf8') as f:
                EnvValDict=json.load(f)
                for key,val in EnvValDict.items():
                    os.system(f'setx {key} {val}')
                    os.environ[key]=key
        setEnvironmentVariableFucn()




def modify_connectionmap_xml():
    if not ENABLE_PERFORCE:
        return
    print (u'修改并复制connectionmap_xm文件到.p4qt文件夹')
    connectionmap_xml_template=Lugwit_publicPath+'\\DCCSoftware\\Perforce\\Config\\connectionmap.xml'
    connectionmap_xml_temp=os.environ['temp']+'\\connectionmap.xml'
    os.system(f'echo F| xcopy {connectionmap_xml_template} {connectionmap_xml_temp} /y /r')
    connectionmap_xml=USERPROFILE+'\\.p4qt\\connectionmap.xml'
    with open(connectionmap_xml_temp,'r') as f:
        f_read=f.read()
        f_read=f_read.replace('userName',userName)
        f_read=f_read.replace('P4dIP:Port',P4dIP+':1666')
        print (f_read)
        
    with open(connectionmap_xml,'w') as f:
        f.write(f_read)
        
# modify_connectionmap_xml()
# sys.exit()

def getWsNameByRoot(RootDir_parm='D:/TD_Depot'):
    RootDir_parm=RootDir_parm.replace('\\', '/')
    if RootDir_parm.endswith('/') and len(rootDir)>3:
        RootDir_parm=RootDir_parm[:-1]
    p4=p4_login()
    clients=p4.run_clients('-u',userName)
    for x in clients:
        if x['Host']!=hostName:
            continue
        rootDir=x['Root'].replace('\\', '/')
        if rootDir.endswith('/') and len(rootDir)>3:
            rootDir=rootDir[:-1]
        if rootDir == RootDir_parm :
            return x['client']
    
    
def modify_ApplicationSettings_xml():
    if not ENABLE_PERFORCE:
        return
    #192.168.1.191:1666, qingqing, qingqing_DESKTOP-M9L2CBO_plug
    connectionmap_xml_template=Lugwit_publicPath+'\\DCCSoftware\\Perforce\\Config\\ApplicationSettings.xml'
    connectionmap_xml_temp=os.environ['temp']+'\\ApplicationSettings.xml'
    os.system(f'echo F| xcopy {connectionmap_xml_template} {connectionmap_xml_temp} /y /r')
    connectionmap_xml=USERPROFILE+'\\.p4qt\\ApplicationSettings.xml'
    with open(connectionmap_xml_temp,'r') as f:
        f_read=f.read()
        wsName=getWsNameByRoot(RootDir_parm='D:/TD_Depot')
        connectionString=f'{P4dIP}:1666,{userName},{wsName}'
        f_read=f_read.replace('ConnectionString',connectionString)
        print (f_read)
        
    with open(connectionmap_xml,'w') as f:
        f.write(f_read)
        
def modify_Deadline_config():
    print (u'设置deadline仓库地址')
    os.system(fr'echo D| xcopy A:\TD\dccData\ThinkBox\Deadline_Client\Config\Deadline10 {os.environ["temp"]}\\Config /y /r')
    os.system(f'echo D| xcopy {os.environ["temp"]}\\Config C:\ProgramData\Thinkbox\Deadline10 /r /y')
    

def insLugwitMayaPlug():
    #data\DCC_Software\MayaModule\Lugwit_Module.mod
    Lugwit_Module_modFile=r"D:\TD_Depot\plugins\mayaPlug\MayaModuel\Lugwit_Module.mod"
    Lugwit_mayaPluginPath=os.environ.get('Lugwit_mayaPluginPath')
    with open(Lugwit_Module_modFile , 'r') as f:
        f_read=f.read().replace('$Lugwit_mayaPluginPath',Lugwit_mayaPluginPath)
       
    # os.system(r'Xcopy  {} {}\Maya\modules\ /Y /R'.format(Lugwit_Module_modFile,LM.documentsPath))
    if not os.path.exists('{}/Maya/modules'.format(LM.documentsPath)):
        os.makedirs('{}/Maya/modules'.format(LM.documentsPath))
    Lugwit_Module_modFile_Dir= '{}/Maya/modules'.format(LM.documentsPath)
    Lugwit_Module_modFile_InsFile= fr'{Lugwit_Module_modFile_Dir}/Lugwit_Module.mod'
    lprint ('insLugwitMayaPlug success',Lugwit_Module_modFile_InsFile)
    with open(Lugwit_Module_modFile_InsFile , 'w') as f:
        f.write(f_read)
    fileCheck_modFile=r'D:\TD_Depot\Software\Lugwit_syncPlug\lugwit_insapp\trayapp\data\DCC_Software\MayaModule\fileCheck.mod'
    shutil.copyfile(fileCheck_modFile,f'{LM.documentsPath}/Maya/modules/fileCheck.mod')
    os.startfile(Lugwit_Module_modFile_Dir)
# insLugwitMayaPlug()
# sys.exit()        
def installUEplugin(*args):
    pathA=Lugwit_publicPath+ r'\UE\init_unreal.py'
    print (pathA)
    pathB='{}\\UnrealEngine\\Python\\'.format(getDocPath())
    print ('pathB:', pathB)
    if not os.path.exists(pathB):
        os.makedirs(pathB)
    copyStr=f'Xcopy {pathA} {pathB} /Y /R'
    print ('copyStr',copyStr)
    os.system(copyStr)
    os.startfile('{}/UnrealEngine/Python'.format(getDocPath()))

def insDeadline():
    modify_Deadline_config()
    import win32con, win32gui
    lprint(LM.deadline_clientDir)
    os.system(fr"echo D| xcopy A:\TD\dccData\ThinkBox\Deadline_Client "+
      f"{LM.deadline_clientDir} /Y /E /d")
    os.system("cmdkey /add:192.168.110.60 /user:OC\Administrator /pass:OC.123456")
    os.startfile(fr"{LM.deadline_clientDir}/bin/deadlinemonitor.exe")
    # response = win32gui.MessageBox(0, "D:\Program Files\Thinkbox文件夹已存在,是否覆盖", "Confirm", win32con.MB_YESNO | win32con.MB_ICONWARNING)
    # if response == win32con.IDYES:
    #     os.system(f'echo D| xcopy {Lugwit_publicPath}\DCCSoftware\Thinkbox  "D:\Program Files\Thinkbox" /Y /E /d')
    # else:
    #     print("不复制文件")
    
def copyPerforceAndDeadline():
    if not ENABLE_PERFORCE:
        return
    print ('复制Deadline和Perforce')
    import win32con, win32gui
    # os.system('mkdir "D:\Program Files"')
    # if os.path.exists("D:\Program Files\Thinkbox"):
    #     response = win32gui.MessageBox(0, "D:\Program Files\Thinkbox文件夹已存在,是否覆盖", "Confirm", win32con.MB_YESNO | win32con.MB_ICONWARNING)
    #     if response == win32con.IDYES:
    #         os.system(f'echo D| xcopy {Lugwit_publicPath}\DCCSoftware\Thinkbox  "D:\Program Files\Thinkbox" /Y /E /d')
    #     else:
    #         print("不复制文件")
    # else:
    #     print ('复制Deadline')
    #     os.system(f'echo D| xcopy {Lugwit_publicPath}\DCCSoftware\Thinkbox  "D:\Program Files\Thinkbox" /Y /E /d')
    PerforceInsDir=f'{TD_DepotDir}/Software/ProgramFiles/Perforce'
    if os.path.exists(PerforceInsDir):
        response = win32gui.MessageBox(0, f"{PerforceInsDir}已存在是否覆盖", 
                                       "Confirm", 
                                       win32con.MB_YESNO | win32con.MB_ICONWARNING)
        if response == win32con.IDYES:
            os.system(f'echo D| xcopy {Lugwit_publicPath}\DCCSoftware\Perforce  "D:\Program Files\Perforce" /Y /E /d')
        else:
            print("不复制文件")
    else:
        os.system(f'echo D| xcopy {Lugwit_publicPath}\DCCSoftware\Perforce  "D:\Program Files\Perforce" /Y /E /d')
    
# copyPerforceAndDeadline()
# sys.exit()

def insP4AndDownloadData():
    if not ENABLE_PERFORCE:
        return
    copyPerforceAndDeadline()
    p4=loginP4.p4_login(port="192.168.110.61:1666",userName=userName)
    print ("旧的工作区",p4_baselib.getOldClient(p4,userName=userName))
    if not p4_baselib.getOldClient(p4,userName=userName):
        print ("创建工作区")
        p4_baselib.createWorkSpace(p4,userName=userName,workSpacePath='D:/TD_Depot',
                                   client_options=["noclobber","nomodtime",'noallwrite'],
                                   client_views=[r"//TD_Depot/... //{Client}/... "],
                                   workName=userName+'_'+hostName+'_plug')
    #setEnvVariable()
    os.system(fr'cmd/k {Lugwit_publicPath}/Python\PyFile\syncPlugLib\update.bat')

# insP4AndDownloadData()
# sys.exit()

def execfile(filepath, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with codecs.open(filepath, 'r',encoding='utf8') as file:
        exec(file.read(), globals, locals)

# 使用这个函数



def copyProgramFilesLocal():
    execfile(r'A:\TD\Python\PyFile\syncNonServerFileToLocal.py')
    cmd = fr'&cmd/c  robocopy {LM.PythonLibDir_Public}\Python310 d:\TD_Depot\plug_in\Python\Python310 /E /MIR /XD __pycache__ build & echo 复制完成' 
    cmd += fr'echo D|xcopy/y/e/r/d A:\TD\Python\Python27 D:\TD_Depot\plug_in\Python\Python27'

    print ('cmd' , cmd)
    os.system(cmd)
# copyProgramFilesLocal()
# os._exit(0)

def createShortCut(exe_path, shortcut_path, name, icon_path='', arguments=''):
    """创建 Windows 快捷方式，失败时自动降级重试。"""
    import os
    import traceback
    import winshell

    def _normalize_icon(icon_value):
        if not icon_value:
            return None
        if isinstance(icon_value, (tuple, list)) and len(icon_value) >= 1:
            icon_file = str(icon_value[0])
            icon_index = int(icon_value[1]) if len(icon_value) > 1 else 0
            return (icon_file, icon_index)
        return (str(icon_value), 0)

    def _write_shortcut(icon_value):
        shortcut = winshell.shortcut(shortcut_path)
        shortcut.name = name
        shortcut.path = exe_path
        shortcut.working_directory = os.path.dirname(exe_path)
        if arguments:
            shortcut.arguments = arguments
        if icon_value:
            shortcut.icon_location = icon_value
        shortcut.write(shortcut_path)

    try:
        shortcut_dir = os.path.dirname(shortcut_path)
        if not os.path.exists(shortcut_dir):
            os.makedirs(shortcut_dir, exist_ok=True)
            print(f'创建目录: {shortcut_dir}')

        normalized_icon = _normalize_icon(icon_path)
        try:
            _write_shortcut(normalized_icon)
        except Exception as first_exc:
            # 常见 COM 未指定错误时，去掉 icon 再写一次，避免整个启动流程中断。
            print(f"创建快捷方式首次失败(带图标): {first_exc}，尝试无图标重试")
            _write_shortcut(None)

        print('创建快捷方式{}'.format(shortcut_path))
    except Exception as e:
        print(f"创建快捷方式失败,原因是{e}")
        print(traceback.format_exc())


def setBoot():
    pyfile=fr'{LugwitToolDir}\src\setBoot.py'
    pyexe=sys.executable
    """检查是否需要更新快捷方式"""
    userDir=os.path.expandvars("%USERPROFILE%")
    StartUp_shortcut = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\0lugwit_insapp.lnk'
    Programs_shortcut=fr'{userDir}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\0lugwit_insapp.lnk'

    # 检查文件是否存在
    if not os.path.exists(StartUp_shortcut):
        print(f"StartUp快捷方式不存在: {StartUp_shortcut}，需要创建")
        l_admin.runAsAdmin(pyexe,pyfile)
        return
    
    if not os.path.exists(Programs_shortcut):
        print(f"Programs快捷方式不存在: {Programs_shortcut}，需要创建")
        l_admin.runAsAdmin(pyexe,pyfile)
        return
    
    # 比较修改时间
    startup_mtime = os.path.getmtime(StartUp_shortcut)
    programs_mtime = os.path.getmtime(Programs_shortcut)
    
    print("StartUp快捷方式修改时间:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(startup_mtime)))
    print("Programs快捷方式修改时间:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(programs_mtime)))
    
    if programs_mtime != startup_mtime:
        print("快捷方式修改时间不一致，需要更新")
        l_admin.runAsAdmin(pyexe,pyfile)


def insHoudiniPlug():
    os.system(fr'setx HOUDINI_PACKAGE_DIR {LugwitHoudiniPlugPath}\\packages')
    
        
def installP4Tool(*args):   
    if not ENABLE_PERFORCE:
        return
    pathA=Lugwit_publicPath+r'\DCCSoftware\ProgramFilesLocal\perforce\Config\customtools.xml'
    pathB='{}\\.p4qt\\customtools.xml'.format(USERPROFILE)
    # copyStr=f'echo F| Xcopy {pathA} {pathB} /Y /R'
    # print ('copyStr',copyStr)
    # shutil.copyfile(r'A:\TD\Lugwit_syncPlug\lugwit_insapp\python_env\python_p4.exe',
    #                 r"D:\TD_Depot\Software\Lugwit_syncPlug\lugwit_insapp\python_env\python_p4.exe")
    os.system(r'echo F|xcopy A:\TD\Lugwit_syncPlug\lugwit_insapp\python_env\python_p4.exe '+
              'D:\TD_Depot\Software\Lugwit_syncPlug\lugwit_insapp\python_env\python_p4.exe')
    os.system(fr'echo F|xcopy /y/r {pathA} {pathB}')

    
    lockhunter_insdir_pub=LM.ProgramFilesLocal_Public+'/LockHunter'
    lockhunter_insdir=LM.ProgramFilesLocal+'/LockHunter'
    # shutil.copyfile()
    os.system(r'cmd/c echo F| xcopy/y/e/r/d A:\TD\DCCSoftware\右键菜单.reg D:\TD_Depot\右键菜单.reg')
    os.startfile(r'D:\TD_Depot\右键菜单.reg')

    cmd = ['cmd/c echo D|','xcopy',  r'/y/e/r/d', 
        r'A:\TD\Lugwit_syncPlug\lugwit_insapp\python_env\Lib\site-packages\qtpy', 
        r'D:\TD_Depot\Software\Lugwit_syncPlug\lugwit_insapp\python_env\Lib\site-packages\qtpy']
    cmd = ' '.join(cmd)
    print (cmd)
    subprocess.run(
        cmd,
        shell=True,

    )


    # 复制 pywinauto 目录
    print ("复制 pywinauto 目录")
    cmd = ['cmd/c echo D|','xcopy',  r'/y/e/r/d', 
        r'A:\TD\Lugwit_syncPlug\lugwit_insapp\python_env\Lib\site-packages\pywinauto', 
        r'D:\TD_Depot\Software\Lugwit_syncPlug\lugwit_insapp\python_env\Lib\site-packages\pywinauto']
    cmd = ' '.join(cmd)
    print (cmd)
    subprocess.run(
        cmd,
        shell=True,

    )
            
    # showMessage_ps.showMessageWin(title='安装P4V工具',
    #             iconPath=LM.LugwitToolDir+'\\icons\\p4v.ico',         
    #             text=f"p4v工具安装成功,安装文件\n{pathB}")
                    
    

    # os.system(copyStr)
    # os.startfile(os.path.dirname(pathB))

# installP4Tool()
# os._exit(0)
def insRightMenu():
    os.system(fr'echo F| xcopy A:\TD\安装步骤\右键菜单.reg %TEMP%\Lugwit_右键菜单.reg /Y /R')
    os.system(fr'cmd /c regedit.exe/s %TEMP%\Lugwit_右键菜单.reg')
    # showMessage_ps.showMessageWin(title='添加路径环境变量',
    #             iconPath=LM.LugwitToolDir+'\\icons\\p4v.ico',         
    #             text=r"请把Maya安装目录添加到路径环境变量,比如\n"+
    #             'C:\\Program Files\\Autodesk\\Maya2018\\bin\n'+
    #             "Maya文件上后右键菜单>CG资产处理>导出Tpose就可以导出TposeFbx文件了")
    
# insRightMenu()
# os._exit(0)

# os._exit(0)
def insAbcViewer():
    os.startfile(r'A:\TD\安装步骤\MayaToUE插件安装\安装Abc查看器.bat')

    # showMessage_ps.showMessageWin(title='添加路径环境变量',
    #             iconPath=LM.LugwitToolDir+'\\icons\\p4v.ico',         
    #             text=r"请把Maya安装目录添加到路径环境变量,比如\n"+
    #             'C:\\Program Files\\Autodesk\\Maya2018\\bin\n'+
    #             "Maya文件上后右键菜单>CG资产处理>导出Tpose就可以导出TposeFbx文件了")
    
# insRightMenu()
# os._exit(0)
    
def insPlug():
    p4_baselib.createWorkSpace()
    p4_baselib.deleteOldClient()
    modify_Deadline_config()

    
def updateNukePlug():
    """更新Nuke插件，提供完全更新或增量更新选项"""
    import win32con, win32gui
    
    # 显示更新方式选择弹窗
    response = win32gui.MessageBox(
        0, 
        u"请选择Nuke插件更新方式：\n\n是(Y) - 完全更新（重新安装所有插件文件）\n否(N) - 增量更新（只更新修改的文件）\n取消 - 取消更新", 
        u"Nuke插件更新选择", 
        win32con.MB_YESNOCANCEL | win32con.MB_ICONQUESTION
    )
    
    if response == win32con.IDCANCEL:
        print(u"用户取消了Nuke插件更新")
        return
    elif response == win32con.IDYES:
        # 完全更新
        print(u"执行完全更新...")
        _performFullNukeUpdate()
    elif response == win32con.IDNO:
        # 增量更新
        print(u"执行增量更新...")
        _performIncrementalNukeUpdate()

def _performFullNukeUpdate():
    """执行完全更新"""
    try:
        print(u"开始执行Nuke插件完全更新...")
        # 执行原有的安装脚本
        os.startfile(LM.Lugwit_publicPath+r'\安装步骤\安装nuke插件_全新安装.bat')       
    except Exception as e:
        print(u"完全更新过程中出现错误:", str(e))
        print(traceback.format_exc())

def _performIncrementalNukeUpdate():
    """执行增量更新"""
    try:
        print(u"开始执行Nuke插件完全更新...")
        # 执行原有的安装脚本
        os.startfile(LM.Lugwit_publicPath+r'\安装步骤\安装nuke插件_增量更新.bat')       
    except Exception as e:
        print(u"完全更新过程中出现错误:", str(e))
        print(traceback.format_exc())


@LM.try_exp
def startP4V(type: Literal['project', 'plug'] = 'project'):
    if not ENABLE_PERFORCE:
        return
    with codecs.open(LM.oriEnvVarFile,'r',encoding='utf8') as f:
            oriEnvVar=json.load(f)
    
    
    customtools= (r'A:\TD\DCCSoftware\ProgramFilesLocal\Perforce\Config\customtools.xml',
         os.path.expandvars(r'%USERPROFILE%\.p4qt\customtools.xml'))
    def safe_copy(src, dst):
        """安全复制文件，遇到权限问题跳过"""
        try:
            if os.path.isfile(src):
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
            else:
                cmd = f'cmd/c echo D| xcopy /y/e/r/d "{src}" "{dst}"'
                subprocess.run(cmd, shell=True, stderr=subprocess.DEVNULL)
        except (PermissionError, OSError) as e:
            print(f"跳过复制 {src} 到 {dst}: {str(e)}")
        except Exception as e:
            print(f"复制 {src} 到 {dst} 时出错: {str(e)}")
    if LM.hostName not in ['DESKTOP-LDSM1H1','TD','PC-20240202CTEU']:
        safe_copy(*customtools)
            
            
    oriEnvVar['PATH']+=fr';{LM.LugwitAppDir}\python_env;{LM.perforceInsDir}'
    p4v_windows = find_all_p4v_windows()
    from lperforce.P4LoginInfoModule import p4_loginInfo
    port = p4_loginInfo[type]['port']
    for p4v_window in p4v_windows:
        hwnd = p4v_window.hwnd
        if port in p4v_window.title:
            # 最大化现有的p4v窗口
            lprint(f"找到已存在的P4V窗口: {p4v_window.title}，最大化显示")
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)  # 最大化窗口
            win32gui.SetForegroundWindow(hwnd)  # 将窗口设置为前台窗口
            return
    args=[LM.perforceInsDir+r'\p4v.exe',
            f"-p {p4_loginInfo[type]['port']}",
            f"-u {p4_loginInfo[type]['User']}",
            f"-c {p4_loginInfo[type]['clientName']}",
            f"-C utf8"]
    cmd = ' '.join(args)
    lprint (cmd)
    # 执行命令
    subprocess.Popen(cmd, shell=True,env=oriEnvVar)

# 为了保持向后兼容性，提供原来的函数
def startP4V_H_Project():
    print(111)
    startP4V('project')
    
def startP4V_Plug():
    startP4V('plug')






# startP4V_H_Project()
# sys.exit()
if __name__=='__main__':
    # updateNukePlug()
    # sys.exit()
    try:
        print(u'执行函数exec func ->:{}\n'.format(sys.argv[1]))
        exStr=sys.argv[1]
        if not exStr.endswith(')'):
            exStr+='()'
        print (u'系统变量 sys_argv->:{}\n'.format(sys.argv))

        print('\n')
        exec (exStr)
    except Exception as ex:
        print(traceback.format_exc())
        print ('run_{}'.format(__file__))
        time.sleep(100)
        pass

