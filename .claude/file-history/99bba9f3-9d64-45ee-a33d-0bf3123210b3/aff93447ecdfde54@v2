<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <div class="icon">🏭</div>
        <h1 class="title">向阳厂管理系统</h1>
        <p class="subtitle">Factory Management System</p>
      </div>

      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="rules"
        class="login-form"
        @submit.prevent="handleLogin"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            size="large"
            prefix-icon="User"
            clearable
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            size="large"
            prefix-icon="Lock"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>

        <el-button
          type="primary"
          size="large"
          class="login-button"
          :loading="loading"
          @click="handleLogin"
        >
          登 录
        </el-button>
      </el-form>

      <div class="login-tip">
        默认账号: admin/admin123 或 factory/factory123
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { login } from '@/api';
import { useUserStore } from '@/store/user';

const router = useRouter();
const userStore = useUserStore();
const loginFormRef = ref(null);
const loading = ref(false);

const loginForm = reactive({
  username: '',
  password: ''
});

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
};

const handleLogin = async () => {
  if (!loginFormRef.value) return;

  await loginFormRef.value.validate(async (valid) => {
    if (!valid) return;

    loading.value = true;
    try {
      const response = await login(loginForm.username, loginForm.password);

      userStore.setUser({
        username: response.username,
        role: response.role,
        token: response.token
      });

      ElMessage.success('登录成功');
      router.push('/main');
    } catch (error) {
      console.error('登录失败:', error);
    } finally {
      loading.value = false;
    }
  });
};
</script>

<style scoped>
.login-container {
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  width: 420px;
  padding: 40px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.title {
  font-size: 24px;
  font-weight: 600;
  color: #212121;
  margin-bottom: 8px;
}

.subtitle {
  font-size: 14px;
  color: #757575;
}

.login-form {
  margin-top: 24px;
}

.login-button {
  width: 100%;
  margin-top: 8px;
  font-size: 16px;
  font-weight: 600;
  height: 46px;
}

.login-tip {
  margin-top: 20px;
  text-align: center;
  font-size: 13px;
  color: #9E9E9E;
}
</style>
