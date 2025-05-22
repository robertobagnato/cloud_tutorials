# 🚀 Step 7 – Creazione del Servizio ECS

Il servizio gestisce l’esecuzione e l’alta disponibilità dei container.

---

## ✅ Crea il servizio

1. Vai su **Clusters > corso-cluster > Services > Create**
2. Tipo: **Fargate**
3. Task Definition: `corso-task`
4. Nome servizio: `corso-service`
5. Numero di task: `1`

---

## 🌐 Configura rete

- Seleziona una **subnet pubblica**
- Abilita: `Auto-assign public IP: ENABLED`
- Security group: apri la porta 80 (HTTP) da `0.0.0.0/0`

Clicca **Create Service**

✅ Il servizio avvierà un container con IP pubblico.
