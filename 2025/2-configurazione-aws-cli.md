# 🔐 Step 2 – Configurazione della AWS CLI

In questo step configurerai la AWS CLI per poter interagire con i servizi AWS dal terminale.

---

## ✅ Requisiti

- Aver installato la [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- Avere una **Access Key** e una **Secret Key** associate al tuo account AWS

Puoi crearle dalla console AWS:
1. Vai su **IAM** (https://console.aws.amazon.com/iam/)
2. Seleziona il tuo utente
3. Vai su **Security credentials**
4. Clicca su **Create access key**

---

## ⚙️ Configura la CLI

Apri il terminale e digita:

```bash
aws configure
```

Ti verrà richiesto di inserire i seguenti dati:

```
AWS Access Key ID [None]: <la tua access key>
AWS Secret Access Key [None]: <la tua secret key>
Default region name [None]: eu-west-1
Default output format [None]: json
```

- `region`: usa `eu-west-1` (Irlanda), o un'altra regione AWS dove vuoi lavorare
- `output`: puoi lasciare `json` o usare `table`/`text` se preferisci

---

## ✅ Verifica che tutto funzioni

Per testare la configurazione:

```bash
aws sts get-caller-identity
```

Se la configurazione è corretta, otterrai un output simile a:

```json
{
  "UserId": "ABCDEF1234567890",
  "Account": "665162913400",
  "Arn": "arn:aws:iam::665162913400:user/tuo-utente"
}
```

---

➡️ Ora sei pronto per passare allo **Step 3: Costruzione dell’immagine e push su Amazon ECR**
