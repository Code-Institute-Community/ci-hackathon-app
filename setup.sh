#!/bin/bash
echo "Gathering the force"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
FILE="$DIR/Pipfile"
randompass=`openssl rand -base64 16`
mkdir .venv
cp .env_sample .env && sed -i '' -e 's/localhost/*/g' .env
sed -i '' -e "s/your_secret_key_here/$randompass/g" .env
echo "Setting up pipenv"
pip3 install pipenv

if [ -e "$FILE " ]
then
echo "============================"
echo "Using Pipefile for installing"
echo "============================"
pipenv install
else
echo "============================"
echo "Using requirements.txt"
echo "============================"
pipenv install --three -r requirements.txt
fi
echo "============================"
echo "Setting up VSCode with Django Linting"
echo "============================"
pipenv install --dev pylint pylint-django pep8 autopep8
cp vscode_settings_sample.json .vscode/settings.json
echo "============================"
echo "Installing Python extension"
echo "============================"
code --install-extension ms-python.python
clear
echo "============================"
echo "Please restart VSCode if running"
echo "============================"