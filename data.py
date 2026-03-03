import sqlite3
from datetime import datetime


def get_database_path():
    """获取数据库文件的正确路径（支持打包后的环境）"""
    if getattr(sys, 'frozen', False):
        # 打包后的环境 - 可执行文件所在目录
        base_path = os.path.dirname(sys.executable)
    else:
        # 开发环境 - 当前脚本所在目录
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    db_path = os.path.join(base_path, 'xiangyang_factory.db')
    
    # 如果数据库不存在，创建初始数据库
    if not os.path.exists(db_path):
        create_initial_database(db_path)
    
    return db_path

class DatabaseManager:
    """数据库管理类"""
    
    def __init__(self, db_name='xiangyang_factory.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """创建数据库表"""

        # ========== 修正1: 创建 goods_processing_v2 表 ==========
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS goods_processing_v2 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goods_type TEXT NOT NULL CHECK(goods_type IN ('织纱', '织片')),
                customer_name TEXT NOT NULL,
                customer_send_date TEXT,
                customer_send_method TEXT,
                customer_send_qty INTEGER DEFAULT 0,
                factory_receive_qty INTEGER DEFAULT 0,
                diff_receive INTEGER,
                factory_send_date TEXT,
                factory_send_method TEXT,
                factory_send_qty INTEGER DEFAULT 0,
                customer_receive_qty INTEGER DEFAULT 0,
                diff_factory_customer INTEGER,
                created_by TEXT,
                created_date TEXT,
                modified_by TEXT,
                modified_date TEXT
            )
        ''')
        
        # ========== 修正2: 用户表应该单独创建 ==========
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                created_date TEXT
            )
        ''')
        
        # 工资核算表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS wage_calculation (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workshop_name TEXT,
                processing_date TEXT,
                knitting_qty INTEGER,
                deduction_amount REAL,
                deduction_remark TEXT,
                knitting_wage REAL,
                overlock_employee TEXT,
                overlock_qty INTEGER,
                overlock_wage REAL,
                hand_sewing_employee TEXT,
                hand_sewing_qty INTEGER,
                hand_sewing_wage REAL,
                outsourcing_date TEXT,
                outsourcing_unit TEXT,
                outsourcing_qty INTEGER,
                outsourcing_wage REAL,
                wage_diff INTEGER,
                wage_diff_amount REAL,
                inspection_employee TEXT,
                inspection_qty INTEGER,
                inspection_unit_price REAL,
                inspection_wage REAL,
                hourly_employee TEXT,
                hourly_time REAL,
                hourly_unit_price REAL,
                hourly_amount REAL,
                created_by TEXT,
                created_date TEXT,
                modified_by TEXT,
                modified_date TEXT
            )
        ''')
        
        # 利润核算表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS profit_calculation (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                overlock_unit_price REAL,
                hand_sewing_unit_price REAL,
                knitting_unit_price REAL,
                outsourcing_price REAL,
                transport_unit_price REAL,
                management_unit_price REAL,
                rent_utility_unit_price REAL,
                tax_unit_price REAL,
                net_profit_diff REAL,
                net_profit_amount REAL,
                goods_id INTEGER,
                created_by TEXT,
                created_date TEXT,
                modified_by TEXT,
                modified_date TEXT,
                FOREIGN KEY (goods_id) REFERENCES goods_processing(id)
            )
        ''')
        
        # 初始化默认用户
        self.cursor.execute("SELECT * FROM users WHERE username='admin'")
        if not self.cursor.fetchone():
            self.cursor.execute('''
                INSERT INTO users (username, password, role, created_date) 
                VALUES (?, ?, ?, ?)
            ''', ('admin', 'admin123', 'finance', datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        
        self.cursor.execute("SELECT * FROM users WHERE username='factory'")
        if not self.cursor.fetchone():
            self.cursor.execute('''
                INSERT INTO users (username, password, role, created_date) 
                VALUES (?, ?, ?, ?)
            ''', ('factory', 'factory123', 'factory', datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        
        self.conn.commit()
    
    def execute_query(self, query, params=None):
        """执行查询"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"数据库错误: {e}")
            return False
    
    def fetch_all(self, query, params=None):
        """获取所有结果"""
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def fetch_one(self, query, params=None):
        """获取单个结果"""
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchone()
    
    def close(self):
        """关闭数据库连接"""
        self.conn.close()
