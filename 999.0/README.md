# l_tray - Simple PySide6 System Tray

简洁的 PySide6 系统托盘应用包

## 功能

- 系统托盘图标
- 右键菜单
- 托盘通知
- 简洁的 API

## 使用示例

```python
from l_tray import TrayApp

# 创建托盘应用
tray = TrayApp(title="我的应用", icon_path="icon.png")

# 添加菜单项
tray.add_action("显示消息", lambda: tray.show_message("标题", "消息内容"))
tray.add_separator()

# 运行
tray.run()
```

## API

### TrayApp(title, icon_path=None)
创建托盘应用

### add_action(text, callback)
添加菜单项

### add_separator()
添加分隔线

### show_message(title, message, icon)
显示托盘通知

### quit()
退出应用

### run()
运行事件循环
