# -*- coding: utf-8 -*-
# 从 _config.py 导入全局配置，修改 _config.py 中的值即可控制所有模块的行为
from ._config import ENABLE_PERFORCE

from .Tray import TrayIcon

__version__ = "1.0.0"
__all__ = ["TrayIcon", "ENABLE_PERFORCE"]
