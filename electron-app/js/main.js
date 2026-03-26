// 检查登录状态
const user = JSON.parse(localStorage.getItem('user') || 'null');
if (!user) {
  window.location.href = 'login.html';
}

// 显示用户信息
const userInfo = document.getElementById('userInfo');
const roleText = user.role === 'finance' ? '财务' : '工厂';
userInfo.textContent = `欢迎，${user.username} (${roleText})`;

// 显示财务专属标签
if (user.role === 'finance') {
  document.getElementById('customerTab').style.display = 'block';
  document.getElementById('profitTab').style.display = 'block';
}

// 标签切换
const tabBtns = document.querySelectorAll('.tab-btn');
const tabPanes = document.querySelectorAll('.tab-pane');

tabBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    const tabName = btn.dataset.tab;

    // 移除所有active类
    tabBtns.forEach(b => b.classList.remove('active'));
    tabPanes.forEach(p => p.classList.remove('active'));

    // 添加active类
    btn.classList.add('active');
    document.getElementById(`${tabName}-tab`).classList.add('active');
  });
});

// 刷新功能
function handleRefresh() {
  const activePane = document.querySelector('.tab-pane.active iframe');
  if (activePane) {
    activePane.contentWindow.location.reload();
  }
  alert('数据刷新成功');
}

// 退出登录
function handleLogout() {
  if (confirm('确定要退出登录吗？')) {
    localStorage.removeItem('user');
    window.location.href = 'login.html';
  }
}

// 更新时间
function updateTime() {
  const now = new Date();
  const timeStr = now.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  });
  document.getElementById('currentTime').textContent = timeStr;
}

updateTime();
setInterval(updateTime, 1000);
