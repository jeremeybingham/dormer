# dormer

dockerized flask app base with nginx proxy, automated SSL, redis with persistent storage + bootstrap

you need your domain A record corretly pointed at the docker host IP.

Installation:
```
# git and enter 
git clone https://user:pass@github.com/mansard/dormer.git
cd dormer

# make scripts executable
sudo chmod +x cert.sh
sudo chmod +x var.sh

# run setup - enter domain and ssl email
./var.sh

# get inital SSL certs
sudo ./cert.sh

# bring up service
docker-compose up
```

Destroy it: 
```
# get into the directory
cd dormer
docker-compose down

# RESET DOCKER KILL ALL IMAGES, CONTAINERS, VOLUMES CAREFUL!
docker rmi $(docker images -a -q)
docker volume rm $(docker volume ls -q)
docker system prune -a

# delete the directory 
cd
sudo rm -rf dormer
```
