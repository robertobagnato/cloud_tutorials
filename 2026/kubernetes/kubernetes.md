# Laboratorio Kubernetes locale con kind e nginx

Questa guida descrive come preparare l'ambiente per svolgere il laboratorio Kubernetes in locale usando **kind**, **kubectl**, **Docker** e un sito **nginx**.

Sono previste due configurazioni:

- **Mac** con Docker Desktop, Homebrew, kind e kubectl
- **Windows** con WSL2, Docker Desktop, kind e kubectl dentro Ubuntu/WSL

Una volta completato il setup, i comandi Kubernetes sono uguali per tutti.

---

## 1. Obiettivo del laboratorio

Durante il laboratorio verrà creato un cluster Kubernetes locale e verrà deployato un semplice sito nginx.

Vedremo come:

- creare un cluster Kubernetes locale;
- creare un namespace dedicato;
- creare una pagina HTML;
- configurare nginx tramite ConfigMap;
- creare un Deployment;
- esporre l'applicazione tramite Service;
- accedere al sito dal browser;
- scalare le repliche;
- simulare un guasto;
- aggiornare la pagina;
- simulare un errore di deployment;
- fare rollback;
- cancellare le risorse.

---

# Parte A — Setup su Mac

## A.1 Prerequisiti

Su Mac servono:

- Docker Desktop
- Homebrew
- kubectl
- kind

Verificare che Docker Desktop sia installato e avviato.

```bash
docker --version
```

Se Docker risponde con una versione, è correttamente installato.

---

## A.2 Installare kubectl e kind

Se Homebrew è già installato:

```bash
brew install kubectl kind
```

Verifica:

```bash
kubectl version --client
kind version
docker ps
```

Se `docker ps` funziona, Docker è attivo e utilizzabile da kind.

---

## A.3 Creare il cluster Kubernetes locale

```bash
kind create cluster --name sistemi-distribuiti
```

Verifica:

```bash
kubectl cluster-info
kubectl get nodes
```

Output atteso:

```text
NAME                                  STATUS   ROLES           AGE   VERSION
sistemi-distribuiti-control-plane     Ready    control-plane   ...   ...
```

---

# Parte B — Setup su Windows

## B.1 Configurazione consigliata

Su Windows si consiglia di usare:

```text
Windows 10/11 + WSL2 + Docker Desktop + Ubuntu + kind + kubectl
```

Gli studenti Windows dovrebbero eseguire i comandi Kubernetes dentro **Ubuntu su WSL2**, non nel Prompt dei comandi tradizionale.

---

## B.2 Installare WSL2

Aprire **PowerShell come amministratore** ed eseguire:

```powershell
wsl --install
```

Riavviare il computer se richiesto.

Al termine, aprire **Ubuntu** dal menu Start.

Verificare dentro Ubuntu:

```bash
wsl --version
uname -a
```

---

## B.3 Installare Docker Desktop

Installare Docker Desktop per Windows.

Poi abilitare l'integrazione con WSL2:

```text
Docker Desktop → Settings → Resources → WSL Integration → Enable integration with Ubuntu
```

Dentro Ubuntu/WSL verificare:

```bash
docker --version
docker ps
```

Se `docker ps` funziona senza errori, Docker Desktop è correttamente collegato a WSL2.

---

## B.4 Installare kubectl dentro WSL2

Dentro Ubuntu/WSL:

```bash
sudo apt update
sudo apt install -y curl
```

Scaricare e installare `kubectl`:

```bash
curl -LO "https://dl.k8s.io/release/stable.txt"
KUBECTL_VERSION=$(cat stable.txt)
curl -LO "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
rm stable.txt
```

Verifica:

```bash
kubectl version --client
```

---

## B.5 Installare kind dentro WSL2

Dentro Ubuntu/WSL:

```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

Verifica:

```bash
kind version
```

---

## B.6 Creare il cluster Kubernetes locale

Sempre dentro Ubuntu/WSL:

```bash
kind create cluster --name sistemi-distribuiti
```

Verifica:

```bash
kubectl cluster-info
kubectl get nodes
```

Da questo punto in poi i comandi sono uguali a quelli usati su Mac.

---

# Parte C — Comandi comuni del laboratorio

Questa parte vale sia per Mac sia per Windows/WSL2.

---

## C.1 Creare un namespace per il laboratorio

```bash
kubectl create namespace lab-k8s
kubectl config set-context --current --namespace=lab-k8s
```

Verifica:

```bash
kubectl get namespaces
```

---

## C.2 Creare la cartella del laboratorio

```bash
mkdir k8s-nginx-lab
cd k8s-nginx-lab
```

---

## C.3 Creare la pagina HTML

```bash
cat <<'EOF' > index.html
<!doctype html>
<html>
  <head>
    <title>Kubernetes Lab</title>
  </head>
  <body>
    <h1>Ciao da Kubernetes!</h1>
    <p>Applicazione nginx in esecuzione su kind.</p>
    <p>Versione: 1</p>
  </body>
</html>
EOF
```

---

## C.4 Creare la ConfigMap

```bash
kubectl create configmap nginx-html --from-file=index.html
```

Verifica:

```bash
kubectl get configmap
kubectl describe configmap nginx-html
```

---

## C.5 Creare il Deployment

Creare il file `deployment.yaml`:

```bash
cat <<'EOF' > deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-web
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx-web
  template:
    metadata:
      labels:
        app: nginx-web
    spec:
      containers:
        - name: nginx
          image: nginx:stable
          ports:
            - containerPort: 80
          volumeMounts:
            - name: html-volume
              mountPath: /usr/share/nginx/html
      volumes:
        - name: html-volume
          configMap:
            name: nginx-html
EOF
```

Applicare il Deployment:

```bash
kubectl apply -f deployment.yaml
```

Verifica:

```bash
kubectl get deployments
kubectl get pods
kubectl get pods -o wide
```

---

## C.6 Creare il Service

Creare il file `service.yaml`:

```bash
cat <<'EOF' > service.yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-web
spec:
  selector:
    app: nginx-web
  ports:
    - port: 80
      targetPort: 80
EOF
```

Applicare il Service:

```bash
kubectl apply -f service.yaml
```

Verifica:

```bash
kubectl get services
kubectl describe service nginx-web
```

---

## C.7 Accedere al sito dal browser

Avviare il port-forward:

```bash
kubectl port-forward service/nginx-web 8080:80
```

Aprire nel browser:

```text
http://localhost:8080
```

In alternativa, da un secondo terminale:

```bash
curl http://localhost:8080
```

Su Windows, il comando `kubectl port-forward` va lasciato in esecuzione dentro Ubuntu/WSL2. Il browser può essere aperto normalmente da Windows su `http://localhost:8080`.

---

## C.8 Mostrare le repliche

```bash
kubectl get pods
```

Scalare a 5 repliche:

```bash
kubectl scale deployment nginx-web --replicas=5
```

Verifica:

```bash
kubectl get pods
```

Tornare a 3 repliche:

```bash
kubectl scale deployment nginx-web --replicas=3
kubectl get pods
```

---

## C.9 Self-healing: eliminare un Pod

Visualizzare i Pod:

```bash
kubectl get pods
```

Eliminare un Pod sostituendo `<nome-pod>` con il nome reale:

```bash
kubectl delete pod <nome-pod>
```

Esempio:

```bash
kubectl delete pod nginx-web-xxxxxxxxxx-yyyyy
```

Verifica:

```bash
kubectl get pods
```

Kubernetes creerà automaticamente un nuovo Pod perché il Deployment richiede 3 repliche.

---

## C.10 Aggiornare la pagina HTML

Modificare `index.html`:

```bash
cat <<'EOF' > index.html
<!doctype html>
<html>
  <head>
    <title>Kubernetes Lab</title>
  </head>
  <body>
    <h1>Ciao da Kubernetes!</h1>
    <p>Applicazione nginx in esecuzione su kind.</p>
    <p>Versione: 2</p>
    <p>La pagina è stata aggiornata tramite ConfigMap.</p>
  </body>
</html>
EOF
```

Aggiornare la ConfigMap:

```bash
kubectl create configmap nginx-html \
  --from-file=index.html \
  --dry-run=client -o yaml | kubectl apply -f -
```

Riavviare il Deployment per far rileggere la ConfigMap:

```bash
kubectl rollout restart deployment/nginx-web
kubectl rollout status deployment/nginx-web
```

Ricaricare il browser:

```text
http://localhost:8080
```

---

## C.11 Rolling update dell'immagine nginx

Cambiare immagine:

```bash
kubectl set image deployment/nginx-web nginx=nginx:alpine
```

Controllare lo stato del rollout:

```bash
kubectl rollout status deployment/nginx-web
kubectl get pods
```

Vedere la cronologia:

```bash
kubectl rollout history deployment/nginx-web
```

Eseguire rollback:

```bash
kubectl rollout undo deployment/nginx-web
kubectl rollout status deployment/nginx-web
```

---

## C.12 Simulare un errore

Impostare un'immagine inesistente:

```bash
kubectl set image deployment/nginx-web nginx=nginx:versione-che-non-esiste
```

Verifica:

```bash
kubectl get pods
```

Indagare sul problema:

```bash
kubectl describe pod <nome-pod>
kubectl get events --sort-by=.metadata.creationTimestamp
```

Errore atteso:

```text
ErrImagePull
ImagePullBackOff
```

Correggere con rollback:

```bash
kubectl rollout undo deployment/nginx-web
kubectl rollout status deployment/nginx-web
```

---

## C.13 Comandi utili di debug

```bash
kubectl get all
kubectl get pods -o wide
kubectl describe deployment nginx-web
kubectl describe service nginx-web
kubectl logs <nome-pod>
kubectl get events --sort-by=.metadata.creationTimestamp
```

---

## C.14 Pulizia finale

Cancellare le risorse del laboratorio:

```bash
kubectl delete -f service.yaml
kubectl delete -f deployment.yaml
kubectl delete configmap nginx-html
```

Cancellare il namespace:

```bash
kubectl delete namespace lab-k8s
```

Cancellare il cluster kind:

```bash
kind delete cluster --name sistemi-distribuiti
```

---

# Parte D — Differenze principali tra Mac e Windows

| Aspetto | Mac | Windows |
|---|---|---|
| Terminale | Terminale macOS / iTerm | Ubuntu su WSL2 |
| Installazione tool | Homebrew | apt + curl dentro WSL2 |
| Docker | Docker Desktop | Docker Desktop con WSL Integration |
| kind | `brew install kind` | binario Linux installato in WSL2 |
| kubectl | `brew install kubectl` | binario Linux installato in WSL2 |
| Browser | Browser macOS | Browser Windows |
| Accesso al sito | `http://localhost:8080` | `http://localhost:8080` |

---

# Parte E — Scaletta rapida della demo

```bash
kind create cluster --name sistemi-distribuiti

kubectl create namespace lab-k8s
kubectl config set-context --current --namespace=lab-k8s

mkdir k8s-nginx-lab
cd k8s-nginx-lab

# creare index.html
# creare ConfigMap
# creare deployment.yaml
# creare service.yaml

kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

kubectl get all
kubectl port-forward service/nginx-web 8080:80
```

In un secondo terminale:

```bash
curl http://localhost:8080
```

Demo principali:

```bash
kubectl scale deployment nginx-web --replicas=5
kubectl get pods

kubectl delete pod <nome-pod>
kubectl get pods

kubectl rollout restart deployment/nginx-web
kubectl rollout status deployment/nginx-web

kubectl set image deployment/nginx-web nginx=nginx:versione-che-non-esiste
kubectl get pods
kubectl describe pod <nome-pod>
kubectl rollout undo deployment/nginx-web
```
