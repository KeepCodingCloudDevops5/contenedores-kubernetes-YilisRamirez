# contenedores-kubernetes-YilisRamirez
<h1>Containers practice</h1>

This practice is intended to deploy a microservice that is able to read and write in a database. To implement this I built a dockerized flask application running in one container which points out toward the database running in another container.
<img src="desktop/microservice.jpg">

<b>Requirements:</b><br>
<ul>
<li> First of all install Docker engine for your OS as described <a href="https://docs.docker.com/engine/install/">here </a> </li>
<li>You would need to install docker compose to run the application and database. You can find the steps <a href="https://docs.docker.com/compose/install/">over here</a> </li>
<li>Python 3.7-alpine, Flask, MySQL 5.7, Docker and Docker Compose already installed</li>
</lu>

<h1>Docker compose installation</h1>
Using the following command to install Docker compose. I am installing it under Linux OS.

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
Applying permissions to make the binary executable

```bash
sudo chmod +x /usr/local/bin/docker-compose
```
Finally you can verify the installation by this command:
```bash
docker-compose --version
```
It will deploy the following info:
```bash
docker-compose version 1.29.2, build 5becea4c
```
<h1>Flask MySQL App</h1>
Now I am going to create a directory called <b>"flask-mysql-app"</b> to store there all files needed to dockerize it through docker compose.

```bash
mkdir flask-mysql-app
 ```
First of all, I am going to define the app.py file to configure flask app and the database settings for establishing the communication between them.
Also, there has been defined environment variables(hardcoded) for sensitive information such as, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST and MYSQL_DB to make it configurable from only one file.
![image](https://user-images.githubusercontent.com/39458920/156873887-3fb40a05-def5-4ac3-b63c-c8826a18b203.png)

Now into the requirements file, I included the required libraries for app.py file
```bash
flask
flask-mysqldb
 ```
For building the app, I have disegned a Dockerfile to add the required dependencies, software or libraries. Notice there were also included the environment variables for MySQL configuration, as it should be synchronized with the application.

There was also introduced the variable <b>FLASK_ENV=development</b>, which reloads the application when it detects any change.

![dockerfile](https://user-images.githubusercontent.com/39458920/156876664-29752dc3-e913-4043-9713-5aa6b473b46e.JPG)

Now the final part is create the docker compose file, where are specified the services for flask and MySQL app, the container's image, the environments, ports, and volumenes to make it persistents for both database and flask app.

![docker-compose](https://user-images.githubusercontent.com/39458920/156877070-c236ed9c-e1e6-424f-b38b-c5c98fb00e48.JPG)

Once deployed the dockerfile, docker compose, and any other the files required, now you can run the application through the command below:
 
 ```bash
 docker-compose up
 ```
 The output should be as follows:
 
 ![docker](https://user-images.githubusercontent.com/39458920/156846760-316557b8-bc69-42d7-88f7-8fbabd14b19b.JPG)
 
 Now you can see the output by typing the url shown above http://172.18.0.3:5000/ on your Unix shell terminal or your browser.
 To see the output of table creation, type the command:  
 
 ```bash
 http://172.18.0.3:5000/create-table
 ```
 You will see the following output on your Unix terminal/browser:

![create-table](https://user-images.githubusercontent.com/39458920/156878380-cd7e6253-e47e-4aab-9ec5-eb188baa699a.JPG)

To see the output of added students, type the command:  
 ```bash
 http://172.18.0.3:5000/add-students
 ```
You will see the following output on your Unix terminal/browser:

![add-students](https://user-images.githubusercontent.com/39458920/156878176-3f0cb950-f870-4c59-ba98-1577547bed4b.JPG)
 
 To see the output of table students, type the command: 
  ```bash
 http://172.18.0.3:5000/
 ```
 You will see the following output on your Unix terminal/browser:
 
 ![table creation](https://user-images.githubusercontent.com/39458920/156878135-58fc7b0c-13e9-4c72-94eb-0a32c949fae7.JPG)
 
<h1>Verifying the logs for database and flask app are being sent to standard output (STDOUT/STDERR)</h1>

![mysql_logs](https://user-images.githubusercontent.com/39458920/156889548-cbc012dc-a797-4328-9157-92150338a255.JPG)

![flask_logs](https://user-images.githubusercontent.com/39458920/156889585-cec4ba8d-a1c0-4183-ad89-50c0fbdcba48.JPG)

<h1>Deploying the application in Kubernetess</h1>
First of all you will need to create a cluster in Google Cloud console to associate it to Kubernetes environment.

Creating namespace for each manifest.
```bash
k create ns database --dry-run -oyaml > ns.yaml
k create ns flask-api --dry-run -oyaml > ns-flask-api.yaml

k create -f ns.yaml
k create -f ns-flask-api.yaml
```
<h1>Storing database credentials in Kubernetes secrets</h1> 
 
 The vulnerable data in the database should be stored as Base64 encoded strings thorugh the following command:
 ```bash
 echo -n 'rootpassword' | base64
```

This command will output a string of characters, as shown below.
```bash
 c2VjcmV0MTIU=
```
Once encoded the rootpassword, a secret file is deployeed for each namespace created.

```bash
apiVersion: v1
kind: Secret
metadata:
  name: mysql-secret
  namespace: database
type: Opaque
data:
  rootpassword: cGFzc3c=
```
```bash
k create -f mysql-secret.yaml
```

```bash
apiVersion: v1
kind: Secret
metadata:
  name: mysql-secret
  namespace: flask-api
type: Opaque
data:
  rootpassword: cGFzc3c=
```
```bash
k create -f flaskapi-secrets.yaml
```
Now let's provide persistence to the database with Persistent Volume Claim. For this is needed to check the storage classes from the cluster.

According to the output below, it seems to be standard:
```bash
kubectl get storageclasses.storage.k8s.io
NAME                 PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
premium-rwo          pd.csi.storage.gke.io   Delete          WaitForFirstConsumer   true                   8d
standard (default)   kubernetes.io/gce-pd    Delete          Immediate              true                   8d
```
Now we can define the manifest for Persistent Volume Claim:

```bash
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pv-claim
  namespace: database
spec:
  storageClassName: standard
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 20Gi
```

```bash
k create -f mysql-pvc.yaml
```
As you can see Persistent Volume Claim has been successfully created and bound.

```bash
kubectl get pvc -n database
NAME             STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
mysql-pv-claim   Bound    pvc-618b86aa-310f-426a-8fd1-70d650c1bb42   20Gi       RWO            standard       10h
```
Additionally, we can see persistent volume is automatically created.

```bash
kubectl get persistentvolume
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                     STORAGECLASS   REASON   AGE
pvc-618b86aa-310f-426a-8fd1-70d650c1bb42   20Gi       RWO            Delete           Bound    database/mysql-pv-claim   standard                11h
```

<h1>Deploying MySQL in Kubernetess</h1>

Now we can run the mysql instance with a deployment workload.

```bash
piVersion: apps/v1
kind: Deployment
metadata:
  name: mysql
  namespace: database
spec:
  selector:
    matchLabels:
      app: mysql
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - image: mysql:5.6
        name: mysql
        env:
        - name: MYSQL_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mysql-secret
              key: rootpassword
        ports:
        - containerPort: 3306
          name: mysql
        volumeMounts:
        - name: mysql-persistent
          mountPath: /var/lib/mysql
      volumes:
      - name: mysql-persistent
        persistentVolumeClaim:
          claimName: mysql-pv-claim
  ```
We can see the associated pod to mysql instance, which is in status running.

```bash
kubectl get pods -n database
NAME                     READY   STATUS    RESTARTS   AGE
mysql-54dccfbfbd-vslwh   1/1     Running   0          10h
```
Creating a service to provide MySQL access towards Flask app or any other pod inside the cluster.

```bash
apiVersion: v1
kind: Service
metadata:
  name: mysql
  namespace: database
spec:
  ports:
  - port: 3306
  selector:
    app: mysql
  clusterIP: None
```

```bash
kubectl create -f service-mysql.yaml
```

<h1>Storing database credentials in Kubernetes Configmap</h1> 

I have specified the variables MYSQL_HOST and MYSQL_DB into the configmap configuration.

```bash
apiVersion: v1
data:
  dbname: studentdb
  host: mysql.database:3306
kind: ConfigMap
metadata:
  creationTimestamp: null
  name: flaskapi-cm
  namespace: flask-api
```

```bash
k create -f configmap.yaml
```
<h1>Deploying Flask app in Kubernetess</h1>
Now I set the environment variales in this deployment, using the values specified in the secret and configmap file.
The flask image was built from Dockerfile configuration.

```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flaskapp-deployment
  namespace: flask-api
  labels:
    app: flaskapp
spec:
  selector:
    matchLabels:
      app: flaskapp
  replicas: 2
  template:
    metadata:
      labels:
        app: flaskapp
    spec:
      containers:
        - name: flaskapp
          image: ramirezy/flask-kubernetes
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 5000
          env:
            - name: MYSQL_HOST
              valueFrom:
                configMapKeyRef:
                  name: flaskapi-cm
                  key: host
            - name: MYSQL_DB
              valueFrom:
                configMapKeyRef:
                  name: flaskapi-cm
                  key: dbname
            - name: MYSQL_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: mysql-secret
                  key: rootpassword
```
Applying the flask app deployment

```bash
kubectl create -f flaskapp-deployment.yaml
```
```bash
kubectl get pods -n flask-api
NAME                                   READY   STATUS    RESTARTS   AGE
flaskapp-deployment-7bd7ccf9b6-h254l   1/1     Running   0          151m
flaskapp-deployment-7bd7ccf9b6-m26jv   1/1     Running   0          151m
```
Creating a service to expose the deployment ousite of the cluster through a LoadBalancer.

```bash
apiVersion: v1
kind: Service
metadata:
  name: flask-service
  namespace: flask-api
  labels:
    app: flaskapp
spec:
  ports:
  - port: 5000
    protocol: TCP
    targetPort: 5000
  selector:
    app: flaskapp
  type: LoadBalancer
```
```bash
kubectl create -f service-flask.yaml
```
Now we can check all the resources deployed in each instance.

Database instance
```bash
kubectl get all -n database
NAME                         READY   STATUS    RESTARTS   AGE
pod/mysql-54dccfbfbd-vslwh   1/1     Running   0          11h

NAME            TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE
service/mysql   ClusterIP   None         <none>        3306/TCP   5h34m

NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/mysql   1/1     1            1           11h

NAME                               DESIRED   CURRENT   READY   AGE
replicaset.apps/mysql-54dccfbfbd   1         1         1       11h
```

Flask instance
```bash
kubectl get all -n flask-api
NAME                                       READY   STATUS    RESTARTS   AGE
pod/flaskapp-deployment-7bd7ccf9b6-h254l   1/1     Running   0          165m
pod/flaskapp-deployment-7bd7ccf9b6-m26jv   1/1     Running   0          165m

NAME                    TYPE           CLUSTER-IP   EXTERNAL-IP     PORT(S)          AGE
service/flask-service   LoadBalancer   10.24.2.84   35.233.41.185   8080:30795/TCP   117m

NAME                                  READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/flaskapp-deployment   2/2     2            2           165m

NAME                                             DESIRED   CURRENT   READY   AGE
replicaset.apps/flaskapp-deployment-7bd7ccf9b6   2         2         2       165m
```

```
