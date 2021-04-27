#!/bin/bash
#Install Go
apt install software-properties-common gpg rsync
add-apt-repository ppa:longsleep/golang-backports
apt update
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F6BC817356A3D45E
apt update && apt upgrade
apt install golang-go

#setup cfss env
useradd cfssl
mkdir -p /etc/cfssl/certs

go get github.com/cloudflare/cfssl/cmd/... #if doesn't work remove -u
go get bitbucket.org/liamstask/goose/cmd/goose
cp -r $HOME/go/bin/* /usr/local/bin/

cp ./db_config.json /etc/cfssl/

rsync -avzhp ./csr_root_ca.json ./csr_intermediate_ca.json ./cfssl-config.json /etc/cfssl/certs/

chown -R cfssl:cfssl /etc/cfssl

cfssl gencert -initca /etc/cfssl/certs/csr_root_ca.json | cfssljson -bare /etc/cfssl/certs/root_ca

cfssl gencert -initca /etc/cfssl/certs/csr_intermediate_ca.json | cfssljson -bare /etc/cfssl/certs/intermediate_ca
cfssl sign -ca /etc/cfssl/certs/root_ca.pem -ca-key /etc/cfssl/certs/root_ca-key.pem -config="/etc/cfssl/certs/cfssl-config.json" -profile="intermediate" /etc/cfssl/certs/intermediate_ca.csr | cfssljson -bare /etc/cfssl/certs/intermediate_ca

cfssl gencert -ca /etc/cfssl/certs/intermediate_ca.pem -ca-key /etc/cfssl/certs/intermediate_ca-key.pem -config="/etc/cfssl/certs/cfssl-config.json" -profile="ocsp" ocsp.csr.json | cfssljson -bare /etc/cfssl/certs/ocsp

echo "custom:" | tee -a $HOME/go/pkg/mod/github.com/cloudflare/cfssl*/certdb/pg/dbconf.yml
echo "  driver: postgres" | tee -a $HOME/go/pkg/mod/github.com/cloudflare/cfssl*/certdb/pg/dbconf.yml
echo "  open: user=stecca password=2zyJ2mUF8atRdep5 dbname=cfssl sslmode=disable" | tee -a $HOME/go/pkg/mod/github.com/cloudflare/cfssl*/certdb/pg/dbconf.yml

cp ./cfssl.service /etc/systemd/system/

echo "Now, use the generated pem certs in lemur configuration (edit bottom of lemur.conf.py) then presse ENTER"
echo "ROOT"
cat /etc/cfssl/certs/root_ca.pem
echo "INTERMEDIATE"
cat /etc/cfssl/certs/intermediate_ca.pem
read -p "Press Enter to continue" </dev/tty

git clone --depth=1 https://github.com/Netflix/lemur.git lemur-build-docker/lemur
docker-compose up -d

goose --env custom -path $HOME/go/pkg/mod/github.com/cloudflare/cfssl*/certdb/pg up

systemctl daemon-reload
systemctl enable cfssl.service
systemctl start cfssl.service

cfssl ocspdump -db-config /etc/cfssl/db_config.json> /etc/cfssl/ocspdump
cfssl ocspserve -port=8889 -responses=/etc/cfssl/ocspdump  -loglevel=0

#ufw allow 8889
#ufw allow 8888 only from lemur container

#add to ctontab the ocsdump command
crontab -e

exit 0