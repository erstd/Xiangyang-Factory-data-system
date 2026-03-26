import axios from 'axios';
import { ElMessage } from 'element-plus';

const API_BASE_URL = 'http://localhost:5000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器
apiClient.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 响应拦截器
apiClient.interceptors.response.use(
  response => {
    return response.data;
  },
  error => {
    if (error.response) {
      const { status, data } = error.response;
      if (status === 401) {
        localStorage.removeItem('token');
        window.location.href = '#/login';
        ElMessage.error('登录已过期，请重新登录');
      } else {
        ElMessage.error(data.message || '请求失败');
      }
    } else {
      ElMessage.error('网络错误，请检查后端服务是否启动');
    }
    return Promise.reject(error);
  }
);

export default apiClient;
