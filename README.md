# 种呱得呱助手 RanaCard Assistant

面向玩家与创作者的游戏数据编辑器。专注于“修改与分享”游戏内数据：支持编辑卡牌、挂件、地图事件、开局效果等内容，并一键发布到分享页，让其他玩家直接导入体验。

## 在线使用
- 立即体验：<https://rana.jie65535.top/>

## 功能介绍
- 数据类型：卡牌（Cards）、挂件（Pendants）、地图事件（Map Events）、开局效果（Begin Effects）
- 编辑体验：表格 + 抽屉表单，所见即所得；可切换“编辑 JSON”模式
- 搜索筛选：按 ID / 名称 / 效果 搜索，内置分类与条件过滤
- 导入导出：本地一键导入、导出；导出前提供基础校验
- 基线数据：内置官方数据作为起点，便于对照修改
- 社区分享：发布你的改动，浏览他人作品，一键导入；支持带管理令牌的删除

## 部署
- Docker Compose（推荐）：
  ```bash
  git clone https://github.com/jie65535/RanaCard.git
  cd RanaCard
  docker compose up -d --build
  ```
- 访问：`http://127.0.0.1:8080`
- 更新：`git pull && docker compose up -d --build`
- 生产建议：保持仅绑定本机回环地址，通过你的 Nginx 反向代理对外服务

## 开发
- 前置：Python 3.10+、Node.js 18+（或直接用 Docker）
- 后端：
  ```bash
  cd server
  pip install -r requirements.txt
  uvicorn main:app --reload
  ```
- 前端：
  ```bash
  cd ui
  npm i
  npm run dev
  ```
- 可选：`ui/.env` 配置 `VITE_API_BASE=http://127.0.0.1:8000`

## 贡献
- 欢迎提交 Issue / PR，共建更好用的编辑与分享体验
- 流程建议：Fork → 新建分支 → 提交改动 → 发起 PR
- 代码风格：Python 遵循 PEP 8；前端使用 TypeScript，中文文案保持一致风格

## 许可证
本项目以 GPL-3.0 许可证开源，详见根目录 `LICENSE`。
