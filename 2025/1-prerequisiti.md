# 📦 Step 1 – Prerequisiti

Questa guida ti guiderà nel deployment di un sito statico su **AWS ECS Fargate** usando **Docker** e **Amazon ECR**.

---

## ✅ Cosa ti serve prima di iniziare:

### 1. Account AWS
- Registrati su [https://aws.amazon.com/](https://aws.amazon.com/) se non ne hai uno.

### 2. Un semplice sito statico
- Deve contenere almeno un file `index.html`.

Esempio:
```html
<!-- index.html -->
<!DOCTYPE html>
<html>
  <head>
    <title>Demo ECS</title>
  </head>
  <body>
    <h1>Sito statico in esecuzione su AWS ECS Fargate!</h1>
  </body>
</html>
```

### 3. Docker installato sul tuo computer
- Scaricabile da: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)

Verifica installazione:
```bash
docker --version
```

### 4. AWS CLI installata
- Guida ufficiale: [https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)

Verifica installazione:
```bash
aws --version
```

### 5. File `Dockerfile` per containerizzare il sito

Esempio:
```dockerfile
# Dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/
EXPOSE 80
```

Con questi prerequisiti completati, puoi passare allo **Step 2: Configurazione della AWS CLI**.
