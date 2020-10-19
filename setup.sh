#!/bin/bash
echo "Gathering the force"
randompass=`openssl rand -base64 16`
mkdir .venv
cp .env_sample .env && sed -i '' -e 's/localhost/*/g' .env
sed -i '' -e "s/your_secret_key_here/$randompass/g" .env
echo "Setting up pipenv"
pip3 install pipenv
pipenv install --three -r requirements.txt
clear
echo "============================"
echo "Please make sure you installed python extension if using vscode"
echo "If restarted please select python interpreter selecting .venv"
echo "============================"


