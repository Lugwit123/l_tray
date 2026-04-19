 
import os
import shutil
import time
import subprocess

userDir=os.path.expandvars("%USERPROFILE%")
StartUp_shortcut = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\0lugwit_insapp.lnk'
Programs_shortcut=fr'{userDir}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\0lugwit_insapp.lnk'


def need_update():
    """检查是否需要更新快捷方式"""
    if any(not os.path.exists(shortcut) for shortcut in [StartUp_shortcut, Programs_shortcut]):
        return True

        
    # 比较修改时间
    startup_mtime = os.path.getmtime(StartUp_shortcut)
    programs_mtime = os.path.getmtime(Programs_shortcut)
    
    print("StartUp快捷方式修改时间:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(startup_mtime)))
    print("Programs快捷方式修改时间:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(programs_mtime)))
    
    return programs_mtime != startup_mtime

if need_update():
    print("检测到Programs快捷方式有更新，正在复制...")
    cmd = fr'echo F| xcopy "{Programs_shortcut}" "{StartUp_shortcut}" /y/r'
    subprocess.run(cmd, shell=True)
else:
    print("无需更新StartUp快捷方式")





 
# # 将快捷方式添加到自启动目录
# ## #获取用户名
# username = getpass.getuser()
# ## 系统盘符名称
# syspath = os.getenv("SystemDrive")
# ## 自启动目录
# startupPath = os.path.join(os.getenv("SystemDrive"),r"\users",getpass.getuser(),r"AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup")
# bin_path = r"main_logic.exe"
# link_path = startupPath + "\\main_logic"
# desc = "喝水提醒小工具"
# create_shortcut(bin_path, link_path, desc)