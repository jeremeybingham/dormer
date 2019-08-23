# dormer
base API and microservices framework

Setup:

[git clone this repo]
cd dormer
sudo chmod +x cert.sh
sudo chmod +x var.sh
./var.sh
sudo ./cert.sh
docker-compose up


Wipe:

cd dormer
docker-compose down
docker rmi $(docker images -a -q)
docker volume rm $(docker volume ls -q)
docker system prune -a
cd
sudo rm -rf dormer
