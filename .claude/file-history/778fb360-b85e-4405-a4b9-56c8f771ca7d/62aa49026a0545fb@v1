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


class GoodsProcessingTab(QWidget):
    """货品加工收发标签页"""
    
    def __init__(self, db_manager, user_role, username):
        super().__init__()
        self.db_manager = db_manager
        self.user_role = user_role
        self.username = username
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # ===== 搜索区域增强 =====
        search_layout = QHBoxLayout()
        
        # 类型筛选
        self.type_filter = QComboBox()
        self.type_filter.addItems(['全部', '织纱', '织片'])
        self.type_filter.currentTextChanged.connect(self.load_data)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('搜索客户名称/款号...')
        self.search_input.returnPressed.connect(self.search_data)
        
        search_btn = QPushButton('搜索')
        search_btn.clicked.connect(self.search_data)
        refresh_btn = QPushButton('刷新')
        refresh_btn.clicked.connect(self.load_data)
        
        search_layout.addWidget(QLabel('货物类型:'))
        search_layout.addWidget(self.type_filter)
        search_layout.addWidget(QLabel('关键词:'))
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        search_layout.addWidget(refresh_btn)
        search_layout.addStretch()
        
        # ===== 操作按钮区域 =====
        button_layout = QHBoxLayout()
        
        # 新增按钮（所有角色都可使用）
        add_btn = QPushButton('新增记录')
        add_btn.clicked.connect(self.add_record)
        add_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 5px;")
        
        # 修改和删除按钮（根据权限控制）
        edit_btn = QPushButton('修改记录')
        edit_btn.clicked.connect(self.edit_record)
        
        delete_btn = QPushButton('删除记录')
        delete_btn.clicked.connect(self.delete_record)
        
        # 根据用户角色控制按钮可用性
        if self.user_role == 'finance':
            # 财务人员只能查看
            add_btn.setEnabled(True)
            edit_btn.setEnabled(True)
            delete_btn.setEnabled(True)

        elif self.user_role == 'operator':
            # 操作员可以新增和修改，但不能删除
            delete_btn.setEnabled(False)
        
        button_layout.addWidget(add_btn)
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addStretch()
        
        # 组合搜索和按钮区域
        top_layout = QVBoxLayout()
        top_layout.addLayout(search_layout)
        top_layout.addLayout(button_layout)
        layout.addLayout(top_layout)
        
        # ===== 表格结构调整 =====
        self.table = QTableWidget()
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels([
            'ID', '类型', '客户名称', '客户款号', 
            '客户发货量', '工厂收货量', '收发差异', 
            '工厂出货量', '客户收货量', '厂客差异',
            '最后更新', '操作人'
        ])
        # 设置关键列宽度（差异列高亮）
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # 客户名称列自适应
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # 收发差异
        header.setSectionResizeMode(9, QHeaderView.ResizeToContents)  # 厂客差异
        header.setSectionResizeMode(10, QHeaderView.ResizeToContents)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)  # 交替行颜色，提高可读性
        layout.addWidget(self.table)
        
        # 添加底部统计信息
        self.status_label = QLabel('')
        self.status_label.setStyleSheet("color: #666; padding: 5px;")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        self.load_data()
        
        # 连接表格选择变化事件，更新状态信息
        self.table.itemSelectionChanged.connect(self.update_status)

    def load_data(self):
        """加载数据（支持类型筛选）"""
        base_query = '''
            SELECT id, goods_type, customer_name,
                customer_send_qty, factory_receive_qty, diff_receive,
                factory_send_qty, customer_receive_qty, diff_factory_customer,
                COALESCE(modified_date, created_date), 
                COALESCE(modified_by, created_by, '-')
            FROM goods_processing_v2
        '''
        
        params = []
        current_type = self.type_filter.currentText()
        if current_type != '全部':
            base_query += ' WHERE goods_type = ?'
            params.append(current_type)
        
        base_query += ' ORDER BY id DESC'
        
        results = self.db_manager.fetch_all(base_query, params if params else None)
        self._populate_table(results)

    def search_data(self):
        """增强搜索（支持款号+客户名）"""
        keyword = self.search_input.text().strip()
        if not keyword:
            self.load_data()
            return
        
        base_query = '''
            SELECT id, goods_type, customer_name,
                customer_send_qty, factory_receive_qty, diff_receive,
                factory_send_qty, customer_receive_qty, diff_factory_customer,
                COALESCE(modified_date, created_date), 
                COALESCE(modified_by, created_by, '-')
            FROM goods_processing_v2
            WHERE (customer_name LIKE ?)
        '''
        
        params = [f'%{keyword}%', f'%{keyword}%']
        current_type = self.type_filter.currentText()
        if current_type != '全部':
            base_query += ' AND goods_type = ?'
            params.append(current_type)
        
        base_query += ' ORDER BY id DESC'
        results = self.db_manager.fetch_all(base_query, params)
        self._populate_table(results)

    def _populate_table(self, results):
        """统一表格填充逻辑（含差异高亮）"""
        self.table.setRowCount(len(results))
        
        # 用于统计的变量
        total_customer_send = 0
        total_factory_receive = 0
        total_factory_send = 0
        total_customer_receive = 0
        
        for row, data in enumerate(results):
            # 累加统计数据（跳过可能的None值）
            if len(data) > 8:  # 确保有足够的数据列
                try:
                    total_customer_send += int(data[4] or 0)
                    total_factory_receive += int(data[5] or 0)
                    total_factory_send += int(data[7] or 0)
                    total_customer_receive += int(data[8] or 0)
                except (ValueError, TypeError, IndexError):
                    pass
            
            for col, value in enumerate(data):
                display_val = str(value) if value not in (None, '') else '0' if col in [4,5,6,7,8,9] else '-'
                item = QTableWidgetItem(display_val)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                
                # 差异列高亮（负差异标红）
                if col == 6 or col == 9:  # 收发差异/厂客差异列
                    try:
                        diff_val = int(value) if value else 0
                        if diff_val < 0:
                            item.setForeground(QColor('red'))
                            item.setFont(QFont('Arial', 10, QFont.Bold))
                        elif diff_val > 0:
                            item.setForeground(QColor('green'))
                    except:
                        pass
                
                # 为数字列设置右对齐
                if col in [4, 5, 6, 7, 8, 9]:
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                
                self.table.setItem(row, col, item)
        
        # 更新统计信息
        total_diff_receive = total_customer_send - total_factory_receive
        total_diff_factory_customer = total_factory_send - total_customer_receive
        
        status_text = (f"📊 统计信息 | "
                    f"总客户发货: {total_customer_send} | "
                    f"总工厂收货: {total_factory_receive} | "
                    f"总收发差异: {total_diff_receive} | "
                    f"总工厂出货: {total_factory_send} | "
                    f"总客户收货: {total_customer_receive} | "
                    f"总厂客差异: {total_diff_factory_customer}")
        
        # 差异高亮
        if total_diff_receive != 0 or total_diff_factory_customer != 0:
            status_text += " ⚠️ 存在差异"
            self.status_label.setStyleSheet("color: orange; padding: 5px; font-weight: bold;")
        else:
            self.status_label.setStyleSheet("color: green; padding: 5px;")
        
        self.status_label.setText(status_text)

    def update_status(self):
        """更新选中状态信息"""
        selected = self.table.selectedItems()
        if selected:
            row = selected[0].row()
            count = len(selected) // self.table.columnCount()  # 粗略估计选中行数
            self.status_label.setText(f"已选择 {count} 行记录 | " + self.status_label.text())

    def add_record(self):
        """添加记录"""
        dialog = GoodsProcessingDialog(self.db_manager, self.username, mode='add')
        if dialog.exec_() == QDialog.Accepted:
            self.load_data()
    
    def edit_record(self):
        """修改记录"""
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, '警告', '请先选择一条记录！')
            return
        
        row = selected[0].row()
        record_id = int(self.table.item(row, 0).text())
        
        dialog = GoodsProcessingDialog(self.db_manager, self.username, mode='edit', record_id=record_id)
        if dialog.exec_() == QDialog.Accepted:
            self.load_data()
        
    def delete_record(self):
        """删除记录"""
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, '警告', '请先选择一条记录！')
            return
        
        reply = QMessageBox.question(self, '确认', '确定要删除这条记录吗？',
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            row = selected[0].row()
            record_id = int(self.table.item(row, 0).text())
            
            query = 'DELETE FROM goods_processing WHERE id=?'
            if self.db_manager.execute_query(query, (record_id,)):
                QMessageBox.information(self, '成功', '记录已删除！')
                self.load_data()


class GoodsProcessingDialog(QDialog):
    """货品加工收发记录对话框"""
    
    def __init__(self, db_manager, username, mode='add', record_id=None):
        super().__init__()
        self.db_manager = db_manager
        self.username = username
        self.mode = mode
        self.record_id = record_id
        self.init_ui()
        
        if mode == 'edit' and record_id:
            self.load_data()
    
    def init_ui(self):
        """初始化UI界面"""
        self.setWindowTitle('货物加工收发记录')
        self.setFixedSize(900, 750)
        
        main_layout = QVBoxLayout()
        
        # ===== 货物类型选择 =====
        if self.mode == 'add':
            type_layout = QHBoxLayout()
            type_layout.addWidget(QLabel('货物类型:'))
            self.goods_type = QComboBox()
            self.goods_type.addItems(['织纱', '织片'])
            type_layout.addWidget(self.goods_type)
            type_layout.addStretch()
            main_layout.addLayout(type_layout)
        
        # ===== 客户发货信息 =====
        send_group = QGroupBox('📦 客户发货信息')
        send_layout = QGridLayout()
        
        self.customer_name = QLineEdit()
        self.customer_send_date = QDateEdit()
        self.customer_send_date.setCalendarPopup(True)
        self.customer_send_date.setDate(QDate.currentDate())
        self.customer_send_method = QComboBox()
        self.customer_send_method.addItems(['快递', '物流', '自提', '其他'])
        self.customer_send_qty = QLineEdit()
        
        send_layout.addWidget(QLabel('客户名称:'), 0, 0)
        send_layout.addWidget(self.customer_name, 0, 1)
        send_layout.addWidget(QLabel('客户款号:'), 0, 2)
        send_layout.addWidget(QLabel('发货时间:'), 1, 0)
        send_layout.addWidget(self.customer_send_date, 1, 1)
        send_layout.addWidget(QLabel('运输方式:'), 1, 2)
        send_layout.addWidget(self.customer_send_method, 1, 3)
        send_layout.addWidget(QLabel('发货数量:'), 2, 0)
        send_layout.addWidget(self.customer_send_qty, 2, 1)
        
        send_group.setLayout(send_layout)
        main_layout.addWidget(send_group)
        
        # ===== 工厂收货信息 =====
        receive_group = QGroupBox('🏭 工厂收货信息')
        receive_layout = QGridLayout()
        
        self.factory_receive_qty = QLineEdit()
        self.diff_receive_display = QLineEdit()
        self.diff_receive_display.setReadOnly(True)
        self.diff_receive_display.setStyleSheet("color: red; font-weight: bold;")
        
        receive_layout.addWidget(QLabel('收货数量:'), 0, 0)
        receive_layout.addWidget(self.factory_receive_qty, 0, 1)
        receive_layout.addWidget(QLabel('收发差异:'), 0, 2)
        receive_layout.addWidget(self.diff_receive_display, 0, 3)
        
        receive_group.setLayout(receive_layout)
        main_layout.addWidget(receive_group)
        
        # ===== 工厂出货信息 =====
        factory_send_group = QGroupBox('🚚 工厂出货信息')
        factory_send_layout = QGridLayout()
        
        self.factory_send_date = QDateEdit()
        self.factory_send_date.setCalendarPopup(True)
        self.factory_send_date.setDate(QDate.currentDate())
        self.factory_send_method = QComboBox()
        self.factory_send_method.addItems(['快递', '物流', '自提', '其他'])
        self.factory_send_qty = QLineEdit()
        
        factory_send_layout.addWidget(QLabel('出货时间:'), 0, 0)
        factory_send_layout.addWidget(self.factory_send_date, 0, 1)
        factory_send_layout.addWidget(QLabel('运输方式:'), 0, 2)
        factory_send_layout.addWidget(self.factory_send_method, 0, 3)
        factory_send_layout.addWidget(QLabel('出货数量:'), 1, 0)
        factory_send_layout.addWidget(self.factory_send_qty, 1, 1)
        
        factory_send_group.setLayout(factory_send_layout)
        main_layout.addWidget(factory_send_group)
        
        # ===== 客户收货信息 =====
        customer_receive_group = QGroupBox('✅ 客户收货信息')
        customer_receive_layout = QGridLayout()
        
        self.customer_receive_qty = QLineEdit()
        self.diff_factory_customer_display = QLineEdit()
        self.diff_factory_customer_display.setReadOnly(True)
        self.diff_factory_customer_display.setStyleSheet("color: red; font-weight: bold;")
        
        customer_receive_layout.addWidget(QLabel('收货数量:'), 0, 0)
        customer_receive_layout.addWidget(self.customer_receive_qty, 0, 1)
        customer_receive_layout.addWidget(QLabel('厂客差异:'), 0, 2)
        customer_receive_layout.addWidget(self.diff_factory_customer_display, 0, 3)
        
        customer_receive_group.setLayout(customer_receive_layout)
        main_layout.addWidget(customer_receive_group)
        
        # 连接信号槽（实时计算差异）
        self.customer_send_qty.textChanged.connect(self._calculate_diffs)
        self.factory_receive_qty.textChanged.connect(self._calculate_diffs)
        self.factory_send_qty.textChanged.connect(self._calculate_diffs)
        self.customer_receive_qty.textChanged.connect(self._calculate_diffs)
        
        # ===== 按钮 =====
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        save_btn = QPushButton('保存')
        save_btn.clicked.connect(self.save)
        cancel_btn = QPushButton('取消')
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        
        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

    def _calculate_diffs(self):
        """实时计算并显示差异"""
        try:
            send = int(self.customer_send_qty.text() or 0)
            recv = int(self.factory_receive_qty.text() or 0)
            self.diff_receive_display.setText(str(send - recv))
        except:
            self.diff_receive_display.setText('')
        
        try:
            factory_send = int(self.factory_send_qty.text() or 0)
            cust_recv = int(self.customer_receive_qty.text() or 0)
            self.diff_factory_customer_display.setText(str(factory_send - cust_recv))
        except:
            self.diff_factory_customer_display.setText('')

    def load_data(self):
        """加载数据（编辑模式）"""
        query = '''
            SELECT goods_type, customer_name, customer_send_date,
                customer_send_method, customer_send_qty, factory_receive_qty,
                factory_send_date, factory_send_method, factory_send_qty,
                customer_receive_qty, created_by
            FROM goods_processing_v2 WHERE id=?
        '''
        result = self.db_manager.fetch_one(query, (self.record_id,))
        
        if result:
            # 设置货物类型（如果是织纱，标题显示织纱）
            if result[0] == '织纱':
                self.setWindowTitle('货物加工收发记录 - 织纱')
            
            self.customer_name.setText(result[1] or '')
            
            if result[3]:
                self.customer_send_date.setDate(QDate.fromString(result[3], 'yyyy-MM-dd'))
            
            self.customer_send_method.setCurrentText(result[4] or '快递')
            self.customer_send_qty.setText(str(result[5]) if result[5] else '')
            self.factory_receive_qty.setText(str(result[6]) if result[6] else '')
            
            if result[7]:
                self.factory_send_date.setDate(QDate.fromString(result[7], 'yyyy-MM-dd'))
            
            self.factory_send_method.setCurrentText(result[8] or '快递')
            self.factory_send_qty.setText(str(result[9]) if result[9] else '')
            self.customer_receive_qty.setText(str(result[10]) if result[10] else '')
            
            # 重新计算差异
            self._calculate_diffs()

    def save(self):
        """保存数据"""
        # 验证必填项
        if not self.customer_name.text().strip():
            QMessageBox.warning(self, '警告', '客户名称不能为空！')
            return
        
        if not self.customer_send_qty.text().strip():
            QMessageBox.warning(self, '警告', '客户发货数量不能为空！')
            return
        
        # 计算差异值
        try:
            customer_send_qty = int(self.customer_send_qty.text() or 0)
            factory_receive_qty = int(self.factory_receive_qty.text() or 0)
            factory_send_qty = int(self.factory_send_qty.text() or 0)
            customer_receive_qty = int(self.customer_receive_qty.text() or 0)
            
            diff_receive = customer_send_qty - factory_receive_qty
            diff_factory_customer = factory_send_qty - customer_receive_qty
        except ValueError:
            QMessageBox.warning(self, '错误', '数量必须是整数！')
            return
        
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if self.mode == 'add':
            # 插入新记录
            query = '''
                INSERT INTO goods_processing_v2 (
                    goods_type, customer_name, customer_send_date,
                    customer_send_method, customer_send_qty, factory_receive_qty, diff_receive,
                    factory_send_date, factory_send_method, factory_send_qty,
                    customer_receive_qty, diff_factory_customer,
                    created_by, created_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            
            params = (
                self.goods_type.currentText(),
                self.customer_name.text().strip(),
                self.customer_send_date.date().toString('yyyy-MM-dd'),
                self.customer_send_method.currentText(),
                customer_send_qty,
                factory_receive_qty,
                diff_receive,
                self.factory_send_date.date().toString('yyyy-MM-dd'),
                self.factory_send_method.currentText(),
                factory_send_qty,
                customer_receive_qty,
                diff_factory_customer,
                self.username,
                current_time
            )
        else:
            # 更新记录
            query = '''
                UPDATE goods_processing_v2 SET
                    customer_name=?, customer_send_date=?,
                    customer_send_method=?, customer_send_qty=?, factory_receive_qty=?, diff_receive=?,
                    factory_send_date=?, factory_send_method=?, factory_send_qty=?,
                    customer_receive_qty=?, diff_factory_customer=?,
                    modified_by=?, modified_date=?
                WHERE id=?
            '''
            
            params = (
                self.customer_name.text().strip(),
                self.customer_send_date.date().toString('yyyy-MM-dd'),
                self.customer_send_method.currentText(),
                customer_send_qty,
                factory_receive_qty,
                diff_receive,
                self.factory_send_date.date().toString('yyyy-MM-dd'),
                self.factory_send_method.currentText(),
                factory_send_qty,
                customer_receive_qty,
                diff_factory_customer,
                self.username,
                current_time,
                self.record_id
            )
        
        if self.db_manager.execute_query(query, params):
            QMessageBox.information(self, '成功', '数据保存成功！')
            self.accept()
        else:
            QMessageBox.critical(self, '错误', '数据保存失败！')