import sys
import os

# Try to import optional modules
try:
    sys.path.append(r"D:\TD_Depot\Software\Lugwit_syncPlug\lugwit_insapp\trayapp\starter_lib")
except:
    pass

# Try to import win32 modules (optional)
try:
    import win32gui
    import win32con
    import win32process
    from win32con import SWP_NOMOVE, SWP_NOSIZE, SW_HIDE, SW_SHOW, SWP_NOZORDER, SWP_FRAMECHANGED
    WIN32_AVAILABLE = True
    print("win32gui", win32gui)
    print("win32con", win32con)
except ImportError:
    print("Warning: win32 modules not available in console.py")
    WIN32_AVAILABLE = False
    win32gui = None
    win32con = None
    win32process = None
    # Define dummy constants
    SWP_NOMOVE = SWP_NOSIZE = SW_HIDE = SW_SHOW = SWP_NOZORDER = SWP_FRAMECHANGED = 0

# Try to import psutil
try:
    import psutil
except ImportError:
    print("Warning: psutil not available")
    psutil = None

def get_grandparent_window_info():
    """获取祖父进程的窗口句柄和名称（仅适用于 Windows）。"""
    # Check if required modules are available
    if not psutil or not WIN32_AVAILABLE:
        print("Warning: psutil or win32 modules not available, returning None")
        return None, None
    
    try:
        current_process = psutil.Process(os.getpid())
        parent_process = current_process.parent()
        if parent_process:
            grandparent_process = parent_process.parent()
            if grandparent_process:
                grandparent_pid = grandparent_process.pid
                grandparent_name = grandparent_process.name()

                # 获取祖父进程的所有顶级窗口句柄
                def callback(hwnd, hwnds):
                    if win32gui.IsWindowVisible(hwnd) and win32gui.GetParent(hwnd) == 0:
                        _, pid = win32process.GetWindowThreadProcessId(hwnd)
                        if pid == grandparent_pid:
                            hwnds.append(hwnd)
                    return True

                hwnds = []
                win32gui.EnumWindows(callback, hwnds)

                if hwnds:
                    hwnd = hwnds[0]  # 获取第一个顶级窗口句柄
                    return hwnd, grandparent_name
                else:
                    return None, grandparent_name  # 未找到窗口句柄
            else:
                return None, None #未找到祖父进程
        else:
            return None, None #未找到父进程

    except Exception as e:
        print(f"Error in get_grandparent_window_info: {e}")
        return None, None

# hwnd, parent_name = get_grandparent_window_info()
# if hwnd:
#     print(f"父进程名称：{parent_name}, 窗口句柄：{hwnd}")
# elif parent_name:
#     print(f"父进程名称：{parent_name}, 未找到窗口句柄。")
# else:
#     print("无法获取父进程信息。")

def find_window_by_title(titleList=[]):
    if not WIN32_AVAILABLE:
        print("Warning: win32 modules not available")
        return None
    
    print("locals>>>>>>>>>>>>>>>",locals(),titleList)
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd):
            # if isinstance(titleList,list):
            if "管理员: 0lugwit_insapp (Admin)" in win32gui.GetWindowText(hwnd):
                hwnds.append(hwnd)

        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    print("hwnds",hwnds,titleList)
    if hwnds:
        os.environ['tray_hwnd'] = str(hwnds[0])
        return hwnds[0]
    else:
        return None
        
def is_window_visible(hwnd):
    if not WIN32_AVAILABLE:
        return False
    
    # 获取窗口样式
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
    # 检查WS_VISIBLE标志
    return (style & win32con.WS_VISIBLE) != 0

# Name	管理员: 0lugwit_insapp (Admin)

def hide_taskbar_icon(titleList=["管理员: 0lugwit_insapp (Admin)"]):
    if not WIN32_AVAILABLE:
        print("Warning: win32 modules not available, cannot hide taskbar icon")
        return
    
    # 获取控制台窗口句柄
    # 支持尝试过通过cpython的控制台窗口查找窗口句柄的,但是找到的是cmd.exe
    # win11的窗口确实window teriminal,所以放弃了这个办法,改用标题查找

    return
    print("locals",locals())
    if os.getenv("tray_hwnd"):
        hwnd=int(os.getenv("tray_hwnd"))
        print(f"get hwnd from env {hwnd}")
    else:
        hwnd = find_window_by_title(titleList)
    if not hwnd:
        return
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
    is_vis= is_window_visible(hwnd)

    if is_vis:
        style &= ~win32con.WS_VISIBLE
        win32gui.ShowWindow(hwnd, SW_HIDE)
    else:
        style |= win32con.WS_VISIBLE
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        win32gui.SetForegroundWindow(hwnd)
        
    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)
    win32gui.SetWindowPos(hwnd, None, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED);
    win32gui.UpdateWindow(hwnd)
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
    return is_vis



if __name__ == "__main__":
    hide_taskbar_icon()

