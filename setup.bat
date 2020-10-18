@ECHO OFF
ECHO Gathering the force
MKDIR  .venv
ECHO CREATING .env file
ECHO DEVELOPMENT=1 >> .env
ECHO SECRET_KEY="your_secret_key_here" >> .env
ECHO SITE_NAME="*" >> .env
ECHO Installing pipenv for development use
pip install pipenv
CLS
@ECHO OFF
ECHO Installing requirements.txt
pipenv install -r requirements.txt

ECHO ============================
ECHO Please edit .env file and add your secret key
ECHO ============================
ECHO Please make sure you installed python extension if using vscode
ECHO If restarted please select python interpreter selecting .venv
ECHO ============================

