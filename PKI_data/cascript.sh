#!/bin/bash
set -e

if [[ $1 == "reset" ]]; then
	rm -fr rootca subca
	echo -e "\e[31m Cleaning up"
	echo -e "\e[0m"
fi


##### COLOR CODES \e[93 yellow \e[31 red \e[32 grep \e[34 blue

############ROOT CA#############
echo -e "\e[93m Starting to generate RootCA data"
echo -e "\e[0m"
mkdir rootca
cd rootca
mkdir certs
mkdir crl
mkdir newcerts
mkdir private
touch serial
echo 0100 > serial
touch index.txt
touch crlnumber
echo 0100 > crlnumber
#openssl rand -out ./private/.rand 1024
#this generates an rsa private key (this is used to sign or encrypt stuff)
echo -e "\e[93m Generating Root CA private key"
echo -e "\e[0m"
openssl genrsa -out ./private/cakey.pem -des3
#-rand ./private/.rand 2048
echo -e "\e[93m Generating Root CA x509 Certificate"
echo -e "\e[0m"
openssl req -x509 -new -key ./private/cakey.pem -out cacert.pem -config ../openssl.cnf

#########SUB CA TODO:CHECK FILENAMES##########

echo -e "\e[31m Starting to generate SubCA data"
echo -e "\e[0m"
echo $pwd
cd ..
mkdir subca
cd subca
mkdir certs
mkdir crl
mkdir newcerts
mkdir private
touch subserial
echo 0100 > subserial
touch index.txt
touch subcrlnumber
echo 0100 > crlnumber
#openssl rand -out ./private/.rand 1024
echo -e "\e[93m Generating Sub CA private key"
echo -e "\e[0m"
openssl genrsa -out ./private/subcakey.pem -des3
# -rand ./private/.rand 2048
echo -e "\e[93m Generating SubCA Certificate Request"
echo -e "\e[0m"
openssl req -new -key ./private/subcakey.pem -out subcareq.pem -config ../opensslsub.cnf

cd ../rootca/
echo -e "\e[93m Entering Root CA Role"
echo -e "\e[0m"
openssl ca -in ../subca/subcareq.pem -extensions v3_ca -config ../openssl.cnf
echo -e "\e[93m Entering Sub CA Role to Generate Client Cert"
echo -e "\e[0m"
cd ../subca/ #entering subca directory
cp ../rootca/newcerts/0100.pem subcacert.pem
cp ../clientgen.sh ../subca
echo -e "\e[93m cd subca and now..."
echo -e "\e[93m you are a SubCA, run ./clientgen.sh nrofclients to generate your clients certificates"
echo -e "\e[0m"

###### CODE OF DATABASE #######
#sqlite3 -batch keys.db "create table users (id INTEGER PRIMARY KEY,username TEXT,keyinfo BLOB);"


