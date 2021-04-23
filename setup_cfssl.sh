#!/bin/bash
#Install Go
apt install software-properties-common gpg
add-apt-repository ppa:longsleep/golang-backports
apt update
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F6BC817356A3D45E
apt update && upgrade
apt install golang-go

#setup cfss env
useradd cfssl
mkdir -p /etc/cfssl/certs
chown -R cfssl:cfssl /etc/cfssl

go get -u github.com/cloudflare/cfssl/cmd/... #if doesn't work remove -u
sudo cp -r /home/$USER/go/bin/* /usr/local/bin/

#https://wiki.defect.ch/os/linux/lemur_and_cfssl_with_nginx_and_postgresql_on_centos8/lemur_and_cfssl_with_nginx_and_postgresql_on_centos8
#https://github.com/Netflix/lemur-docker
#https://github.com/mrts/docker-postgresql-multiple-databases