from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
import jwt
import os
from functools import wraps

app = Flask(__name__)
CORS(app)

# 配置
app.config['SECRET_KEY'] = 'xiangyang-factory-secret-key-2024'
DB_PATH = os.path.join(os.path.dirname(__file__), 'xiangyang_factory.db')


def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def token_required(f):
    """JWT 认证装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': '缺少认证令牌'}), 401

        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            request.user = data
        except:
            return jsonify({'message': '无效的认证令牌'}), 401

        return f(*args, **kwargs)

    return decorated


@app.route('/api/auth/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': '用户名和密码不能为空'}), 400

    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE username = ? AND password = ?',
        (username, password)
    ).fetchone()
    conn.close()

    if not user:
        return jsonify({'message': '用户名或密码错误'}), 401

    # 生成 JWT token
    token = jwt.encode({
        'username': user['username'],
        'role': user['role']
    }, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({
        'token': token,
        'username': user['username'],
        'role': user['role']
    })


@app.route('/api/goods', methods=['GET'])
@token_required
def get_goods():
    """获取货品列表"""
    goods_type = request.args.get('goods_type', '')
    keyword = request.args.get('keyword', '')

    conn = get_db_connection()

    query = '''
        SELECT id, goods_type, customer_name, customer_style_no,
               customer_send_qty, factory_receive_qty, diff_receive,
               factory_send_qty, customer_receive_qty, diff_factory_customer,
               COALESCE(modified_date, created_date) as modified_date,
               COALESCE(modified_by, created_by, '-') as modified_by
        FROM goods_processing_v2
        WHERE 1=1
    '''
    params = []

    if goods_type:
        query += ' AND goods_type = ?'
        params.append(goods_type)

    if keyword:
        query += ' AND (customer_name LIKE ? OR customer_style_no LIKE ?)'
        params.append(f'%{keyword}%')
        params.append(f'%{keyword}%')

    query += ' ORDER BY id DESC'

    goods = conn.execute(query, params).fetchall()
    conn.close()

    return jsonify([dict(row) for row in goods])


@app.route('/api/goods', methods=['POST'])
@token_required
def add_goods():
    """添加货品记录"""
    data = request.get_json()
    username = request.user['username']
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO goods_processing_v2 (
            goods_type, customer_name, customer_style_no, customer_send_date,
            customer_send_method, customer_send_qty, factory_receive_qty, diff_receive,
            factory_send_date, factory_send_method, factory_send_qty,
            customer_receive_qty, diff_factory_customer,
            created_by, created_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('goods_type'),
        data.get('customer_name'),
        data.get('customer_style_no'),
        data.get('customer_send_date'),
        data.get('customer_send_method'),
        data.get('customer_send_qty', 0),
        data.get('factory_receive_qty', 0),
        data.get('diff_receive', 0),
        data.get('factory_send_date'),
        data.get('factory_send_method'),
        data.get('factory_send_qty', 0),
        data.get('customer_receive_qty', 0),
        data.get('diff_factory_customer', 0),
        username,
        current_time
    ))
    conn.commit()
    conn.close()

    return jsonify({'message': '添加成功'}), 201


@app.route('/api/goods/<int:goods_id>', methods=['PUT'])
@token_required
def update_goods(goods_id):
    """更新货品记录"""
    data = request.get_json()
    username = request.user['username']
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = get_db_connection()
    conn.execute('''
        UPDATE goods_processing_v2 SET
            customer_name=?, customer_style_no=?, customer_send_date=?,
            customer_send_method=?, customer_send_qty=?, factory_receive_qty=?, diff_receive=?,
            factory_send_date=?, factory_send_method=?, factory_send_qty=?,
            customer_receive_qty=?, diff_factory_customer=?,
            modified_by=?, modified_date=?
        WHERE id=?
    ''', (
        data.get('customer_name'),
        data.get('customer_style_no'),
        data.get('customer_send_date'),
        data.get('customer_send_method'),
        data.get('customer_send_qty', 0),
        data.get('factory_receive_qty', 0),
        data.get('diff_receive', 0),
        data.get('factory_send_date'),
        data.get('factory_send_method'),
        data.get('factory_send_qty', 0),
        data.get('customer_receive_qty', 0),
        data.get('diff_factory_customer', 0),
        username,
        current_time,
        goods_id
    ))
    conn.commit()
    conn.close()

    return jsonify({'message': '更新成功'})


@app.route('/api/goods/<int:goods_id>', methods=['DELETE'])
@token_required
def delete_goods(goods_id):
    """删除货品记录"""
    conn = get_db_connection()
    conn.execute('DELETE FROM goods_processing_v2 WHERE id=?', (goods_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': '删除成功'})


@app.route('/api/wage', methods=['GET'])
@token_required
def get_wage():
    """获取工资列表"""
    conn = get_db_connection()
    wages = conn.execute('''
        SELECT id, workshop_name, knitting_qty, knitting_wage,
               overlock_goods_type, overlock_wage,
               hand_sewing_goods_type, hand_sewing_wage,
               created_by, created_date
        FROM wage_calculation
        ORDER BY id DESC
    ''').fetchall()
    conn.close()

    return jsonify([dict(row) for row in wages])


@app.route('/api/wage', methods=['POST'])
@token_required
def add_wage():
    """添加工资记录"""
    data = request.get_json()
    username = request.user['username']
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO wage_calculation (
            workshop_name, processing_date, knitting_qty, knitting_wage,
            overlock_employee, overlock_goods_type, overlock_qty, overlock_wage,
            hand_sewing_employee, hand_sewing_goods_type, hand_sewing_qty, hand_sewing_wage,
            created_by, created_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('workshop_name'),
        data.get('processing_date'),
        data.get('knitting_qty', 0),
        data.get('knitting_wage', 0.0),
        data.get('overlock_employee'),
        data.get('overlock_goods_type'),
        data.get('overlock_qty', 0),
        data.get('overlock_wage', 0.0),
        data.get('hand_sewing_employee'),
        data.get('hand_sewing_goods_type'),
        data.get('hand_sewing_qty', 0),
        data.get('hand_sewing_wage', 0.0),
        username,
        current_time
    ))
    conn.commit()
    conn.close()

    return jsonify({'message': '添加成功'}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
