#!/bin/bash
while true
do
	sudo ip addr add 192.168.8.5/24 dev enxa0cec8e7497c
	sudo ip addr add 192.168.7.5/24 dev enxa0cec8d67856
	sleep 1
done
