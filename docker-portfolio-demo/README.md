# Infra Portfolio Demo

這是一個適合系統工程師 / Infra Team 面試展示的小型作品集專案。

## 架構
- Flask API container
- PostgreSQL container
- Docker Compose 啟動雙容器
- Health check / restart policy / volume

## 啟動方式
```bash
cd infra-portfolio-demo
docker compose up --build -d
```

## 驗證
```bash
curl http://localhost:5000/health
curl http://localhost:5000/
curl http://localhost:5000/visits
```

## 關閉
```bash
docker compose down
```

## 完整刪除資料
```bash
docker compose down -v
```

## 面試可講亮點
1. 使用 Docker Compose 管理多容器服務
2. Web 服務依賴資料庫健康檢查後才啟動
3. 使用 volume 保存 PostgreSQL 資料
4. 使用 restart policy 提升服務穩定性
5. 具備 health endpoint 可供監控系統串接

## 常用除錯指令
```bash
docker ps
docker logs infra_demo_web
docker logs infra_demo_db
docker exec -it infra_demo_web sh
docker exec -it infra_demo_db psql -U demo -d infra_demo
```

## Linux 面試延伸
```bash
ps aux | head
df -h
free -m
ss -lntp
chmod +x scripts/test.sh
```
