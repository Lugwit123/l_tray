import sys
import requests
from PyQt5.QtWidgets import *  # noqa: F403
from PyQt5.QtCore import QByteArray, pyqtSlot
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPixmap, QPalette, QBrush,QPainter
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

import json
import os
import random
import string
sys.path.append(os.getenv('LugwitLibDir'))
import Lugwit_Module as LM
from Lugwit_Module import lprint
from Lugwit_Module.l_src.UILib.QTLib.styleSheet import self_qss


class CustomTitleBar(QWidget):
    def __init__(self, title='登录与注册'):
        super().__init__()
        self.title = title
        self.initUI()
        

    def initUI(self):
        self.layout = QHBoxLayout()
        self.titleLabel = QLabel(self.title)
        self.titleLabel.setStyleSheet("background-color: rgba(20, 20, 50,10);font-size: 18px;color: black;")
        self.layout.addWidget(self.titleLabel)

        # 关闭按钮
        self.closeButton = QPushButton('X', self)
        self.closeButton.clicked.connect(self.on_close_clicked)
        self.closeButton.setFixedSize(40, 40)  # 设置按钮大小
        self.closeButton.setStyleSheet("background-color: transparent;font-size: 28px;color: red;")  # 设置透明背景
        self.layout.addWidget(self.closeButton)

        # ... 其他按钮（最小化等）

        self.setLayout(self.layout)

    def on_close_clicked(self):
        self.window().close()
        




class App(QMainWindow):
    def __init__(self):
        super().__init__(flags=Qt.FramelessWindowHint)
        self.title = '登录与注册'
        self.initUrl()
        self.initUI()
        self.setFixedSize(600, 608)
        self.setStyleSheet(f'{self_qss}\nQMainWindow {{border: 3px solid rgba(200, 200, 250, 50)}}\nQWidget {{\
        background-color: rgba(205, 205, 205, 20);}}')

    def initUrl(self):
        self.server_url=r'http://localhost:8000'
        self.register_url=f'{self.server_url}/register'

        
    def paintEvent(self, event):
            painter = QPainter(self)
            pixmap = QPixmap("aa.jpg")  # 替换为您的图片文件路径
            rect = self.rect()
            
            # 限制绘制区域为窗口的上半部分
            rect.setBottom(230)
            painter.drawPixmap(rect, pixmap, pixmap.rect())



    def initUI(self):
        self.setWindowTitle(self.title)
        self.title_bar = CustomTitleBar()
        
        self.setMenuWidget(self.title_bar)
        layout = QVBoxLayout()
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_widget.setLayout(layout)

        layout.addSpacing(180)
        # 用户名下拉框
        
        self.tabWidget = QTabWidget(self)
        
        
        layout.addWidget(self.tabWidget)
        
        loginTabWidget = QWidget(self.tabWidget)
        regiterTabWidget = QWidget(self.tabWidget)
        loginTabWidget.setVisible(True)
        regiterTabWidget.setVisible(False)

        
        self.tabWidget.addTab(loginTabWidget, "登录")
        self.tabWidget.addTab(regiterTabWidget, "注册")
        self.tabWidget.currentChanged.connect(self.tabChanged)

        
        # 登录界面
        self.username_combo = QComboBox()
        layout.addWidget(self.username_combo)
        self.username_combo.setFixedHeight(40)
        self.username_combo.setEditable(True)
        self.username_combo.lineEdit().setPlaceholderText("请输入用户名")  
                
        # 邮箱输入框
        self.email_edit = QLineEdit()
        self.email_edit.setFixedHeight(40)
        self.email_edit.setPlaceholderText("请输入邮箱")
        layout.addWidget(self.email_edit)

        # 密码输入框和眼睛按钮
        self.password_edit = QLineEdit()
        self.password_edit.setFixedHeight(40)
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setPlaceholderText("请输入密码")
        layout.addWidget(self.password_edit)


        # 密码显示按钮
        self.toggle_password_visibility = QAction(self)
        self.toggle_password_visibility.setIcon(QIcon("eye_icon.png"))  # 使用适当的眼睛图标
        self.toggle_password_visibility.triggered.connect(self.toggle_password)
        self.password_edit.addAction(self.toggle_password_visibility, QLineEdit.TrailingPosition)

        # 加载用户名历史
        self.load_username_history()

        # 登录按钮
        self.login_button = QPushButton('登录', self)
        self.login_button.clicked.connect(self.on_login_click)
        layout.addWidget(self.login_button)
        
        # 注册按钮
        self.register_button = QPushButton('注册', self)
        self.register_button.clicked.connect(self.on_register_click)
        layout.addWidget(self.register_button)

        # 登录按钮
        self.randGenRegisterInfo = QPushButton('随机生成注册信息', self)
        self.randGenRegisterInfo.clicked.connect(self.on_generate_click)
        layout.addWidget(self.randGenRegisterInfo)

        # 保存密码和自动登录复选框
        self.save_password_checkbox = QCheckBox("保存密码", self)
        layout.addWidget(self.save_password_checkbox)
        self.save_password_checkbox.setFixedWidth(100)
        self.auto_login_checkbox = QCheckBox("自动登录", self)
        self.auto_login_checkbox.setFixedWidth(100)
        layout.addWidget(self.auto_login_checkbox)

        self.setGeometry(300, 300, 300, 200)
        self.load_credentials()
        self.center()
        self.tabChanged()
        
    def tabChanged(self):
        if self.tabWidget.currentIndex() == 0:
            self.register_button.setEnabled(False)
            self.randGenRegisterInfo.setEnabled(False)
            self.email_edit.setEnabled(False)
        else:
            self.register_button.setEnabled(True)
            self.randGenRegisterInfo.setEnabled(True)
            self.email_edit.setEnabled(True)

    @pyqtSlot()
    def on_register_click(self):
        # 从UI中收集用户输入
        username = self.username_combo.currentText()
        password = self.password_edit.text()
        email = self.email_edit.text()  # 获取邮箱地址

        # 对密码加密
        encrypted_password = self.encrypt(password).decode()

        # 准备发送到服务器的数据
        data = {
            'username': username,
            'password': encrypted_password,
            'email': email  # 添加邮箱地址
        }

        # 向服务器的注册端点发送 POST 请求
        response = requests.post(self.register_url, json=data)
        lprint (response)
        lprint (dir(response))

        if response.status_code == 200:
            QMessageBox.information(self, 'Success', '用户注册成功！')
            self.save_username_history()  # 保存用户名历史
        else:
            error_message = response.json().get('detail', '注册失败，请重试。')
            msgBox = QMessageBox(self)
            msgBox.setText(f"注册失败\n{error_message}")
            msgBox.resize(400, msgBox.sizeHint().height())
            msgBox.exec_()


    def on_login_click(self):
        pass

    def save_credentials(self, username, password):
        encrypted_username = self.encrypt(username).decode()
        encrypted_password = self.encrypt(password).decode()
        with open("credentials.json", "w") as file:
            json.dump({"username": encrypted_username, "password": encrypted_password}, file)

    def load_credentials(self):
        if os.path.exists("credentials.json"):
            with open("credentials.json", "r") as file:
                credentials = json.load(file)
                decrypted_username = self.decrypt(credentials["username"].encode())
                decrypted_password = self.decrypt(credentials["password"].encode())
                self.username_combo.setText(decrypted_username)
                self.password_edit.setText(decrypted_password)
                if self.auto_login_checkbox.isChecked():
                    self.on_login_click()

    def encrypt(self, data):
        return self.cipher_suite.encrypt(data.encode())

    def decrypt(self, encrypted_data):
        return self.cipher_suite.decrypt(encrypted_data).decode()
    
    def toggle_password(self):
        if self.password_edit.echoMode() == QLineEdit.Password:
            self.password_edit.setEchoMode(QLineEdit.Normal)
        else:
            self.password_edit.setEchoMode(QLineEdit.Password)
            
    @pyqtSlot()
    def on_generate_click(self):
        # 随机生成用户名和密码
        username = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        email = f"{username}@example.com"

        # 填充到输入框中
        self.username_combo.setCurrentText(username)
        self.password_edit.setText(password)
        self.email_edit.setText(email)

    def load_username_history(self):
        if os.path.exists("usernames.json"):
            with open("usernames.json", "r") as file:
                usernames = json.load(file)
                self.username_combo.addItems(usernames)

    def save_username_history(self):
        usernames = [self.username_combo.itemText(i) for i in range(self.username_combo.count())]
        with open("usernames.json", "w") as file:
            json.dump(usernames, file)
    
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        cp.setY(cp.y() - 200)  # 向上移动200像素
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.window().move(self.window().pos() + delta)
            self.oldPos = event.globalPos()

def main():
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
