# -*- coding: utf-8 -*-

name = "l_tray"
version = "999.0"
description = "Lugwit Tray Application"
authors = ["Lugwit Team"]

requires = ["python-3.12+<3.13", "lperforce", "lugwit_env", "L_Tools", "l_scheduler",
            "pyside6", "pywin32", "psutil"]

def commands():
    env.PYTHONPATH.append('{root}/src')
    env.L_TRAY_ROOT = '{root}'
    
    # Command alias - start the full tray application
    alias('start_tray', 'python {root}/src/l_tray/plugSync.py')

build_command = False
cachable = True
relocatable = True

