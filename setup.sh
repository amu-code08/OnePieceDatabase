#!/bin/bash

### 必要な場合以下を変更する。
### APP_SRCはソースコードを置くパスです。
APP_SRC=$HOME/dm_src
### APP_NAMEはURIの一部になります。http://user.keio.ac.jp/~$USER/$APP_NAME/
APP_NAME=dm_app

### ITC/Env specific parameters
ITC_USER=$USER
APP_URI="/~${ITC_USER}/${APP_NAME}"
HTML_DIR=$HOME/public_html/${APP_NAME}
PYTHON_EXE=/home/kyozai/dm_flask/Python-3.10.10/python
ITCWEB_PYTHON_PATH=/usr/local/bin/python3

### Step1. Source setup
echo "[1/3] Setting up application source at $APP_SRC"
if [ ! -d $APP_SRC ] || [ ! -d $APP_SRC/venv ]; then
    git clone https://github.com/FujikiLab/dm_app.git $APP_SRC
    cd $APP_SRC
    echo "-- Creating VENV. This will take a while."
    $PYTHON_EXE -m venv venv
    ln -s $ITCWEB_PYTHON_PATH venv/bin/python_itc
    source venv/bin/activate
    pip install Flask
    echo ""
    echo "-- Done setting up source and venv."
else 
    cd $APP_SRC
    source venv/bin/activate
    echo "-- Source directory already exists."
fi
echo "-- To activate VENV, use \"source $APP_SRC/venv/bin/activate\""
echo "-- To exit, use \"deactivate\""


### Step2. Load sample database
echo ""
echo "[2/3] Loading sample database"
if [ -f database.db ]; then
    echo "-- database.db already exists."
else
    sqlite3 database.db < sample.sql
fi


### Step3. Deploy
echo ""
echo "[3/3] Deploying app for URI $APP_URI"
mkdir -p $HTML_DIR
chmod 755 $HTML_DIR
cat << EOF > $HTML_DIR/.htaccess
AddHandler cgi-script .cgi
Options +ExecCGI

RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^(.*)$ ${APP_URI}/index.cgi/\$1 [L]
EOF

cat << EOF > $HTML_DIR/index.cgi
#!${APP_SRC}/venv/bin/python_itc
APP_DIR = '${APP_SRC}'
ALIAS = '${APP_URI}'

import cgitb
cgitb.enable()

from wsgiref.handlers import CGIHandler
import os, sys
os.environ["SCRIPT_NAME"] = ALIAS
os.chdir(APP_DIR)
sys.path.append(APP_DIR)

from app import app

CGIHandler().run(app)
EOF

chmod 755 $HTML_DIR/index.cgi
echo "-- Done. http://user.keio.ac.jp$APP_URI/"
