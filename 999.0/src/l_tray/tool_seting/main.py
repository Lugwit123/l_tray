# coding:utf-8
import winreg,os,sys,traceback,winshell
import win32com.client,shutil

LugwitToolDir = os.environ.get('LugwitToolDir')
sys.path.append(LugwitToolDir+'/Lib')

import Lugwit_Module as LM
toolSettingUIFile="pyqt_ui_file\工具设置.ui"