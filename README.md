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
