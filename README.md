# Tutorial corso Architetture dei Sistemi Distribuiti
Una volta creato l'account AWS, effettuare il login alla console aws console.aws.amazon.com
Selezionare la Regione Virginia Settentrionale. 
Nella barra di ricerca cercare il servizio EC2 e aprire una nuova scheda. Per creare la nostra architettura abbiamo bisogno di: 
* ***Key pair***: permette la connessione tramite SSH alle macchine EC2
* ***Security Group***: definisce le regole di sicurezza per le macchine ad esso associate (es. consenti traffico HTTP)
* ***EC2 template***: template della macchina che dovremo creare in base a determinate regole comprensive di script di esecuzione in fase di avvio
* ***Application Load Balancer***: Bilanciatore di traffico per gestire le richieste verso il nostro sistema distribuito
* ***Autoscaling Group***: contiene un insieme di istanze EC2 che vengono trattate come un raggruppamento logico ai fini dello scaling e della gestione automatica. 
* ***Target group***: usato per smistare il traffico verso una o più risorse registrate (tipicamente EC2)

Iniziamo con il creare i security group, i quali consentiranno traffico SSH e HTTP in ingresso alle nostre macchine. Sulla barra di sinistra abbiamo una voce di menu chiamata Security group
(o Gruppi di sicurezza). Entrati facciamo click su Nuovo (abbiamo bisogno di 2 security group, uno per le macchine EC2 e l'altro per il Load balancer).
* EC2:
  * Il nome e la descrizione sono __EC2WEBSG__
  * Aggiungere una regola di ingresso per SSH da 0.0.0.0/0  (non raccomandato per ambienti diversi da ambienti di test/sviluppo)
  * Aggiungere una regola di ingresso per HTTP da 0.0.0.0/0 
* Loadb Balancer:
  * Il nome e la descrizione sono __ALBSG__
  * Aggiungere una regola di ingresso per HTTP da 0.0.0.0/0 
  
Cliccare su continua e poi conferma per ogni gruppo e attendiamo la corretta creazione. 

Creiamo ora la nostra chiave per poter accedere successivamente alle macchine. Nella barra di sinistra spostarsi sotto Key Pairs (coppia di chiavi) e cliccare crea una coppia di chiavi. 
Come nome inseriamo __EC2KP__, lasciamo di default .ppk e scarichiamo il file ( ci servirà poi per inserirlo dentro un software come ad esempio putty)

Passiamo alla creazione del Launch template, che si trova all'interno della barra di sinistra sotto Istanze. Clicchiamo crea un nuovo template:
* Nome e descrizione sono __HOLLT__
* Cerchiamo e selezioniamo come AMI Amazon Linux 2023(64 bit)
* Impostare la tipologia di istanza a t2.micro (free tier eligible)
* Selezionare il Key Pair appena creato __EC2KP__
* Selezionare come security group __EC"WEBSG__
* Come subnet scegliamo due subnet (es. us-east-1a e us-east-1b)
* Spostarsi su Advanced Details e inserire sotto il campo __user data__ il codice di seguito per poi confermare la creazione


```console
#!/bin/bash
yum update -y
yum install -y httpd
yum install -y wget
cd /var/www/html
wget https://raw.githubusercontent.com/fenderbob/cloud_tutorials/main/index.html
service httpd start
```

Possiamo ora creare finalmente il nostro Loadb balancer, spostandoci sempre sulla barra di sinistra sotto Load Balancer e selezionando __Application Load Balancer__
* Nome : ALB
* Schema : internet-facing
* Ip address type : ipv4
* Load balancer protocol : HTTP
* Port : 80
* Sulla sezione Health Check impostiamo i threshold checks a 2
* Lasciare vuota per il momento la sezione target group

  
