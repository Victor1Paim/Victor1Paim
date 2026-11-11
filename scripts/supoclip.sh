#!/usr/bin/env bash
# Sobe o SupoClip local (fora do repositório, em ../supoclip): Postgres e Redis no Docker,
# API e worker nativos, Whisper local para transcrever e OpenAI (já conectada pelo proxy) para escolher os cortes.
# Uso: scripts/supoclip.sh [subir|parar|status]. API em http://127.0.0.1:8000, usuário "local-user".
set -u
dir="${SUPOCLIP_DIR:-$(cd "$(dirname "$0")/../.." && pwd)/supoclip}"
acao="${1:-subir}"

if [ "$acao" = "parar" ]; then
  pkill -f "uvicorn src.main" ; pkill -f run_workers
  (cd "$dir" && docker compose stop postgres redis) ; exit 0
fi
if [ "$acao" = "status" ]; then
  curl -s -m 5 http://127.0.0.1:8000/health || echo "API fora do ar"; echo
  docker ps --format '{{.Names}} {{.Status}}' | grep supoclip ; exit 0
fi

docker info >/dev/null 2>&1 || { (dockerd >/tmp/dockerd.log 2>&1 &); for i in $(seq 1 30); do docker info >/dev/null 2>&1 && break; sleep 1; done; }
[ -d "$dir" ] || git clone -q --depth 1 https://github.com/FujiwaraChoki/supoclip.git "$dir"
cd "$dir"
[ -f docker-compose.override.yml ] || printf 'services:\n  postgres:\n    ports:\n      - "127.0.0.1:5432:5432"\n' > docker-compose.override.yml
if [ ! -f .env ]; then
  cat > .env <<ENV
TRANSCRIPTION_PROVIDER=whisper
WHISPER_MODEL_SIZE=small
LLM=openai:gpt-5.5
OPENAI_API_KEY=sk-proxy-injected
DATABASE_URL=postgresql+asyncpg://supoclip:supoclip_password@localhost:5432/supoclip
REDIS_HOST=localhost
REDIS_PORT=6379
SELF_HOST=true
TEMP_DIR=$dir/uploads
ALLOW_UNSIGNED_BACKEND_AUTH=true
ENV
fi
cp .env backend/.env; mkdir -p uploads logs
docker compose up -d postgres redis >/dev/null 2>&1
for i in $(seq 1 30); do docker exec supoclip-postgres pg_isready -U supoclip >/dev/null 2>&1 && break; sleep 1; done
cd backend
[ -d .venv ] || uv venv -q .venv
uv sync -q --extra cpu
.venv/bin/python -c "import asyncio; from src.database import init_db; asyncio.run(init_db())"
docker exec supoclip-postgres psql -U supoclip -d supoclip -qc "insert into users (id,name,email,\"emailVerified\",is_admin,plan,subscription_status,default_clip_length) values ('local-user','Local','local@localhost',true,true,'pro','active','long') on conflict (id) do nothing" >/dev/null
pgrep -f "uvicorn src.main" >/dev/null || (nohup .venv/bin/uvicorn src.main:app --host 127.0.0.1 --port 8000 > ../logs/api.log 2>&1 &)
pgrep -f run_workers >/dev/null || (nohup .venv/bin/python -m src.workers.run_workers > ../logs/worker.log 2>&1 &)
sleep 8; curl -s -m 5 http://127.0.0.1:8000/health; echo
