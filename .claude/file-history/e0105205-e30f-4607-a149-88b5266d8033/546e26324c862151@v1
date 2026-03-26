import sqlite3
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QDialog, QTabWidget, QComboBox, QDateEdit, QHeaderView,
    QTextEdit, QGridLayout, QGroupBox, QSplitter, QFileDialog
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont



class WageCalculationTab(QWidget):
    """工资核算标签页"""
    
    def __init__(self, db_manager, user_role, username):
        super().__init__()
        self.db_manager = db_manager
        self.user_role = user_role
        self.username = username
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # 按钮区域
        btn_layout = QHBoxLayout()
        refresh_btn = QPushButton('刷新')
        refresh_btn.clicked.connect(self.load_data)
        btn_layout.addWidget(refresh_btn)
        
        if self.user_role == 'finance':
            add_btn = QPushButton('添加记录')
            add_btn.clicked.connect(self.add_record)
            btn_layout.addWidget(add_btn)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # 数据表格
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            'ID', '加工车间', '织片数量', '织片工资', '套口工资', '创建人'
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        self.load_data()
    
    def load_data(self):
        """加载数据"""
        query = '''
            SELECT id, workshop_name, knitting_qty, knitting_wage,
                   overlock_wage, created_by
            FROM wage_calculation 
            ORDER BY id DESC
        '''
        results = self.db_manager.fetch_all(query)
        
        self.table.setRowCount(len(results))
        for row, data in enumerate(results):
            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value) if value else '')
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, col, item)
    
    def add_record(self):
        """添加记录"""
        dialog = WageCalculationDialog(self.db_manager, self.username)
        if dialog.exec_() == QDialog.Accepted:
            self.load_data()


class WageCalculationDialog(QDialog):
    """工资核算对话框"""
    
    def __init__(self, db_manager, username):
        super().__init__()
        self.db_manager = db_manager
        self.username = username
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('工资核算记录')
        self.setFixedSize(700, 600)
        
        layout = QVBoxLayout()
        
        # 车间信息
        workshop_group = QGroupBox('车间信息')
        workshop_layout = QGridLayout()
        
        self.workshop_name = QLineEdit()
        self.processing_date = QDateEdit()
        self.processing_date.setCalendarPopup(True)
        self.processing_date.setDate(QDate.currentDate())
        self.knitting_qty = QLineEdit()
        self.knitting_wage = QLineEdit()
        
        workshop_layout.addWidget(QLabel('加工车间:'), 0, 0)
        workshop_layout.addWidget(self.workshop_name, 0, 1)
        workshop_layout.addWidget(QLabel('加工日期:'), 0, 2)
        workshop_layout.addWidget(self.processing_date, 0, 3)
        workshop_layout.addWidget(QLabel('织片数量:'), 1, 0)
        workshop_layout.addWidget(self.knitting_qty, 1, 1)
        workshop_layout.addWidget(QLabel('织片工资:'), 1, 2)
        workshop_layout.addWidget(self.knitting_wage, 1, 3)
        
        workshop_group.setLayout(workshop_layout)
        layout.addWidget(workshop_group)
        
        # 套口信息
        overlock_group = QGroupBox('套口信息')
        overlock_layout = QGridLayout()
        
        self.overlock_employee = QLineEdit()
        self.overlock_qty = QLineEdit()
        self.overlock_wage = QLineEdit()
        
        overlock_layout.addWidget(QLabel('套口员工:'), 0, 0)
        overlock_layout.addWidget(self.overlock_employee, 0, 1)
        overlock_layout.addWidget(QLabel('套口数量:'), 0, 2)
        overlock_layout.addWidget(self.overlock_qty, 0, 3)
        overlock_layout.addWidget(QLabel('套口工资:'), 1, 0)
        overlock_layout.addWidget(self.overlock_wage, 1, 1)
        
        overlock_group.setLayout(overlock_layout)
        layout.addWidget(overlock_group)
        
        # 手缝信息
        sewing_group = QGroupBox('手缝信息')
        sewing_layout = QGridLayout()
        
        self.sewing_employee = QLineEdit()
        self.sewing_qty = QLineEdit()
        self.sewing_wage = QLineEdit()
        
        sewing_layout.addWidget(QLabel('手缝员工:'), 0, 0)
        sewing_layout.addWidget(self.sewing_employee, 0, 1)
        sewing_layout.addWidget(QLabel('手缝数量:'), 0, 2)
        sewing_layout.addWidget(self.sewing_qty, 0, 3)
        sewing_layout.addWidget(QLabel('手缝工资:'), 1, 0)
        sewing_layout.addWidget(self.sewing_wage, 1, 1)
        
        sewing_group.setLayout(sewing_layout)
        layout.addWidget(sewing_group)
        
        # 按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        save_btn = QPushButton('保存')
        save_btn.clicked.connect(self.save)
        cancel_btn = QPushButton('取消')
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def save(self):
        """保存数据"""
        if not self.workshop_name.text().strip():
            QMessageBox.warning(self, '警告', '加工车间不能为空！')
            return
        
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        query = '''
            INSERT INTO wage_calculation (
                workshop_name, processing_date, knitting_qty, knitting_wage,
                overlock_employee, overlock_qty, overlock_wage,
                hand_sewing_employee, hand_sewing_qty, hand_sewing_wage,
                created_by, created_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        params = (
            self.workshop_name.text().strip(),
            self.processing_date.date().toString('yyyy-MM-dd'),
            int(self.knitting_qty.text()) if self.knitting_qty.text() else 0,
            float(self.knitting_wage.text()) if self.knitting_wage.text() else 0.0,
            self.overlock_employee.text().strip(),
            int(self.overlock_qty.text()) if self.overlock_qty.text() else 0,
            float(self.overlock_wage.text()) if self.overlock_wage.text() else 0.0,
            self.sewing_employee.text().strip(),
            int(self.sewing_qty.text()) if self.sewing_qty.text() else 0,
            float(self.sewing_wage.text()) if self.sewing_wage.text() else 0.0,
            self.username,
            current_time
        )
        
        if self.db_manager.execute_query(query, params):
            QMessageBox.information(self, '成功', '工资记录保存成功！')
            self.accept()
        else:
            QMessageBox.critical(self, '错误', '保存失败！')
