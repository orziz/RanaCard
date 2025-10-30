# syntax=docker/dockerfile:1

ARG VITE_API_BASE=/

FROM node:20-alpine AS build
WORKDIR /app/ui
COPY ui/package.json ui/package-lock.json* ui/pnpm-lock.yaml* ui/yarn.lock* ./
RUN npm ci || npm i
COPY ui ./
# 将后端 API 基址注入构建环境，前端以同域 /api 访问
ENV VITE_API_BASE=${VITE_API_BASE}
RUN npm run build

FROM nginx:1.25-alpine AS runner
COPY deploy/nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/ui/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx","-g","daemon off;"]

