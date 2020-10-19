@ECHO OFF
ECHO Gathering the force
MKDIR  .venv
ECHO CREATING .env file
ECHO DEVELOPMENT=1 >> .env
ECHO SECRET_KEY="your_secret_key_here" >> .env
ECHO SITE_NAME="*" >> .env
ECHO Installing Python extension
pip install pipenv
CLS
@ECHO OFF
ECHO Installing requirements.txt
pipenv install -r requirements.txt
ECHO ============================
ECHO Setting up VSCode with Django Linting
ECHO ============================
pipenv install --dev pylint pylint-django pep8 autopep8
COPY vscode_settings_sample.json .vscode/settings.json
ECHO ============================
ECHO Installing Python extension
ECHO ============================
code --install-extension ms-python.python
echo
ECHO ============================
ECHO Please edit .env file and add your secret key
ECHO Please restart VSCode if running
ECHO ============================
