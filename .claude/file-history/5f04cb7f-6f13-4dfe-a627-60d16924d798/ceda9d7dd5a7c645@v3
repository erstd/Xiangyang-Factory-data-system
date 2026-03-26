const API_BASE = 'http://localhost:5000';
const user = JSON.parse(localStorage.getItem('user') || 'null');

let tableData = [];
let selectedRows = [];
let dialogMode = 'add';
let editingId = null;

// 页面加载时获取数据
window.addEventListener('load', () => {
  loadData();
  setupEventListeners();
});

// 设置事件监听
function setupEventListeners() {
  // 全选checkbox
  document.getElementById('selectAll').addEventListener('change', (e) => {
    const checkboxes = document.querySelectorAll('#tableBody input[type="checkbox"]');
    checkboxes.forEach(cb => cb.checked = e.target.checked);
    updateSelectedRows();
  });

  // 货物类型变化时自动搜索
  document.getElementById('goodsType').addEventListener('change', loadData);

  // 数量输入框变化时计算差异
  ['customerSendQty', 'factoryReceiveQty', 'factorySendQty', 'customerReceiveQty'].forEach(id => {
    document.getElementById(id).addEventListener('input', calculateDiff);
  });
}

// 加载数据
async function loadData() {
  try {
    const goodsType = document.getElementById('goodsType').value;
    const keyword = document.getElementById('keyword').value;

    let url = `${API_BASE}/api/goods`;
    const params = new URLSearchParams();
    if (goodsType) params.append('goods_type', goodsType);
    if (keyword) params.append('keyword', keyword);
    if (params.toString()) url += '?' + params.toString();

    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${user.token}`
      }
    });

    if (response.ok) {
      tableData = await response.json();
      renderTable();
      renderStatistics();
    } else {
      alert('加载数据失败');
    }
  } catch (error) {
    console.error('加载数据错误:', error);
    alert('加载数据失败');
  }
}

// 渲染表格
function renderTable() {
  const tbody = document.getElementById('tableBody');
  tbody.innerHTML = '';

  tableData.forEach(row => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><input type="checkbox" data-id="${row.id}"></td>
      <td>${row.id}</td>
      <td>${row.goods_type}</td>
      <td>${row.customer_name}</td>
      <td>${row.customer_style_no || ''}</td>
      <td style="text-align:right">${row.customer_send_qty}</td>
      <td style="text-align:right">${row.factory_receive_qty}</td>
      <td style="text-align:right;color:${getDiffColor(row.diff_receive)}">${row.diff_receive}</td>
      <td style="text-align:right">${row.factory_send_qty}</td>
      <td style="text-align:right">${row.customer_receive_qty}</td>
      <td style="text-align:right;color:${getDiffColor(row.diff_factory_customer)}">${row.diff_factory_customer}</td>
      <td>${row.modified_date || ''}</td>
      <td>${row.modified_by || ''}</td>
    `;

    tr.querySelector('input[type="checkbox"]').addEventListener('change', updateSelectedRows);
    tbody.appendChild(tr);
  });
}

// 渲染统计信息
function renderStatistics() {
  const stats = {
    totalCustomerSend: 0,
    totalFactoryReceive: 0,
    totalDiffReceive: 0,
    totalFactorySend: 0,
    totalCustomerReceive: 0,
    totalDiffFactoryCustomer: 0
  };

  tableData.forEach(row => {
    stats.totalCustomerSend += row.customer_send_qty || 0;
    stats.totalFactoryReceive += row.factory_receive_qty || 0;
    stats.totalFactorySend += row.factory_send_qty || 0;
    stats.totalCustomerReceive += row.customer_receive_qty || 0;
  });

  stats.totalDiffReceive = stats.totalCustomerSend - stats.totalFactoryReceive;
  stats.totalDiffFactoryCustomer = stats.totalFactorySend - stats.totalCustomerReceive;

  const statsDiv = document.getElementById('statistics');
  statsDiv.innerHTML = `
    <span class="tag tag-info">总客户发货: ${stats.totalCustomerSend}</span>
    <span class="tag tag-info">总工厂收货: ${stats.totalFactoryReceive}</span>
    <span class="tag ${stats.totalDiffReceive !== 0 ? 'tag-warning' : 'tag-success'}">总收发差异: ${stats.totalDiffReceive}</span>
    <span class="tag tag-info">总工厂出货: ${stats.totalFactorySend}</span>
    <span class="tag tag-info">总客户收货: ${stats.totalCustomerReceive}</span>
    <span class="tag ${stats.totalDiffFactoryCustomer !== 0 ? 'tag-warning' : 'tag-success'}">总厂客差异: ${stats.totalDiffFactoryCustomer}</span>
  `;
}

// 更新选中行
function updateSelectedRows() {
  const checkboxes = document.querySelectorAll('#tableBody input[type="checkbox"]:checked');
  selectedRows = Array.from(checkboxes).map(cb => {
    const id = parseInt(cb.dataset.id);
    return tableData.find(row => row.id === id);
  });

  // 更新删除按钮状态
  const deleteBtn = document.getElementById('deleteBtn');
  deleteBtn.disabled = !(user.role === 'finance' && selectedRows.length > 0);
}

// 获取差异颜色
function getDiffColor(value) {
  if (value < 0) return '#F44336';
  if (value > 0) return '#4CAF50';
  return '#616161';
}

// 搜索
function handleSearch() {
  loadData();
}

// 重置
function handleReset() {
  document.getElementById('goodsType').value = '';
  document.getElementById('keyword').value = '';
  loadData();
}

// 新增
function handleAdd() {
  dialogMode = 'add';
  editingId = null;
  document.getElementById('dialogTitle').textContent = '新增货品记录';
  document.getElementById('goodsTypeSection').style.display = 'block';
  resetForm();
  document.getElementById('dialog').classList.add('show');
}

// 修改
function handleEdit() {
  if (selectedRows.length === 0) {
    alert('请先选择一条记录');
    return;
  }
  if (selectedRows.length > 1) {
    alert('只能选择一条记录进行编辑');
    return;
  }

  dialogMode = 'edit';
  const row = selectedRows[0];
  editingId = row.id;
  document.getElementById('dialogTitle').textContent = '修改货品记录';
  document.getElementById('goodsTypeSection').style.display = 'none';

  // 填充表单
  document.getElementById('formGoodsType').value = row.goods_type;
  document.getElementById('customerName').value = row.customer_name;
  document.getElementById('customerStyleNo').value = row.customer_style_no || '';
  document.getElementById('customerSendDate').value = row.customer_send_date || '';
  document.getElementById('customerSendMethod').value = row.customer_send_method || '快递';
  document.getElementById('customerSendQty').value = row.customer_send_qty || 0;
  document.getElementById('factoryReceiveQty').value = row.factory_receive_qty || 0;
  document.getElementById('factorySendDate').value = row.factory_send_date || '';
  document.getElementById('factorySendMethod').value = row.factory_send_method || '快递';
  document.getElementById('factorySendQty').value = row.factory_send_qty || 0;
  document.getElementById('customerReceiveQty').value = row.customer_receive_qty || 0;

  calculateDiff();
  document.getElementById('dialog').classList.add('show');
}

// 删除
async function handleDelete() {
  if (selectedRows.length === 0) {
    alert('请先选择要删除的记录');
    return;
  }

  if (!confirm('确定要删除选中的记录吗？')) {
    return;
  }

  try {
    for (const row of selectedRows) {
      const response = await fetch(`${API_BASE}/api/goods/${row.id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${user.token}`
        }
      });

      if (!response.ok) {
        throw new Error('删除失败');
      }
    }

    alert('删除成功');
    loadData();
  } catch (error) {
    console.error('删除错误:', error);
    alert('删除失败');
  }
}

// 提交表单
async function handleSubmit() {
  const form = document.getElementById('goodsForm');
  if (!form.checkValidity()) {
    form.reportValidity();
    return;
  }

  const data = {
    goods_type: document.getElementById('formGoodsType').value,
    customer_name: document.getElementById('customerName').value,
    customer_style_no: document.getElementById('customerStyleNo').value,
    customer_send_date: document.getElementById('customerSendDate').value,
    customer_send_method: document.getElementById('customerSendMethod').value,
    customer_send_qty: parseInt(document.getElementById('customerSendQty').value) || 0,
    factory_receive_qty: parseInt(document.getElementById('factoryReceiveQty').value) || 0,
    factory_send_date: document.getElementById('factorySendDate').value,
    factory_send_method: document.getElementById('factorySendMethod').value,
    factory_send_qty: parseInt(document.getElementById('factorySendQty').value) || 0,
    customer_receive_qty: parseInt(document.getElementById('customerReceiveQty').value) || 0,
    diff_receive: parseInt(document.getElementById('customerSendQty').value) - parseInt(document.getElementById('factoryReceiveQty').value),
    diff_factory_customer: parseInt(document.getElementById('factorySendQty').value) - parseInt(document.getElementById('customerReceiveQty').value)
  };

  try {
    let response;
    if (dialogMode === 'add') {
      response = await fetch(`${API_BASE}/api/goods`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${user.token}`
        },
        body: JSON.stringify(data)
      });
    } else {
      response = await fetch(`${API_BASE}/api/goods/${editingId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${user.token}`
        },
        body: JSON.stringify(data)
      });
    }

    if (response.ok) {
      alert(dialogMode === 'add' ? '添加成功' : '修改成功');
      closeDialog();
      loadData();
    } else {
      alert('保存失败');
    }
  } catch (error) {
    console.error('保存错误:', error);
    alert('保存失败');
  }
}

// 关闭对话框
function closeDialog() {
  document.getElementById('dialog').classList.remove('show');
  resetForm();
}

// 重置表单
function resetForm() {
  document.getElementById('goodsForm').reset();
  document.getElementById('formGoodsType').value = '织纱';
  document.getElementById('customerSendMethod').value = '快递';
  document.getElementById('factorySendMethod').value = '快递';
  calculateDiff();
}

// 计算差异
function calculateDiff() {
  const customerSend = parseInt(document.getElementById('customerSendQty').value) || 0;
  const factoryReceive = parseInt(document.getElementById('factoryReceiveQty').value) || 0;
  const factorySend = parseInt(document.getElementById('factorySendQty').value) || 0;
  const customerReceive = parseInt(document.getElementById('customerReceiveQty').value) || 0;

  const diffReceive = customerSend - factoryReceive;
  const diffFactoryCustomer = factorySend - customerReceive;

  const diffReceiveInput = document.getElementById('diffReceive');
  const diffFactoryCustomerInput = document.getElementById('diffFactoryCustomer');

  diffReceiveInput.value = diffReceive;
  diffReceiveInput.style.color = getDiffColor(diffReceive);

  diffFactoryCustomerInput.value = diffFactoryCustomer;
  diffFactoryCustomerInput.style.color = getDiffColor(diffFactoryCustomer);
}
