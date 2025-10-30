# 种呱得呱助手（RanaCard Mod 数据编辑器）

面向中文玩家的网页工具：查看、搜索并编辑游戏加密数据（Card.json、Pendant.json），导出为游戏可识别的加密格式。后端保留加解密秘钥，前端不暴露。

## 功能
- 自动加载“官方数据”（仓库 Data/ 目录）
- 导入/导出游戏加密文件（Card.json、Pendant.json）
- 列表查看、排序、筛选；支持按 ID/名称/效果 搜索
- 侧边抽屉编辑“常用且存在差异”的字段；可切换“直接编辑 JSON”

## 目录结构
- `ui/` 前端（Vue 3 + Vite + Element Plus）
- `server/` 后端（FastAPI + Gunicorn/Uvicorn），仅服务端持有加解密秘钥
- `Data/` 官方数据（供“加载游戏数据”使用）
- `deploy/nginx/default.conf` 前端容器内 Nginx 配置（含 /api 反代）
- `docker-compose.yml` 一键起前后端

## 本地开发
- 后端：
  - `cd server && pip install -r requirements.txt`
  - `uvicorn main:app --reload`
- 前端：
  - `cd ui && npm i && npm run dev`
  - 如需改后端地址：在 `ui/.env` 写 `VITE_API_BASE=http://127.0.0.1:8000`

## 一键部署（Docker Compose）
服务器上克隆仓库后，执行：

```bash
docker compose up -d --build
```

- 端口绑定：默认绑定至本机 `127.0.0.1:8080`（更安全），通过外部 Nginx 反代对外提供服务
- 目录挂载：`./Data` 只读挂载到后端容器 `/app/Data`
- 组件说明：
  - `web`：Nginx 提供前端静态；容器内 `/api` 反代至 `backend:8000`
  - `backend`：FastAPI（Gunicorn+Uvicorn）对内监听 8000

本机调试需要直接暴露时，可将 `docker-compose.yml` 中端口改为 `"0.0.0.0:8080:80"`。

## 外部 Nginx 反代到 Docker
若你已有部署好的 Nginx（推荐 HTTPS），直接将子域名反代到本机 8080：

```
server {
  listen 80; # 建议配合 443/HTTPS 与证书
  server_name sub.your.domain;

  location / {
    proxy_pass http://127.0.0.1:8080/; # 前端容器映射端口
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
}
```

如已将 compose 端口绑定到本地回环（127.0.0.1），外部只能通过 Nginx 访问，更安全。

## 使用指引
- 导入：选择游戏路径中加密文件
  - 例（Steam）：`C:\\Program Files (x86)\\Steam\\steamapps\\common\\RanaCard\\RanaCard_Data\\StreamingAssets\\Card.json`
- 编辑：点击列表项 → 右侧抽屉表单；需要时可切换“直接编辑 JSON”
- 导出：下载同名加密文件，覆盖游戏路径原文件（建议先备份）

## 安全说明
- 加/解密秘钥仅在后端（server）保存与使用；前端不包含秘钥或算法细节。

## 常见问题
- 端口被占用：修改 `docker-compose.yml` 中 `8080:80` 为其他端口
- 上传大小限制：在外部 Nginx 中设置 `client_max_body_size 20m;`
- 更新数据或代码：`git pull && docker compose up -d --build`
