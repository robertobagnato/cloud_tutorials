# 🐳 Step 3 – Costruzione dell’Immagine Docker e Push su Amazon ECR

In questo step creerai l'immagine del sito statico con Docker e la caricherai su Amazon ECR.

---

## ✅ Crea un repository su Amazon ECR

Puoi usare la Console AWS oppure il comando:

```bash
aws ecr create-repository --repository-name corso_sistemi_distribuiti --region eu-west-1
```

---

## 🔐 Login a ECR

```bash
aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 665162913400.dkr.ecr.eu-west-1.amazonaws.com
```

---

## 🔧 Costruisci l'immagine Docker

```bash
docker buildx build --platform linux/amd64 -t corso_sistemi_distribuiti . --load
```

> 🔹 Importante: la flag `--platform linux/amd64` garantisce compatibilità con ECS.

---

## 🏷️ Tagga l’immagine

```bash
docker tag corso_sistemi_distribuiti:latest 665162913400.dkr.ecr.eu-west-1.amazonaws.com/corso_sistemi_distribuiti:latest
```

---

## ☁️ Push su ECR

```bash
docker push 665162913400.dkr.ecr.eu-west-1.amazonaws.com/corso_sistemi_distribuiti:latest
```

---

✅ L'immagine è ora disponibile su ECR e pronta per essere usata in una task ECS.
