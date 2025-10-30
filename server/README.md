# 后端（FastAPI）

## 启动

- 安装依赖：`pip install -r requirements.txt`
- 开发运行：`uvicorn main:app --reload`
- 健康检查：`GET http://localhost:8000/api/health`

## API（M1）
- `GET /api/data/card` | `/api/data/pendant` 返回官方数据（同 `/baseline/*` 兼容）
- `POST /api/validate?kind=card|pendant` 结构校验与简单约束
- `POST /api/decode` multipart 上传加密文件 -> 返回 JSON
- `POST /api/encode` body `{ payload }` -> 返回加密文本（可直接保存为游戏同名文件）

读取路径基于仓库根目录的 `Data/`。

## Docker（生产部署）

推荐使用仓库根目录的 `docker-compose.yml` 一键部署前后端（默认仅本机 127.0.0.1:8080 暴露前端）：

1. 构建并启动：
   - `docker compose up -d --build`
   - 前端地址：`http://localhost:8080`
2. 后端容器名：`zgdg-backend`，前端容器名：`zgdg-web`
3. `./Data` 会只读挂载到后端容器 `/app/Data`
