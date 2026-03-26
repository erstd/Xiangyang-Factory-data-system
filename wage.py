import sqlite3
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QDialog, QTabWidget, QComboBox, QDateEdit, QHeaderView,
    QTextEdit, QGridLayout, QGroupBox, QSplitter, QFileDialog, QFrame
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QColor


def show_styled_message(parent, title, text, icon=QMessageBox.Information):
    """显示统一样式的消息框"""
    msg = QMessageBox(parent)
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(icon)
    msg.setStyleSheet("""
        QMessageBox {
            background-color: white;
        }
        QLabel {
            color: #212121;
            font-size: 16px;
            min-width: 240px;
            padding: 10px;
        }
        QPushButton {
            background-color: #2196F3;
            color: white;
            border: none;
            padding: 8px 24px;
            border-radius: 4px;
            font-size: 16px;
            font-weight: bold;
            min-width: 70px;
        }
        QPushButton:hover {
            background-color: #1976D2;
        }
    """)
    return msg.exec_()



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
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)

        # ===== 操作按钮区域 =====
        button_card = QFrame()
        button_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
            }
        """)

        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(15, 12, 15, 12)
        btn_layout.setSpacing(10)

        refresh_btn = QPushButton('刷新')
        refresh_btn.clicked.connect(self.load_data)
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.setFont(QFont('Microsoft YaHei', 13))
        refresh_btn.setFixedHeight(46)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0 24px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        btn_layout.addWidget(refresh_btn)

        if self.user_role == 'finance':
            add_btn = QPushButton('添加记录')
            add_btn.clicked.connect(self.add_record)
            add_btn.setCursor(Qt.PointingHandCursor)
            add_btn.setFont(QFont('Microsoft YaHei', 13))
            add_btn.setFixedHeight(46)
            add_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 0 24px;
                }
                QPushButton:hover {
                    background-color: #45A049;
                }
            """)
            btn_layout.addWidget(add_btn)

        btn_layout.addStretch()
        button_card.setLayout(btn_layout)
        layout.addWidget(button_card)

        # ===== 表格区域 =====
        table_card = QFrame()
        table_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
            }
        """)

        table_layout = QVBoxLayout()
        table_layout.setContentsMargins(15, 15, 15, 15)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            'ID', '加工车间', '织片数量', '织片工资',
            '套口货物', '套口工资', '手缝货物', '创建人'
        ])

        # 表格样式美化
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                gridline-color: #E0E0E0;
                font-size: 16px;
            }
            QTableWidget::item {
                padding: 10px 8px;
                border-bottom: 1px solid #F5F5F5;
            }
            QTableWidget::item:selected {
                background-color: #E3F2FD;
                color: #212121;
            }
            QTableWidget::item:hover {
                background-color: #F5F5F5;
            }
            QHeaderView::section {
                background-color: #FAFAFA;
                color: #424242;
                padding: 12px 8px;
                border: none;
                border-bottom: 2px solid #E0E0E0;
                font-weight: bold;
                font-size: 16px;
            }
        """)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)

        table_layout.addWidget(self.table)
        table_card.setLayout(table_layout)
        layout.addWidget(table_card)

        self.setLayout(layout)
        self.load_data()
    
    def load_data(self):
        """加载数据"""
        query = '''
            SELECT id, workshop_name, knitting_qty, knitting_wage,
                   overlock_goods_type, overlock_wage,
                   hand_sewing_goods_type, created_by
            FROM wage_calculation
            ORDER BY id DESC
        '''
        results = self.db_manager.fetch_all(query)

        self.table.setRowCount(len(results))
        for row, data in enumerate(results):
            for col, value in enumerate(data):
                # 格式化显示
                if col in [4, 6]:  # 货物种类列
                    display_value = value if value else '-'
                else:
                    display_value = str(value) if value else ''

                item = QTableWidgetItem(display_value)
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
        self.setFixedSize(750, 680)

        # 设置对话框样式
        self.setStyleSheet("""
            QDialog {
                background-color: #FAFAFA;
            }
            QGroupBox {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                margin-top: 16px;
                padding: 18px;
                font-weight: bold;
                font-size: 16px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 6px 12px;
                color: #212121;
            }
            QLabel {
                color: #424242;
                font-size: 16px;
            }
            QLineEdit, QComboBox, QDateEdit {
                background-color: #F5F5F5;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 16px;
            }
            QLineEdit:hover, QComboBox:hover, QDateEdit:hover {
                border: 1px solid #2196F3;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border: 1px solid #2196F3;
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
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
        self.overlock_goods_type = QComboBox()
        self.overlock_goods_type.addItems(['织纱', '织片'])
        self.overlock_qty = QLineEdit()
        self.overlock_wage = QLineEdit()

        overlock_layout.addWidget(QLabel('套口员工:'), 0, 0)
        overlock_layout.addWidget(self.overlock_employee, 0, 1)
        overlock_layout.addWidget(QLabel('货物种类:'), 0, 2)
        overlock_layout.addWidget(self.overlock_goods_type, 0, 3)
        overlock_layout.addWidget(QLabel('套口数量:'), 1, 0)
        overlock_layout.addWidget(self.overlock_qty, 1, 1)
        overlock_layout.addWidget(QLabel('套口工资:'), 1, 2)
        overlock_layout.addWidget(self.overlock_wage, 1, 3)
        
        overlock_group.setLayout(overlock_layout)
        layout.addWidget(overlock_group)
        
        # 手缝信息
        sewing_group = QGroupBox('手缝信息')
        sewing_layout = QGridLayout()

        self.sewing_employee = QLineEdit()
        self.sewing_goods_type = QComboBox()
        self.sewing_goods_type.addItems(['织纱', '织片'])
        self.sewing_qty = QLineEdit()
        self.sewing_wage = QLineEdit()

        sewing_layout.addWidget(QLabel('手缝员工:'), 0, 0)
        sewing_layout.addWidget(self.sewing_employee, 0, 1)
        sewing_layout.addWidget(QLabel('货物种类:'), 0, 2)
        sewing_layout.addWidget(self.sewing_goods_type, 0, 3)
        sewing_layout.addWidget(QLabel('手缝数量:'), 1, 0)
        sewing_layout.addWidget(self.sewing_qty, 1, 1)
        sewing_layout.addWidget(QLabel('手缝工资:'), 1, 2)
        sewing_layout.addWidget(self.sewing_wage, 1, 3)
        
        sewing_group.setLayout(sewing_layout)
        layout.addWidget(sewing_group)
        
        # 按钮
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 18, 0, 0)
        btn_layout.addStretch()

        save_btn = QPushButton('保存')
        save_btn.setFixedHeight(46)
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setFont(QFont('Microsoft YaHei', 14, QFont.Bold))
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0 36px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        save_btn.clicked.connect(self.save)

        cancel_btn = QPushButton('取消')
        cancel_btn.setFixedHeight(46)
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setFont(QFont('Microsoft YaHei', 14))
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #F5F5F5;
                color: #616161;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                padding: 0 36px;
            }
            QPushButton:hover {
                background-color: #EEEEEE;
            }
        """)
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(btn_layout)

        self.setLayout(layout)
    
    def save(self):
        """保存数据"""
        if not self.workshop_name.text().strip():
            show_styled_message(self, '警告', '加工车间不能为空！', QMessageBox.Warning)
            return

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        query = '''
            INSERT INTO wage_calculation (
                workshop_name, processing_date, knitting_qty, knitting_wage,
                overlock_employee, overlock_goods_type, overlock_qty, overlock_wage,
                hand_sewing_employee, hand_sewing_goods_type, hand_sewing_qty, hand_sewing_wage,
                created_by, created_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''

        params = (
            self.workshop_name.text().strip(),
            self.processing_date.date().toString('yyyy-MM-dd'),
            int(self.knitting_qty.text()) if self.knitting_qty.text() else 0,
            float(self.knitting_wage.text()) if self.knitting_wage.text() else 0.0,
            self.overlock_employee.text().strip(),
            self.overlock_goods_type.currentText(),
            int(self.overlock_qty.text()) if self.overlock_qty.text() else 0,
            float(self.overlock_wage.text()) if self.overlock_wage.text() else 0.0,
            self.sewing_employee.text().strip(),
            self.sewing_goods_type.currentText(),
            int(self.sewing_qty.text()) if self.sewing_qty.text() else 0,
            float(self.sewing_wage.text()) if self.sewing_wage.text() else 0.0,
            self.username,
            current_time
        )

        if self.db_manager.execute_query(query, params):
            show_styled_message(self, '成功', '工资记录保存成功！', QMessageBox.Information)
            self.accept()
        else:
            show_styled_message(self, '错误', '保存失败！', QMessageBox.Critical)
