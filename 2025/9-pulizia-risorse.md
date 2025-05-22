# 🧹 Step 9 – Pulizia delle risorse (opzionale)

Per evitare costi, puoi eliminare le risorse create dopo la demo.

---

## ❌ Elimina il servizio ECS

```bash
aws ecs delete-service --cluster corso-cluster --service corso-service --force
```

## ❌ Elimina il cluster

```bash
aws ecs delete-cluster --cluster corso-cluster
```

## ❌ Elimina il repository ECR

```bash
aws ecr delete-repository --repository-name corso_sistemi_distribuiti --force
```

✅ Le tue risorse sono state rimosse.
