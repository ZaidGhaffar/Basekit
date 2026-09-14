# BaseKit

A clean and reusable FastAPI starter template for building production-ready Python backends.

## Git

### Remove Existing Git Repository

PowerShell:

```powershell
Remove-Item -Recurse -Force .git
```
---

## File Structure

Show the project structure while ignoring `.venv`, `.git`, and `__pycache__`:

```powershell
ls -Exclude .venv, .git, __pycache__ | % {
    if ($_.PSIsContainer) {
        tree $_.FullName /f /a
    } else {
        "+-- " + $_.Name
    }
}
```

---

## Docker Compose

### Build & Start

```bash
docker compose -f docker/docker-compose.yml up --build
```

Run in background:

```bash
docker compose -f docker/docker-compose.yml up -d --build
```

### Stop

```bash
docker compose -f docker/docker-compose.yml down
```

### View Logs

```bash
docker compose -f docker/docker-compose.yml logs -f
```

### Restart

```bash
docker compose -f docker/docker-compose.yml restart
```

---

## Docker Image

### Build Image

```bash
docker build -f docker/Dockerfile -t basekit .
```

### Build With Version Tag

```bash
docker build -f docker/Dockerfile -t basekit:v1.0 .
```

### List Images

```bash
docker images
```

### Remove Image

```bash
docker rmi basekit:v1.0
```

---

## Docker Container

### Run Container

```bash
docker run -d --name basekit -p 8000:8000 basekit:v1.0
```

With environment file:

```bash
docker run -d --name basekit -p 8000:8000 --env-file .env basekit:v1.0
```

### View Logs

```bash
docker logs -f basekit
```

### Stop Container

```bash
docker stop basekit
```

### Start Container

```bash
docker start basekit
```

### Restart Container

```bash
docker restart basekit
```

---

## Redis

### Start Redis

```bash
docker run -d \
  -p 6379:6379 \
  --name basekit_redis \
  redis:7-alpine
```

PowerShell one-line version:

```powershell
docker run -d -p 6379:6379 --name basekit_redis redis:7-alpine
```

### Stop Redis

```bash
docker stop basekit_redis
```

### Remove Redis

```bash
docker rm -f basekit_redis
```

---

## Docker Cleanup

---

## Quick Start

```bash
# Build and start
docker compose -f docker/docker-compose.yml up -d --build

# Check containers
docker ps

# Follow logs
docker compose -f docker/docker-compose.yml logs -f

# Stop everything
docker compose -f docker/docker-compose.yml down
```
