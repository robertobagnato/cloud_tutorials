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

Passiamo alla creazione del __Launch template__, che si trova all'interno della barra di sinistra sotto Istanze. Clicchiamo crea un nuovo template:
* Nome e descrizione sono __HOLLT__
* Cerchiamo e selezioniamo come AMI Amazon Linux 2023(64 bit)
* Impostare la tipologia di istanza a t2.micro (free tier eligible)
* Selezionare il Key Pair appena creato __EC2KP__
* Selezionare come security group __EC2WEBSG__
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

Come ultimo step di preparazione dobbiamo creare il nostro __Target Group__, presente sotto la voce Loadb Balancing nel menu di sinistra.
* Name : ALBTG
* Target Type : Instance
* Protocol : HTTP
* Port : 80
* VPC : quella creata di default
* Sulla sezione Health Check impostiamo i threshold checks a 2 per healty ed unhealty
Clicchiamo su avanti e concludi senza scegliere le istanze.

Possiamo ora creare finalmente il nostro Loadb balancer, spostandoci sempre sulla barra di sinistra sotto Load Balancer e selezionando __Application Load Balancer__
* Name : ALB
* Scheme : internet-facing
* Ip address type : ipv4
* Load balancer protocol : HTTP
* Port : 80
* Target group : __ALBTG__
Clicchiamo su avanti e confermiamo la creazione. Attendiamo ora qualche minuto e non appena completato prendiamo nota del nome DNS associato al nostro Load Balancer. 

Per completare la creazione ora del sistema spostiamoci su Autoscaling group e creiamone uno nuovo:
* Name : ASG
* Launch Template : __HOLLT__
* VPC : default
* Subent : quelle selezionate in precedenza qualora lo chiedesse
* Abilitare "Enable group metrics collection with CloudWatch"
* Per Group size utilizzare :
  * Desired Capacity: 2 
  * Minimum Capacity: 2 
  * Maximum Capacity: 6 
  
Come policy di scaling selezionare Target tracking scaling policy con i seguenti valori: 
* Scaling Policy Name: Target Tracking Policy 
* Metric type : Average CPU utilization 
* Target value : 30 
* Instances need : 300 
Clicchiamo avanti e poi Crea Autoscaling group. 

A questo punto dovremmo visualizzare le nostre istanze sulla dashboard e andando sul nome DNS del bilanciatore in una nuova pagina web dovremmo vedere il nostro sito web (potrebbe volerci qualche minuto).
Per personalizzare il sito possiamo cambiare l'url dello script nello user data ad esempio con un comando di git per clonare il nostro sito. 
Andando nella sezione istanze possiamo cliccare sulle singole istanze e recuperare l'ip pubblico da inserire poi successivamente nel nostro client SSH (l'user di default è ec2-user). 
