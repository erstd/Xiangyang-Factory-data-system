#!/bin/bash

echo "开始打包向阳厂管理系统..."

# 1. 打包Python后端
echo "打包Python后端..."
source .venv/bin/activate
pyinstaller --onefile --name xiangyang-backend api_server.py

# 2. 打包Electron前端
echo "打包Electron前端..."
cd electron-app
npm run build:win

# 3. 创建发布目录
echo "创建发布包..."
cd ..
mkdir -p release/xiangyang-factory
cp dist/xiangyang-backend.exe release/xiangyang-factory/
cp xiangyang_factory.db release/xiangyang-factory/
cp -r electron-app/dist-electron/* release/xiangyang-factory/

# 4. 创建启动脚本
cat > release/xiangyang-factory/start.bat << 'EOF'
@echo off
echo 启动向阳厂管理系统...
start /B xiangyang-backend.exe
timeout /t 2 /nobreak >nul
start "向阳厂管理系统" "向阳厂管理系统.exe"
EOF

echo "打包完成！发布包位于: release/xiangyang-factory/"
