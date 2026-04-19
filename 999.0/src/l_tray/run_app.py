#lugwitSyncApp.py
from . import console
import sys
import ctypes
import os
print("ctypes",ctypes)

# Try to import optional modules (use dynamic paths)
try:
    # Get the package directory dynamically
    package_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    lib_dir = os.path.join(package_dir, 'Lib')
    uiLib_dir = os.path.join(lib_dir, 'Lugwit_Module', 'l_src', 'UILib')
    
    if os.path.exists(uiLib_dir):
        sys.path.append(uiLib_dir)
    if os.path.exists(lib_dir):
        sys.path.append(lib_dir)
    
    import toggle_ui_visable
except ImportError:
    print("Warning: toggle_ui_visable not available")
    toggle_ui_visable = None
# 定义 SetConsoleTitle 函数
SetConsoleTitle = ctypes.windll.kernel32.SetConsoleTitleW

# 设置窗口标题
SetConsoleTitle("0lugwit_insapp")



titleList=[u"管理员: 0lugwit_insapp (Admin)",u"0lugwit_insapp"]
hwnd, parent_name = console.get_grandparent_window_info()
vis = console.is_window_visible(hwnd)
print ( 'vis',vis)
os.environ['comenu_hwnd']=str(hwnd)

# Toggle window visibility if toggle_ui_visable is available
if toggle_ui_visable:
    hwnd = toggle_ui_visable.toggle_win_vis_by_hwnd(hwnd)
    vis = console.is_window_visible(hwnd)
    print ( 'vis',vis)
else:
    print("Warning: toggle_ui_visable not available, skipping window visibility toggle")

import sys,os,subprocess,codecs,re,json,time
curDir=os.path.dirname(os.path.abspath(__file__))

# Use plugSync.py from the current package directory
plugsync_path = os.path.join(curDir, 'plugSync.py')

# Try to get LugwitToolDir for backward compatibility
try:
    LugwitToolDir=re.search('.+trayapp',__file__).group()
    python_envDir=os.path.dirname(LugwitToolDir)+'\\python_env'
except:
    # If pattern doesn't match (e.g., in Rez package), use fallback
    LugwitToolDir = curDir
    python_envDir = os.path.join(os.path.dirname(os.path.dirname(LugwitToolDir)), 'python_env')


# 构建 PowerShell 命令
command = 'powershell -Command "[Environment]::GetFolderPath(\'MyDocuments\')"'

# 执行命令并捕获输出
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
stdout, stderr = process.communicate()

# stdout 包含命令的输出，这里是“我的文档”目录的路径
if process.returncode == 0:
    print("我的文档目录：", stdout.strip())
    
    documentsPath= stdout.strip()
else:
    print("命令执行出错：", stderr)

user_home = os.path.expandvars("%USERPROFILE%")

oriEnvVarFile=os.path.expandvars("%USERPROFILE%")+r'/.Lugwit/config/oriEnvVar.json'
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
    # 判断目录是否不在sys_executable_dir中
    # if userName == 'qqfeng':
    #     with open('D:/aa.txt','a+') as f:
    #         f.write(f'{sys_executable_dir} {x}  {sys_executable_dir not in x}\n')
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



# os.system('taskkill /F /IM lugwit_pythonw.exe')

def get_fqdn():
    try:
        # 获取主机名
        hostname = subprocess.check_output("hostname", shell=True).decode().strip()

        # 使用 nslookup 获取完整设备名称
        nslookup_result = subprocess.check_output(f"chcp 65001 > nul & nslookup {hostname}", shell=True).decode('utf-8', errors='ignore')

        # 解析 nslookup 的结果以获取 FQDN
        fqdn = None
        for line in nslookup_result.split("\n"):
            if "Name:" in line:
                fqdn = line.split(":")[1].strip()
                break

        if fqdn:
            return fqdn
        else:
            return "获取设备全名失败"
    except subprocess.CalledProcessError as e:
        return f"命令执行失败: {e}"
    except UnicodeDecodeError as e:
        return f"解码错误: {e}"

print ("映射A盘");print (os.path.exists('A:/temp/61.txt'))
if not os.path.exists('A:/temp/61.txt'):
    if os.path.exists('A:'):
        os.system('net use A: /delete /y')
    # if not get_fqdn().endswith('.oc.com'):
    #     os.system('cmdkey /add:192.168.110.61 /user:OC\\OC2 /pass:%OC.123456')
    if not os.path.exists('A:'):
        # /savecred 因为已经添加了凭据,再次添加会冲突
        subprocess.Popen(r"cmd /c start cmd /c echo 命令行映射A盘 & net use A: \\192.168.110.61\A  /persistent:yes",shell=True)
        time.sleep(2)



# Use plugSync.py from the package if it exists, otherwise use external path
if os.path.exists(plugsync_path):
    cmd=f'{python_envDir}/lugwit_python.exe {plugsync_path}'
    print(f"Using plugSync.py from package: {plugsync_path}")
else:
    cmd=f'{python_envDir}/lugwit_python.exe {LugwitToolDir}/src/plugSync.py'
    print(f"Using plugSync.py from external path: {LugwitToolDir}/src/plugSync.py")
# 获取当前进程的PID
current_pid = os.getpid()
env=os.environ.copy()
env['parentProcID']=str(current_pid)
print ('cmd,\n',cmd)
print ('os.getcwd,\n',os.getcwd())

# Use dynamic path instead of hardcoded absolute path
PYTHON_PATH = os.path.join(LugwitToolDir, 'Lib')
print(os.environ.get("PYTHONPATH",'.'))
get_PYTHONPATH= os.environ.get("PYTHONPATH",'')
print("从已有环境获取的PYTHONPATH",get_PYTHONPATH)

# Create PYTHON_PATH if it doesn't exist
if not os.path.exists(PYTHON_PATH):
    try:
        os.makedirs(PYTHON_PATH,exist_ok=True)
    except Exception as e:
        print("创建目录失败:", e)

# Check if PYTHON_PATH is already in PYTHONPATH
pythonpath_list = [p.strip() for p in get_PYTHONPATH.split(';') if p.strip()]
path_already_set = False
try:
    for p in pythonpath_list:
        if os.path.exists(p) and os.path.exists(PYTHON_PATH):
            if os.path.samefile(p, PYTHON_PATH):
                path_already_set = True
                break
except Exception as e:
    print(f"Warning: Error checking PYTHONPATH: {e}")

if not path_already_set:
    print(f"Setting PYTHONPATH to: {PYTHON_PATH}")
    os.system(u'setx {} {}'.format("PYTHONPATH",PYTHON_PATH))
    
# env.update({'PYTHONHOME':python_envDir,
#           'PYTHONPATH':python_envDir+r'\Lib'})
env['PATH'] = python_envDir+os.pathsep+\
        os.path.join(python_envDir, 'Scripts') + os.pathsep + env['PATH']
proc = subprocess.Popen(cmd,
                      env=env,
                      )
console.hide_taskbar_icon()
print ('cmd',cmd)
proc.wait()



if proc.returncode != 0:
    hwnd = console.find_window_by_title(titleList)
    vis = console.is_window_visible(hwnd)
    print (f'窗口是否可见{vis}')
    while not console.is_window_visible(hwnd):
        time.sleep(0.1)
        console.hide_taskbar_icon()
        time.sleep(0.1)
    ps_script = f'''
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.MessageBox]::Show("程序崩溃,控制台窗口显示,请发送控制台截图给开发人员，")
    '''
    
    # 在Python中运行PowerShell脚本
    subprocess.run(["powershell", "-ExecutionPolicy", 
                    "Bypass", "-Command", ps_script], check=True)


