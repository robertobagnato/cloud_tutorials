# 🌐 Step 8 – Accesso al sito online

Ora che il servizio è attivo, puoi accedere al tuo sito statico via browser.

---

## 🔍 Trova l’IP pubblico del container

1. Vai su **ECS > Clusters > corso-cluster > Tasks**
2. Clicca sul task in stato `RUNNING`
3. Scorri fino alla sezione **Network**
4. Copia il valore **Public IP**

---

## 🌍 Apri il sito nel browser

```text
http://<PUBLIC-IP>
```

Dovresti vedere il contenuto del tuo `index.html`.

✅ Il tuo sito è live su AWS ECS Fargate!
