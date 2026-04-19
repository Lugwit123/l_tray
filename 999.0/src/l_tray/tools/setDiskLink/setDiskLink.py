import sys
import re
import os
import json
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QComboBox, QMessageBox, QLabel, QLineEdit, QHBoxLayout
)
from PyQt5 import uic

curDir=os.path.dirname(__file__)
# 添加 src 目录到 sys.path，以便导入 tool_env
src_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, src_dir)
from tool_env import *
sys.path.insert(0,LugwitToolDir+'/Lib')

# 导入 Lugwit_Module 并获取路径变量
import Lugwit_Module as LM
from Lugwit_Module import lprint
from Lugwit_Module.l_src import l_admin

# 获取 Lugwit_Module 中的路径变量
LugwitToolDir = LM.LugwitToolDir if hasattr(LM, 'LugwitToolDir') else LugwitToolDir
Lugwit_publicPath = getattr(LM, 'Lugwit_publicPath', None)
LugwitPath = getattr(LM, 'LugwitPath', None)
plugDataDir_user = getattr(LM, 'plugDataDir_user', None)
TD_DepotDir = getattr(LM, 'TD_DepotDir', None)

diskLinkFile=f"{LugwitToolDir}/data/diskLink.json"

# ==================== 工具函数 ====================
def load_qss_style():
    """加载QSS样式文件"""
    qss_path = os.path.join(LM.LugwitToolDir, 'src', 'qss_style', 'setDiskLink.qss')
    if os.path.exists(qss_path):
        with open(qss_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        print(f"QSS文件未找到: {qss_path}")
        return ""

# ==================== LinkFormRow 类：单行表单 ====================
class LinkFormRow(QWidget):
    def __init__(self, parent_app=None):
        super(LinkFormRow, self).__init__()
        # 加载 .ui 文件
        ui_file_path = os.path.join(os.path.dirname(__file__), 'setDiskLink.ui')
        uic.loadUi(ui_file_path, self)
        self.setFixedHeight(60)
        
        # 存储父窗口引用
        self.parent_app = parent_app
        
        # 绑定事件
        self.swapBtn.clicked.connect(self.swapSourceTarget)
        self.sourceLink.textChanged.connect(self.updateStatus)
        self.targetLink.textChanged.connect(self.updateStatus)
        self.createLinkBtn.clicked.connect(self.onCreateButtonClicked)
        self.updateStatus()

    def set_parent_app(self, app):
        self.parent_app = app

    def onCreateButtonClicked(self):
        """单行创建按钮点击事件"""
        if self.parent_app:
            link_type = self.parent_app.link_type_combo.currentIndex()
            self.createSingleLink(link_type)

    def swapSourceTarget(self):
        """交换源和目标路径"""
        src = self.sourceLink.text()
        tgt = self.targetLink.text()
        self.sourceLink.setText(tgt)
        self.targetLink.setText(src)

    def _update_status_label(self, label, path_exists):
        """更新状态标签的显示和样式"""
        if path_exists:
            label.setText('✔')
            label.setProperty('status', 'success')
            label.setStyleSheet('color: #4caf50; font-family: "Segoe UI Symbol"; font-size: 14pt; font-weight: bold;')
        else:
            label.setText('✘')
            label.setProperty('status', 'error')
            label.setStyleSheet('color: #f44336; font-family: "Segoe UI Symbol"; font-size: 14pt; font-weight: bold;')
    
    def updateStatus(self):
        """更新源和目标路径的状态显示"""
        src = self.sourceLink.text()
        tgt = self.targetLink.text()
        self._update_status_label(self.sourceStatus, os.path.exists(src))
        self._update_status_label(self.targetStatus, os.path.exists(tgt))

    def createSingleLink(self, link_type):
        """创建单个链接
        Args:
            link_type: 0=软链接(symlink), 1=目录联接(Junction)
        """
        source_link = self.sourceLink.text()
        target_link = self.targetLink.text()
        
        try:
            if os.path.exists(target_link) or os.path.islink(target_link):
                QMessageBox.warning(self, "创建失败", f"目标已存在: {target_link}")
                return
            
            if link_type == 0:
                os.symlink(source_link, target_link, target_is_directory=True)
            else:
                cmd = f'cmd.exe /c mklink /J "{target_link}" "{source_link}"'
                subprocess.check_call(cmd, shell=True)
            
            QMessageBox.information(
                self, "创建成功",
                f"链接创建成功！\n源: {source_link}\n目标: {target_link}"
            )
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "创建失败", f"创建链接失败：{e}")
        except OSError as e:
            QMessageBox.critical(self, "创建失败", f"创建链接失败：{e}")
        except Exception as e:
            QMessageBox.critical(self, "创建失败", f"创建链接失败：{e}")

# ==================== DiskLinkManagerApp 类：主窗口 ====================
class DiskLinkManagerApp(QWidget):
    def __init__(self, parent=None):
        super(DiskLinkManagerApp, self).__init__(parent)
        self.top_layout = QVBoxLayout()
        self.forms_layout = QVBoxLayout()
        self.top_layout.addLayout(self.forms_layout)
        self.link_form_rows = []
        
        # 加载并应用QSS样式到整个应用程序
        self._apply_qss_style()
        
        # 加载配置文件
        self._load_config()
        
        # 显示配置文件路径
        self._add_config_file_path_display()
        
        # 链接类型选择
        self.link_type_combo = QComboBox()
        self.link_type_combo.addItems(["软链接 (symlink)", "目录联接 (Junction)"])
        self.top_layout.addWidget(self.link_type_combo)
        
        # 初始化表单
        self._init_forms()

        # 操作按钮
        self.create_all_btn = QPushButton('创建链接')
        self.create_all_btn.clicked.connect(self.create_all_links)
        self.top_layout.addWidget(self.create_all_btn)

        self.save_btn = QPushButton('保存设置')
        self.save_btn.clicked.connect(self.save_settings)
        self.top_layout.addWidget(self.save_btn)

        self.setLayout(self.top_layout)
        self._update_window_height()
    
    def _apply_qss_style(self):
        """加载并应用QSS样式到整个应用程序"""
        qss_content = load_qss_style()
        app = QApplication.instance()
        if app and qss_content:
            app.setStyleSheet(qss_content)
    
    def _load_config(self):
        """加载配置文件"""
        try:
            with open(diskLinkFile, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.disk_link_list = data.get("linkList", [])
        except Exception as e:
            lprint(f"加载配置文件失败: {e}")
            self.disk_link_list = []
    
    def _add_config_file_path_display(self):
        """添加配置文件路径显示"""
        disk_link_file_label = QLabel("配置文件路径:")
        disk_link_file_path = QLineEdit()
        disk_link_file_path.setReadOnly(True)
        disk_link_file_path.setText(diskLinkFile)
        disk_link_file_path.setStyleSheet(
            "color: #aaaaaa; background: #2a2a2a; border: 1px solid #444a52; padding: 2px 6px;"
        )
        disk_link_file_layout = QHBoxLayout()
        disk_link_file_layout.addWidget(disk_link_file_label)
        disk_link_file_layout.addWidget(disk_link_file_path)
        self.top_layout.addLayout(disk_link_file_layout)
    
    def _init_forms(self):
        """初始化表单行"""
        if not self.disk_link_list:
            # 如果没有数据，创建一个空行
            first_row = self.add_form_row()
            first_row.addBtn.setText('增加')
            first_row.addBtn.clicked.connect(self.add_form_row)
            return
        
        # 创建第一个表单行（显示"增加"按钮）
        first_row = self.add_form_row()
        first_row.sourceLink.setText(self.parse_var(self.disk_link_list[0][0]))
        first_row.targetLink.setText(self.disk_link_list[0][1])
        first_row.addBtn.setText('增加')
        first_row.addBtn.clicked.connect(self.add_form_row)
        
        # 创建其他表单行（显示"删除"按钮）
        for source, target in self.disk_link_list[1:]:
            row = self.add_form_row()
            row.sourceLink.setText(self.parse_var(source))
            row.targetLink.setText(target)
            row.addBtn.setText('删除')
            row.addBtn.clicked.connect(lambda checked, r=row: self.remove_form_row(r))

    def add_form_row(self):
        """添加新的表单行"""
        form_row = LinkFormRow(self)  # parent_app 已在 __init__ 中设置
        self.link_form_rows.append(form_row)
        self.forms_layout.addWidget(form_row)
        self._update_window_height()
        return form_row

    def remove_form_row(self, form_row):
        """移除表单行"""
        if form_row in self.link_form_rows:
            self.forms_layout.removeWidget(form_row)
            form_row.deleteLater()
            self.link_form_rows.remove(form_row)
            self._update_window_height()
    
    def _update_window_height(self):
        """更新窗口高度"""
        base_height = 200
        row_height = 60
        self.setMinimumHeight(base_height + row_height * len(self.link_form_rows))
    
    def parse_var(self, var_str):
        """解析变量字符串，替换环境变量
        Args:
            var_str: 包含 $VAR 格式的字符串
        Returns:
            替换后的字符串
        """
        pattern = r'\$\w+'
        matches = re.findall(pattern, var_str)
        for match in matches:
            env_var_name = match[1:]  # 去掉 $ 符号
            if env_var_name in os.environ:
                var_str = var_str.replace(match, os.environ[env_var_name])
        return var_str

    def create_all_links(self):
        """批量创建所有链接"""
        link_type = self.link_type_combo.currentIndex()  # 0: symlink, 1: junction
        success_count = 0
        fail_messages = []
        
        for form_row in self.link_form_rows:
            source_link = form_row.sourceLink.text()
            target_link = form_row.targetLink.text()
            
            if not source_link or not target_link:
                continue
            
            try:
                if os.path.exists(target_link) or os.path.islink(target_link):
                    fail_messages.append(f"目标已存在: {target_link}")
                    continue
                
                if link_type == 0:
                    os.symlink(source_link, target_link, target_is_directory=True)
                else:
                    # Windows下用mklink /J创建目录联接
                    cmd = f'cmd.exe /c mklink /J "{target_link}" "{source_link}"'
                    subprocess.check_call(cmd, shell=True)
                
                success_count += 1
            except subprocess.CalledProcessError as e:
                fail_messages.append(f"{target_link} 创建失败: {e}")
            except OSError as e:
                fail_messages.append(f"{target_link} 创建失败: {e}")
            except Exception as e:
                fail_messages.append(f"{target_link} 创建失败: {e}")
        
        # 显示结果
        message = f"成功创建 {success_count} 个链接。"
        if fail_messages:
            message += "\n失败信息:\n" + "\n".join(fail_messages)
        QMessageBox.information(self, "创建结果", message)
        self._update_window_height()

    def save_settings(self):
        """保存设置到配置文件"""
        link_list = []
        for form_row in self.link_form_rows:
            source = form_row.sourceLink.text()
            target = form_row.targetLink.text()
            if source or target:  # 至少有一个不为空
                link_list.append([source, target])
        
        try:
            with open(diskLinkFile, 'w', encoding='utf-8') as f:
                json.dump({"linkList": link_list}, f, ensure_ascii=False, indent=2)
            QMessageBox.information(self, "保存设置", "设置已成功保存！")
        except IOError as e:
            QMessageBox.critical(self, "保存失败", f"文件写入错误：{e}")
        except Exception as e:
            QMessageBox.critical(self, "保存失败", f"保存设置时出错：{e}")

# ==================== 主程序入口 ====================
if __name__ == "__main__":
    # 检查是否有管理员权限，如果没有则自动提权
    if not l_admin.is_admin():
        lprint("检测到无管理员权限，正在请求提权...")
        try:
            l_admin.runAsAdmin(
                pyexe=sys.executable,
                pyfile=__file__,
                args=sys.argv[1:]
            )
            sys.exit(0)  # 退出当前进程
        except Exception as e:
            lprint(f"提权失败: {e}")
            # 提权失败也继续运行，让用户手动处理权限问题
    
    app = QApplication(sys.argv)
    main_win = DiskLinkManagerApp()
    main_win.show()
    sys.exit(app.exec_())

'''
import sys
import hou
sys.path.append(r'D:\TD_Depot\interview_test\HoudiniExCache' )
print (sys.executable)
import main
from imp import reload
reload (main)
mainwin = main.ExampleApp()
mainwin.show()

'''

