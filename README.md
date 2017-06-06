# AppServer
the server of the internet online movie ticketing system

# Environment

python3.5, mysql, redis

# Setting
* create a config file in directory app such as app/your_config.py
* then complete the setting in your_config.py files
* set the envvar
  * $export YOURAPPLICATION_SETTINGS=your_config.py

# Deploy

* Install require package
  * pip3 install -r requirements.txt
* Create database migrate repo
  * python3 managy.py db init
* Create database migrate script
  * python3 managy.py db migrate -m "initial migration"
* Run the script
  * python3 managy.py db upgrade
* Run the server
  * python3 managy.py runserver