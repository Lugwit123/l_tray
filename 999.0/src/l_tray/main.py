import subprocess,os,sys
import sys,os

sys.path.append(os.path.dirname(__file__)+'\\starter_lib')
import tkinter as tk
import ctypes

# Try to import win32 modules (optional)
try:
    import win32gui
    import win32con
    WIN32_AVAILABLE = True
except ImportError:
    print("Warning: win32gui/win32con not available, some features may be limited")
    WIN32_AVAILABLE = False
    win32gui = None
    win32con = None

sys.path.append(os.path.dirname(__file__)+'\\src')

# def is_admin():
#     try:
#         return ctypes.windll.shell32.IsUserAnAdmin()
#     except:
#         return False

# if not is_admin():
#     ctypes.windll.shell32.ShellExecuteW(
#         None, "runas", sys.executable, " ".join(sys.argv), None, 1
#     )
#     sys.exit(0)

try:
    # Import run_app module from the same package
    from . import run_app
except Exception as e:
    import traceback
    # Get traceback string and escape it
    error_message = traceback.format_exc().replace('"', '`"').replace('\n', '`n')
    
    # PowerShell script to show error message
    ps_script = f'''
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.MessageBox]::Show("{error_message}")
    '''
    
    # Run PowerShell script
    subprocess.run(["powershell", "-Command", ps_script], check=True)



