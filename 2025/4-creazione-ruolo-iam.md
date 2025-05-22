# 🔒 Step 4 – Creazione del ruolo IAM per ECS

Amazon ECS ha bisogno di un ruolo IAM per eseguire task Fargate e accedere a ECR.

---

## ✅ Crea o verifica il ruolo `ecsTaskExecutionRole`

### Opzione 1: Console AWS

1. Vai su **IAM > Roles**
2. Clicca **Create Role**
3. **Trusted entity type**: AWS Service
4. **Use case**: Elastic Container Service → Elastic Container Service Task
5. Clicca **Next**
6. Aggiungi la policy: `AmazonECSTaskExecutionRolePolicy`
7. Dai un nome: `ecsTaskExecutionRole`
8. Clicca **Create Role**

---

### Opzione 2: AWS CLI

```bash
aws iam create-role   --role-name ecsTaskExecutionRole   --assume-role-policy-document file://trust-policy.json
```

Poi allega la policy:

```bash
aws iam attach-role-policy   --role-name ecsTaskExecutionRole   --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
```

✅ Il ruolo è ora pronto per essere usato nelle Task Definition.
