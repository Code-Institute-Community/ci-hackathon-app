#!/bin/bash
echo "Gathering the force"
mkdir .venv
cp .env_sample .env && sed -i '' -e 's/localhost/*/g' .env
echo "Setting up pipenv"
pip3 install pipenv
pipenv install -r requirements.txt
clear
echo "============================"
echo "Please edit .env file and add your secret key"
echo "PRO TIP: run this command to generate one for you"
echo "Run the below command 👇"
echo "openssl rand -base64 16"
echo "============================"
echo ""
echo "============================"
echo "Please make sure you installed python extension if using vscode"
echo "If restarted please select python interpreter selecting .venv"
echo "============================"


