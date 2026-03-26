<template>
  <div class="main-container">
    <!-- 顶部工具栏 -->
    <div class="header">
      <div class="header-left">
        <span class="logo">🏭</span>
        <span class="app-name">向阳厂管理系统</span>
      </div>
      <div class="header-right">
        <span class="user-info">
          欢迎，{{ userStore.username }} ({{ roleText }})
        </span>
        <el-button type="primary" size="default" @click="handleRefresh">
          刷新
        </el-button>
        <el-button size="default" @click="handleLogout">
          退出
        </el-button>
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="content">
      <el-tabs v-model="activeTab" type="card" class="main-tabs">
        <el-tab-pane label="📦 货品加工收发" name="goods">
          <GoodsProcessing />
        </el-tab-pane>

        <el-tab-pane label="💰 工资核算" name="wage">
          <WageCalculation />
        </el-tab-pane>

        <el-tab-pane
          v-if="userStore.isFinance"
          label="🤝 客户结算"
          name="customer"
        >
          <div class="placeholder">客户结算功能开发中...</div>
        </el-tab-pane>

        <el-tab-pane
          v-if="userStore.isFinance"
          label="📊 利润核算"
          name="profit"
        >
          <div class="placeholder">利润核算功能开发中...</div>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- 底部状态栏 -->
    <div class="footer">
      <span>{{ currentTime }}</span>
      <span class="status">● 数据库正常</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessageBox, ElMessage } from 'element-plus';
import { useUserStore } from '@/store/user';
import GoodsProcessing from '@/components/GoodsProcessing.vue';
import WageCalculation from '@/components/WageCalculation.vue';

const router = useRouter();
const userStore = useUserStore();
const activeTab = ref('goods');
const currentTime = ref('');

const roleText = computed(() => {
  return userStore.role === 'finance' ? '财务' : '工厂';
});

let timer = null;

const updateTime = () => {
  const now = new Date();
  currentTime.value = now.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  });
};

const handleRefresh = () => {
  ElMessage.success('数据刷新成功');
  // 触发当前标签页的刷新
  window.location.reload();
};

const handleLogout = () => {
  ElMessageBox.confirm('确定要退出登录吗？', '确认退出', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    userStore.clearUser();
    router.push('/login');
    ElMessage.success('已退出登录');
  }).catch(() => {});
};

onMounted(() => {
  updateTime();
  timer = setInterval(updateTime, 1000);
});

onUnmounted(() => {
  if (timer) {
    clearInterval(timer);
  }
});
</script>

<style scoped>
.main-container {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #FAFAFA;
}

.header {
  height: 64px;
  background: white;
  border-bottom: 1px solid #E0E0E0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo {
  font-size: 28px;
}

.app-name {
  font-size: 18px;
  font-weight: 600;
  color: #212121;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-info {
  font-size: 14px;
  color: #616161;
  font-weight: 500;
}

.content {
  flex: 1;
  overflow: hidden;
  padding: 16px;
}

.main-tabs {
  height: 100%;
}

.main-tabs :deep(.el-tabs__content) {
  height: calc(100% - 50px);
  overflow: auto;
}

.placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 400px;
  font-size: 18px;
  color: #9E9E9E;
}

.footer {
  height: 36px;
  background: white;
  border-top: 1px solid #E0E0E0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  font-size: 13px;
  color: #757575;
}

.status {
  color: #4CAF50;
  font-weight: 600;
}
</style>
