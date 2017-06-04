# AppServer
the server of the internet online movie ticketing system

# Environment

python3.5, mysql, redis

# Setting
* mysql database name: ticketingServerDev
* root password: 12234810

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