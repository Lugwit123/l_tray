# -*- coding: utf-8 -*-
"""l_tray 使用示例"""

import sys
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent / "src"))

from l_tray import TrayApp


def main():
    """Run example tray application"""
    # Get icon path
    icon_path = Path(__file__).parent / "src" / "l_tray" / "icons" / "tray_icon.svg"
    
    # Create tray application
    tray = TrayApp(title="Lugwit 托盘示例", icon_path=str(icon_path))
    
    # 添加菜单项
    tray.add_action("显示消息", lambda: tray.show_message("提示", "这是一条测试消息"))
    tray.add_action("显示警告", lambda: tray.show_message("警告", "这是一条警告消息", tray.tray.Warning))
    tray.add_separator()
    
    # 运行应用
    print("托盘应用已启动，右键点击托盘图标查看菜单")
    tray.run()


if __name__ == "__main__":
    main()
