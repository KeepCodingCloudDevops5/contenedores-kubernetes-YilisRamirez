# contenedores-kubernetes-YilisRamirez
<h1>Containers practice</h1>

This practice is intended to deploy a microservice that is able to read and write in a database. To implement this I built a dockerized flask application running in one container which points out toward the database running in another container.
<img src="desktop/microservice.jpg">

<b>Requirements:</b><br>
<ul>
<li> First of all install Docker engine for your OS as described <a href="https://docs.docker.com/engine/install/">here </a> </li>
<li>You would need to install docker compose to run the application and database. You can find the steps <a href="https://docs.docker.com/compose/install/">over here</a> </li>
 </lu>
 
 Once deployed the dockerfile, docker compose, and any other the files required to run the app, you can execute it through the command <b>docker-compose up</b><br>
 
 The output should be as follows:
 Now you can test the application http:/localhost:5000
