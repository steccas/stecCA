#!/bin/bash

#ask if password and readme are done
read -r -p "Have you read the readme and setup your passwords? [y/N] " response
response=${response,,}    # tolower
if [[ "$response" =~ ^(yes|y)$ ]]
then
    #Install Go
    apt install software-properties-common gpg rsync jq
    add-apt-repository ppa:longsleep/golang-backports
    apt update
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F6BC817356A3D45E
    apt update && apt upgrade
    apt install golang-go

    #setup password from password config file
    source ./creds

    $json = "postgres://$users:$dbpass@localhost/cfssl?sslmode=disable"
    jq '.data_source = $json' --arg json $json ./db_config.json

    sed -i "s/^POSTGRES_USER=.*$/POSTGRES_PASSWORD=$user/" ./lemur_db.env ./database.env
    sed -i "s/^POSTGRES_PASSWORD=.*$/POSTGRES_PASSWORD=$dbpass/" ./lemur_db.env ./database.env
    sed -i "s/^LEMUR_ADMIN_PASSWORD=.*$/LEMUR_ADMIN_PASSWORD=$lempass/" ./lemur_db.env ./database.env
    unset $lempass

    #setup cfss env
    useradd cfssl
    mkdir -p /etc/cfssl/certs

    go get github.com/cloudflare/cfssl/cmd/...
    go get bitbucket.org/liamstask/goose/cmd/goose
    cp -r $HOME/go/bin/* /usr/local/bin/

    cp ./db_config.json /etc/cfssl/
    
    chown -R cfssl:cfssl /etc/cfssl

    rsync -avzhp ./csr_root_ca.json ./csr_intermediate_ca.json ./cfssl-config.json /etc/cfssl/certs/

    cfssl gencert -initca /etc/cfssl/certs/csr_root_ca.json | cfssljson -bare /etc/cfssl/certs/root_ca

    cfssl gencert -initca /etc/cfssl/certs/csr_intermediate_ca.json | cfssljson -bare /etc/cfssl/certs/intermediate_ca
    cfssl sign -ca /etc/cfssl/certs/root_ca.pem -ca-key /etc/cfssl/certs/root_ca-key.pem -config="/etc/cfssl/certs/cfssl-config.json" -profile="intermediate" /etc/cfssl/certs/intermediate_ca.csr | cfssljson -bare /etc/cfssl/certs/intermediate_ca

    cfssl gencert -ca /etc/cfssl/certs/intermediate_ca.pem -ca-key /etc/cfssl/certs/intermediate_ca-key.pem -config="/etc/cfssl/certs/cfssl-config.json" -profile="ocsp" ocsp.csr.json | cfssljson -bare /etc/cfssl/certs/ocsp

    chown -R cfssl:cfssl /etc/cfssl

    echo "custom:" | tee -a $HOME/go/pkg/mod/github.com/cloudflare/cfssl*/certdb/pg/dbconf.yml
    echo "  driver: postgres" | tee -a $HOME/go/pkg/mod/github.com/cloudflare/cfssl*/certdb/pg/dbconf.yml
    echo "  open: user=$user password=$dbpass dbname=cfssl sslmode=disable" | tee -a $HOME/go/pkg/mod/github.com/cloudflare/cfssl*/certdb/pg/dbconf.yml

    unset $dbpass

    #setup services and fw
    rsync -avzhp ./cfssl.service ./ocsp.service /etc/systemd/system/

    echo "Now, paste the generated pem certs (not the key) in lemur configuration (edit bottom of lemur.conf.py) and set the address of the ca (this machine address or DNS name) then press ENTER"
    echo "ROOT"
    cat /etc/cfssl/certs/root_ca.pem
    echo "INTERMEDIATE"
    cat /etc/cfssl/certs/intermediate_ca.pem
    read -p "Press Enter to continue" </dev/tty

    ufw allow 8889 #or change here to make your firewall allow oscp requests
    ufw allow from 192.168.48.4 to any port 8888 #or change here to make your firewall allow request to your ca only from lemur container

    git clone --depth=1 https://github.com/Netflix/lemur.git lemur-build-docker/lemur

    #start everything
    docker-compose up -d

    goose --env custom -path $HOME/go/pkg/mod/github.com/cloudflare/cfssl*/certdb/pg up

    systemctl daemon-reload
    systemctl enable cfssl.service
    systemctl enable ocsp.service
    systemctl start cfssl.service
    systemctl start ocsp.service

    cfssl ocspdump -db-config /etc/cfssl/db_config.json> /etc/cfssl/ocspdump
    #cfssl ocspserve -port=8889 -responses=/etc/cfssl/ocspdump  -loglevel=0

    docker-compose restart

    echo "We are almost ready please paste this command into the crontab that it is about to open then save. Press ENTER when ready"
    echo "cfssl ocspdump -db-config /etc/cfssl/db_config.json> /etc/cfssl/ocspdump"
    #add to crontab the ocsdump command
    crontab -e

    exit 0
else
    echo "Read the readme, and configure your passwords!"
fi

exit 1