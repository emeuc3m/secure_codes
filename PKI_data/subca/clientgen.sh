#!/bin/bash

####GENERATE AS MANY PRIVKEYS-CERT-REQ PER CLIENT
set -e
for id in $(seq	$1);
do

######CREATE CLIENT REQ###########
echo -e "\e[93m Creating Client Request"
echo -e "\e[0m"
openssl genrsa -out ./private/clientkey_$id.pem
openssl req -new -key ./private/clientkey_$id.pem -out client_req_$id.pem -config ../opensslsub.cnf
#####CREATE CLIENTS CERTS####
echo -e "\e[93m Signing Client Request"
echo -e "\e[0m"
openssl ca -in client_req_$id.pem -out client_cert_$id.pem -config ../opensslsub.cnf
openssl rsa -inform pem -in ./private/clientkey_$id.pem -outform der -out ./private/client${id}_privatek.der
openssl x509 -in client_cert_$id.pem -pubkey -noout | openssl enc -base64 -d > client${id}_publick.der

mkdir client_$id
mv *.der ./client_$id
mv ./private/*.der client_$id
mv *$id.pem ./client_$id

done;
