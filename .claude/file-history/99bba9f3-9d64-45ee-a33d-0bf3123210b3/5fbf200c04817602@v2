# 向阳厂管理系统 - Electron 版

基于 Electron + Vue 3 + Element Plus 重构的工厂管理系统。

## 技术栈

### 前端
- **Electron**: 跨平台桌面应用框架
- **Vue 3**: 渐进式 JavaScript 框架
- **Element Plus**: Vue 3 UI 组件库
- **Vite**: 前端构建工具
- **Pinia**: 状态管理
- **Vue Router**: 路由管理
- **Axios**: HTTP 客户端

### 后端
- **Flask**: Python Web 框架
- **SQLite**: 轻量级数据库
- **JWT**: 身份认证

## 项目结构

```
xiangyang/
├── electron-app/              # Electron 前端项目
│   ├── src/
│   │   ├── api/              # API 接口
│   │   ├── assets/           # 静态资源
│   │   ├── components/       # Vue 组件
│   │   ├── router/           # 路由配置
│   │   ├── store/            # 状态管理
│   │   ├── views/            # 页面视图
│   │   ├── App.vue           # 根组件
│   │   └── main.js           # 入口文件
│   ├── main.js               # Electron 主进程
│   ├── preload.js            # 预加载脚本
│   ├── package.json          # 项目配置
│   └── vite.config.js        # Vite 配置
├── api_server.py             # Flask API 服务器
├── requirements.txt          # Python 依赖
└── xiangyang_factory.db      # SQLite 数据库
```

## 安装与运行

### 1. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 2. 启动后端 API 服务器

```bash
python api_server.py
```

后端服务将在 `http://localhost:5000` 启动。

### 3. 安装前端依赖

```bash
cd electron-app
npm install
```

### 4. 运行开发环境

```bash
npm run electron:dev
```

这将同时启动 Vite 开发服务器和 Electron 应用。

### 5. 打包应用

```bash
npm run electron:build
```

打包后的应用将在 `electron-app/dist-electron` 目录中。

## 默认账号

- **财务账号**: admin / admin123
- **工厂账号**: factory / factory123

## 功能模块

### 1. 登录系统
- 用户身份验证
- JWT Token 认证
- 角色权限管理

### 2. 货品加工收发
- 货品记录管理（新增、修改、删除）
- 客户发货/工厂收货跟踪
- 工厂出货/客户收货跟踪
- 差异统计与高亮显示
- 按类型和关键词搜索

### 3. 工资核算
- 工资记录管理
- 织片工资计算
- 套口工资计算
- 手缝工资计算

### 4. 客户结算（开发中）
- 客户货款结算

### 5. 利润核算（开发中）
- 利润统计与分析

## 开发说明

### API 接口

所有 API 接口都需要在请求头中携带 JWT Token：

```
Authorization: Bearer <token>
```

### 主要接口

- `POST /api/auth/login` - 用户登录
- `GET /api/goods` - 获取货品列表
- `POST /api/goods` - 添加货品记录
- `PUT /api/goods/:id` - 更新货品记录
- `DELETE /api/goods/:id` - 删除货品记录
- `GET /api/wage` - 获取工资列表
- `POST /api/wage` - 添加工资记录

### 权限说明

- **财务角色 (finance)**: 拥有所有功能的完整权限
- **工厂角色 (factory)**: 可以查看和新增记录，但不能删除

## 注意事项

1. 确保 Python 后端服务在前端启动前已经运行
2. 数据库文件 `xiangyang_factory.db` 需要与 `api_server.py` 在同一目录
3. 开发环境下，Vite 服务器运行在 5173 端口，Flask 服务器运行在 5000 端口
4. 生产环境打包时，需要确保后端 API 服务器可访问

## 相比 PyQt5 版本的改进

1. **更现代的 UI 设计**: 采用 Element Plus 组件库，界面更美观
2. **更好的跨平台支持**: Electron 可以轻松打包为 Windows、Mac、Linux 应用
3. **前后端分离**: 便于维护和扩展
4. **更灵活的部署**: 可以将前端部署为 Web 应用或桌面应用
5. **更好的开发体验**: 热重载、组件化开发

## 许可证

MIT
