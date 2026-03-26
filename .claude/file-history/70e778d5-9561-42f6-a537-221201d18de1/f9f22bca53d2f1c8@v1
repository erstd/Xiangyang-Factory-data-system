# -*- coding: utf-8 -*-
"""
向阳厂数据管理系统
权限等级：
1. 一线工厂 - 数据录入权限
2. 财务 - 数据核查与修改权限
"""

import sys
import sqlite3
from datetime import datetime
import os
from data import DatabaseManager, get_database_path
from goodsprocess import GoodsProcessingTab, GoodsProcessingDialog
from wage import WageCalculationDialog, WageCalculationTab
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QDialog, QTabWidget, QComboBox, QDateEdit, QHeaderView,
    QTextEdit, QGridLayout, QGroupBox, QSplitter, QFileDialog
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont


class LoginDialog(QDialog):
    """登录对话框"""
    
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.user_role = None
        self.username = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('向阳厂数据管理系统 - 登录')
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # 标题
        title = QLabel('向阳厂数据管理系统')
        title.setFont(QFont('Arial', 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 用户名
        user_layout = QHBoxLayout()
        user_label = QLabel('用户名:')
        user_label.setFixedWidth(80)
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText('请输入用户名')
        user_layout.addWidget(user_label)
        user_layout.addWidget(self.user_input)
        layout.addLayout(user_layout)
        
        # 密码
        pwd_layout = QHBoxLayout()
        pwd_label = QLabel('密码:')
        pwd_label.setFixedWidth(80)
        self.pwd_input = QLineEdit()
        self.pwd_input.setPlaceholderText('请输入密码')
        self.pwd_input.setEchoMode(QLineEdit.Password)
        pwd_layout.addWidget(pwd_label)
        pwd_layout.addWidget(self.pwd_input)
        layout.addLayout(pwd_layout)
        
        # 登录按钮
        btn_layout = QHBoxLayout()
        login_btn = QPushButton('登录')
        login_btn.clicked.connect(self.login)
        login_btn.setFixedWidth(100)
        cancel_btn = QPushButton('退出')
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setFixedWidth(100)
        
        btn_layout.addStretch()
        btn_layout.addWidget(login_btn)
        btn_layout.addWidget(cancel_btn)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        
        # 提示信息
        tip_label = QLabel('提示：默认账号 factory/factory123 (一线工厂) 或 admin/admin123 (财务)')
        tip_label.setStyleSheet('color: gray; font-size: 10px;')
        tip_label.setWordWrap(True)
        layout.addWidget(tip_label)
        
        self.setLayout(layout)
    
    def login(self):
        username = self.user_input.text().strip()
        password = self.pwd_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, '警告', '请输入用户名和密码！')
            return
        
        result = self.db_manager.fetch_one(
            'SELECT role FROM users WHERE username=? AND password=?',
            (username, password)
        )
        
        if result:
            self.user_role = result[0]
            self.username = username
            self.accept()
        else:
            QMessageBox.critical(self, '错误', '用户名或密码错误！')



class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self, user_role, username):
        super().__init__()
        self.user_role = user_role
        self.username = username
        self.db_manager = DatabaseManager()
        
        self.init_ui()
        self.showMaximized()
    
    def init_ui(self):
        # 窗口设置
        self.setWindowTitle(f'向阳厂数据管理系统 - {self.username}({self.user_role})')
        
        # 中央部件
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        # 欢迎信息
        welcome_label = QLabel(f'欢迎 {self.username} ({self.user_role})')
        welcome_label.setFont(QFont('Arial', 12))
        welcome_label.setStyleSheet('color: blue; padding: 10px;')
        layout.addWidget(welcome_label)
        
        # 标签页
        tab_widget = QTabWidget()
        
        # 货品加工收发
        goods_tab = GoodsProcessingTab(self.db_manager, self.user_role, self.username)
        tab_widget.addTab(goods_tab, '货品加工收发')
        
        # 工资核算
        wage_tab = WageCalculationTab(self.db_manager, self.user_role, self.username)
        tab_widget.addTab(wage_tab, '工资核算')
        
        # 未来可添加：客户结算货款、利润核算等标签页
        
        layout.addWidget(tab_widget)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    
    def closeEvent(self, event):
        """关闭事件"""
        self.db_manager.close()
        event.accept()


def main():
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyle('Fusion')
    
    # 创建数据库管理器
    db_manager = DatabaseManager()
    
    # 显示登录对话框
    login_dialog = LoginDialog(db_manager)
    
    if login_dialog.exec_() == QDialog.Accepted:
        # 创建主窗口
        main_window = MainWindow(login_dialog.user_role, login_dialog.username)
        main_window.show()
        
        sys.exit(app.exec_())
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()