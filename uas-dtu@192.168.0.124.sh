# Not in use
#!/bin/bash

path=/home/uas-dtu/Desktop/new_on_uav
path2=/home/uas-dtu/Desktop/new_on_uav/VISION/
multicast_interface="eth0"
interface="wlan0"

echo 'Aether' | sudo -S systemctl stop nvgetty.service
sudo systemctl disable nvgetty.service
sudo systemctl stop nvgetty.service
sudo systemctl disable nvgetty.service
#python3 get_sysid.py
ip=116
ip2=$ip
sysid=$(($ip -100))
#wait
var=/dev/serial/by-id/*
gnome-terminal -- mavproxy.py --master=/dev/ttyTHS1 --master=$(echo $var) --out=127.0.0.1:14550 --out=127.0.0.1:14551 --out=127.0.0.1:14552 --out=127.0.0.1:14553 --out=127.0.0.1:14554 
# if path fails exit the script
cd $path || exit

sudo ip link set $multicast_interface up
sudo ip addr add 192.168.0.$ip2/24 dev $multicast_interface
sudo route add -net 239.0.0.0 netmask 255.255.255.0 $multicast_interface

sudo ip link set $interface up
sudo ip addr add 192.168.4.$ip2/24 dev $interface

gnome-terminal -- python3 -u Uav_to_GCS.py $path $sysid &
gnome-terminal -- python3 -u modified_server8.py $path $sysid &
gnome-terminal -- python3 VISION/LocalPlanner.py $path2  $sysid &

