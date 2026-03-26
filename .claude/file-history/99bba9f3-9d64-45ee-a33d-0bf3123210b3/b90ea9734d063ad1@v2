import request from './request';

// 用户登录
export const login = (username, password) => {
  return request.post('/auth/login', { username, password });
};

// 获取货品列表
export const getGoodsList = (params) => {
  return request.get('/goods', { params });
};

// 添加货品记录
export const addGoods = (data) => {
  return request.post('/goods', data);
};

// 更新货品记录
export const updateGoods = (id, data) => {
  return request.put(`/goods/${id}`, data);
};

// 删除货品记录
export const deleteGoods = (id) => {
  return request.delete(`/goods/${id}`);
};

// 获取工资列表
export const getWageList = (params) => {
  return request.get('/wage', { params });
};

// 添加工资记录
export const addWage = (data) => {
  return request.post('/wage', data);
};
