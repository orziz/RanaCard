# 种呱得呱助手（M1）

本目录为前端（Vue 3 + Vite + TypeScript + Element Plus）。

## 开发

- 安装依赖：`npm i` 或 `pnpm i` 或 `yarn`
- 启动开发：`npm run dev`
- 配置后端地址：默认 `http://localhost:8000`，可通过 `.env` 设置 `VITE_API_BASE`

## 功能（M1）

- 自动加载官方数据（需后端 `/api/data/*`，兼容 `/baseline/*`）
- 本地上传：加密文件 `.../RanaCard_Data/StreamingAssets/*.json`（游戏目录）
- 列表查看、搜索（含效果）、排序；编辑常用字段与高级 JSON
- 导出加密文件（服务端加密）、后端校验

## Docker 部署

- 一键启动（仓库根目录）：`docker compose up -d --build`
- 端口绑定：默认绑定到本机 `127.0.0.1:8080`，通过外部 Nginx 对外暴露
- 说明：
  - 前端（Nginx）容器监听 80，经 compose 绑定到本机 8080
  - `/api` 自动反代到后端容器（FastAPI，内部 8000）
  - 构建时 `VITE_API_BASE` 已设置为 `/`，前端使用同域 `/api` 调用后端

## 外部 Nginx 反代到 Docker（可选）

若服务器已有 Nginx，可将流量反代至本机 Docker：

```
server {
  listen 80;
  server_name your.domain.com;

  location / {
    proxy_pass http://127.0.0.1:8080/; # 前端 Nginx 容器映射端口
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
}
```
