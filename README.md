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
pip3 install virtualenv
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
