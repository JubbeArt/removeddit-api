# Removeddit API
Closed (for now) API for removeddit.

# Endpoints

## /api/threads
Get a list of removed thread ids

### Params
page: integer (starts at 0)

subreddit: string 

## /api/subreddits
Get a list of banned subs

### Params
page: integer (starts at 0)



# Production

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
```
## Database
Set database info in `config.py` and then import the database provided in the repo

```
mysql -u root -p removeddit < removeddit.sql
```

Alternatively create an empty database with
```
python setup-database.py
```

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