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
    try:
        import win32api
    except ImportError:
        win32api = None
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
    win32api = None
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


def bring_top_level_window_to_front_by_pids(pids):
    """按 PID 列表查找顶层可见窗口并置前（返回 hwnd 或 None）。"""
    if not psutil or not WIN32_AVAILABLE:
        return None
    try:
        want = set(int(x) for x in pids if x is not None)
    except Exception:
        want = set()
    if not want:
        return None

    hwnds = []

    def callback(hwnd, _):
        try:
            # 不要求可见：部分程序“最小化到托盘”时会隐藏窗口，但仍可恢复
            if win32gui.GetParent(hwnd) != 0:
                return True
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            if pid in want:
                hwnds.append(hwnd)
        except Exception:
            pass
        return True

    win32gui.EnumWindows(callback, None)
    if not hwnds:
        return None

    def _safe_get_title(h: int) -> str:
        try:
            return win32gui.GetWindowText(h) or ""
        except Exception:
            return ""

    def _safe_get_class(h: int) -> str:
        try:
            return win32gui.GetClassName(h) or ""
        except Exception:
            return ""

    def _safe_get_style(h: int) -> tuple[int, int]:
        try:
            style = int(win32gui.GetWindowLong(h, win32con.GWL_STYLE))
        except Exception:
            style = 0
        try:
            exstyle = int(win32gui.GetWindowLong(h, win32con.GWL_EXSTYLE))
        except Exception:
            exstyle = 0
        return style, exstyle

    def _is_bad_candidate(h: int) -> bool:
        title = _safe_get_title(h).strip().lower()
        cls = _safe_get_class(h).strip()
        if title in {"pythonw", "python", "cmd.exe", "powershell"}:
            return True
        if cls in {"ConsoleWindowClass"}:
            return True
        # 典型“工具窗口/不可任务栏窗口”往往不是主界面
        _, exstyle = _safe_get_style(h)
        try:
            if exstyle & getattr(win32con, "WS_EX_TOOLWINDOW", 0):
                return True
        except Exception:
            pass
        return False

    def _score(hwnd: int) -> tuple[int, int, int, int, int]:
        """优先选择“更像主窗口”的 hwnd。分数越大越优先。"""
        title = _safe_get_title(hwnd)
        try:
            vis = 1 if win32gui.IsWindowVisible(hwnd) else 0
        except Exception:
            vis = 0
        try:
            iconic = 1 if win32gui.IsIconic(hwnd) else 0
        except Exception:
            iconic = 0
        style, exstyle = _safe_get_style(hwnd)
        has_title = 1 if title.strip() else 0
        title_len = min(len(title.strip()), 200)
        appwindow = 1 if (exstyle & getattr(win32con, "WS_EX_APPWINDOW", 0)) else 0
        toolwindow = 1 if (exstyle & getattr(win32con, "WS_EX_TOOLWINDOW", 0)) else 0
        disabled = 1 if (style & getattr(win32con, "WS_DISABLED", 0)) else 0
        # 评分策略：
        # - 非空标题、标题更长、可见、可 restore 的最小化窗口优先
        # - WS_EX_APPWINDOW 优先
        # - WS_EX_TOOLWINDOW / WS_DISABLED 降权
        return (
            has_title,
            title_len,
            vis,
            iconic,
            appwindow - toolwindow - disabled,
        )

    good = [h for h in hwnds if not _is_bad_candidate(h)]
    pick_pool = good if good else hwnds
    hwnd = sorted(pick_pool, key=_score, reverse=True)[0]

    def _force_show_foreground(target_hwnd: int) -> None:
        # 1) 尝试还原/显示
        for cmd in (getattr(win32con, "SW_RESTORE", 9), getattr(win32con, "SW_SHOW", 5)):
            try:
                win32gui.ShowWindow(target_hwnd, cmd)
            except Exception:
                pass
        # 2) 利用“topmost 切换”强制 Z-Order 刷新（很多情况下比单纯 SetForeground 更稳）
        try:
            win32gui.SetWindowPos(
                target_hwnd,
                getattr(win32con, "HWND_TOPMOST", -1),
                0,
                0,
                0,
                0,
                SWP_NOMOVE | SWP_NOSIZE,
            )
            win32gui.SetWindowPos(
                target_hwnd,
                getattr(win32con, "HWND_NOTOPMOST", -2),
                0,
                0,
                0,
                0,
                SWP_NOMOVE | SWP_NOSIZE,
            )
        except Exception:
            pass
        # 3) BringWindowToTop / SetForegroundWindow（可能被系统限制）
        try:
            win32gui.BringWindowToTop(target_hwnd)
        except Exception:
            pass
        try:
            win32gui.SetForegroundWindow(target_hwnd)
        except Exception:
            pass
        # 4) 前台限制兜底：AttachThreadInput 把前台线程输入附加到当前线程
        try:
            if win32api is not None:
                fg = win32gui.GetForegroundWindow()
                fg_tid, _ = win32process.GetWindowThreadProcessId(fg)
                tgt_tid, _ = win32process.GetWindowThreadProcessId(target_hwnd)
                cur_tid = win32api.GetCurrentThreadId()
                # 附加当前线程到前台线程与目标线程，再尝试激活
                win32api.AttachThreadInput(cur_tid, fg_tid, True)
                win32api.AttachThreadInput(cur_tid, tgt_tid, True)
                try:
                    win32gui.SetForegroundWindow(target_hwnd)
                    win32gui.SetActiveWindow(target_hwnd)
                    win32gui.SetFocus(target_hwnd)
                finally:
                    win32api.AttachThreadInput(cur_tid, tgt_tid, False)
                    win32api.AttachThreadInput(cur_tid, fg_tid, False)
        except Exception:
            pass

    _force_show_foreground(hwnd)
    return hwnd
        
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

