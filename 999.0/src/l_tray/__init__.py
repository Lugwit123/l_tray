# -*- coding: utf-8 -*-

# Perforce 功能总开关，设为 False 关闭所有 P4 相关功能
ENABLE_PERFORCE = False

from .Tray import TrayIcon

__version__ = "1.0.0"
__all__ = ["TrayIcon", "ENABLE_PERFORCE"]
