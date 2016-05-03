
sudo echo "deb http://overviewer.org/debian ./" >> /etc/apt/sources.list
echo 'deb http://www.rabbitmq.com/debian/ testing main' | sudo tee /etc/apt/sources.list.d/rabbitmq.list
apt-get update
apt-get install minecraft-overviewer
apt-get install rabbitmq-server
VERSION=1.9
wget https://s3.amazonaws.com/Minecraft.Download/versions/1.9/1.9.jar -P ~/.minecraft/versions/1.9/
sudo pip install -r requirements.txt
