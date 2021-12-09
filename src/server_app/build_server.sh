sudo docker build -t server-app:v1.0.0 .
sudo docker tag server-app:v1.0.0 192.168.33.10:5000/server-app:v1.0.0
sudo docker push 192.168.33.10:5000/server-app:v1.0.0