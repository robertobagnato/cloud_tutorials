# Docker Volumes

This tutorial shows how a container can read files from a folder on the host machine by mounting it as a volume.

## 1. Build the image

```bash
docker build -t volume-file-lister .
```

## 2. Run with Docker

```bash
docker run -d --name volume-file-lister -v "$(pwd)/data:/data" volume-file-lister
```

Read the logs:

```bash
docker logs volume-file-lister
```

Expected output:

```text
Files mounted in /data:
- notes.txt (102 bytes)
- todo.txt (62 bytes)
Container still running. Refreshing in 5 seconds...
```

The `-v "$(pwd)/data:/data"` option mounts the local `data` folder into the container at `/data`.

Stop and remove the container:

```bash
docker rm -f volume-file-lister
```

## 3. Run with Docker Compose

```bash
docker compose up --build -d
```

Read the logs:

```bash
docker compose logs -f
```

Compose uses the same mount declared in `docker-compose.yml`:

```yaml
volumes:
  - ./data:/data
```

Try adding another file inside `data/`. The new file appears in the logs without rebuilding the image because it lives on the host, not inside the image.

Stop the Compose app:

```bash
docker compose down
```
