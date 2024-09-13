# coming_soon_ai_product_hack

### How to prepare the local repo

### How to run application
#### With docker
Open project folder in terminal. Use command below to create and run containers from docker-compose.yaml:
```
docker-compose up
```
<!-- Show all containers
```
docker ps -a
```
Or
```
docker container ls -a
```
Stop all containers from docker-compose.yaml (open project folder in terminal):
```
docker-compose stop
```
Stop certain container:
```
docker stop <container-name>
```
Run all containers previously stopped from docker-compose.yaml (open project folder in terminal):
```
docker-compose start
```
Run certain container previously stopped:
```
docker start <container-name>
``` -->
#### Run manually
Frontend  
Open ./frontend in terminal. Use commands:
```
npm install
npm start
```
Backend
Use commands:
```
fastapi dev main.py
```
Or uncomment end of file main.py and use
```
python main.py
```
