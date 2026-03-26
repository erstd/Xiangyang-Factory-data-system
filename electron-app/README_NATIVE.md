# 向阳厂管理系统 - 纯Electron版本

## 项目结构

```
electron-app/
├── pages/           # HTML页面
│   ├── login.html   # 登录页面
│   ├── main.html    # 主页面
│   ├── goods.html   # 货品加工收发
│   └── wage.html    # 工资核算
├── js/              # JavaScript文件
│   ├── login.js
│   ├── main.js
│   ├── goods.js
│   └── wage.js
├── styles/          # CSS样式
│   ├── common.css   # 公共样式
│   ├── login.css
│   ├── main.css
│   ├── goods.css
│   └── wage.css
├── main.js          # Electron主进程
├── preload.js       # 预加载脚本
└── package.json
```

## 技术栈

- Electron - 桌面应用框架
- 原生HTML/CSS/JavaScript - 无任何前端框架
- Fetch API - HTTP请求

## 运行方式

1. 安装依赖：
```bash
cd electron-app
npm install
```

2. 启动应用：
```bash
npm start
```

3. 开发模式（带开发者工具）：
```bash
npm run dev
```

## 功能说明

- 登录页面：用户认证
- 货品加工收发：管理货物进出记录
- 工资核算：管理车间工资
- 权限控制：财务和工厂角色

## API接口

后端API地址：http://localhost:8000

需要先启动Python后端服务。
