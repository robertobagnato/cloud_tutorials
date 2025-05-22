# ⚙️ Step 6 – Creazione della Task Definition

Una Task Definition specifica come eseguire il container (immagine, CPU, memoria, porta, ecc).

---

## ✅ Crea una nuova Task Definition

### Via Console:

1. Vai su **Task Definitions > Create new**
2. Launch type: **Fargate**
3. Nome: `corso-task`
4. OS: **Linux**
5. Task role: `ecsTaskExecutionRole`
6. CPU: `0.25 vCPU`
7. Memory: `0.5 GB`

---

## ➕ Aggiungi il container

- Nome container: `corso-site`
- Image URI:  
  `665162913400.dkr.ecr.eu-west-1.amazonaws.com/corso_sistemi_distribuiti:latest`
- Port mapping: `80`

Clicca **Add container** → **Create**

✅ Task pronta per essere avviata.
