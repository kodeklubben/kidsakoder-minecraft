sudo rabbitmqctl add_user admin adminpass123
sudo rabbitmqctl add_vhost myvhost
sudo rabbitmqctl set_permissions -p myvhost admin ".*" ".*" ".*"
