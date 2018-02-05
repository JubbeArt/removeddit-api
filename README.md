# Removeddit API
Closed (for now) API for removeddit.

# Endpoints

## /api/banned


# Development
## MySQL
```
sudo apt update
sudo apt install mysql-server
# I do: no, no, then all yes for the security questions
mysql_secure_installation
```

## Python packages
```
sudo apt install build-essential python3-dev python3-pip
sudo -H pip3 install virtualenv
virtualenv -p python3 .venv
source .venv/bin/activate
pip install -r requirements.txt
```
## Database
Set database info in `config.py` and the run

```
python setup-database.py
```
## Start uwsgi server
```
source .venv/bin/activate
uwsgi --http :9000 --wsgi-file api.py --callable app
```

# Production

## Server directory
```
sudo mkdir /srv/removeddit-api /srv/removeddit-api/socket /srv/removeddit-api/site
sudo git clone https://github.com/JubbeArt/removeddit-api.git /srv/removeddit-api/site
cd /srv/removeddit-api/site
sudo virtualenv -p python3 .venv
source .venv/bin/activate
sudo .venv/bin/pip install -r requirements.txt
sudo chown -R www-data:www-data /srv/removeddit-api
```

## uWsgi

Disable default LSB service
```
systemctl stop uwsgi-emperor
systemctl disable uwsgi-emperor
```

Install new service
```
sudo apt install uwsgi uwsgi-emperor uwsgi-plugin-python3
sudo mkdir -p /etc/uwsgi-emperor/vassals
sudo cp /srv/removeddit-api/site/production/removeddit-api.ini /etc/uwsgi-emperor/vassals/
sudo cp /srv/removeddit-api/site/production/emperor.uwsgi.service /etc/systemd/system/emperor.uwsgi.service

systemctl daemon-reload
systemctl enable nginx emperor.uwsgi
systemctl reload nginx
systemctl start emperor.uwsgi
```

## nginx
See https://github.com/JubbeArt/removeddit

Just removed the comments for the /api/ route. 