# Removeddit API
Closed (for now) API for removeddit.

# Endpoints

## /api/banned


# Development
## Setup

### MySQL
```
sudo apt update
sudo apt install mysql-server
mysql_secure_installation
```

### Python packages
```
sudo apt install build-essential python3-dev
pip install virtualenv
virtualenv -p python3 .venv
source .venv/bin/activate
pip install -r requirements.txt
```
### Database
Set database info in `config.py` and the run

```
python setup-database.py
```

## Generate banned subs
**WARNING: be careful running these scripts. The first script uses 2 GB of RAM and the second one runs 32 terminals in parallel. Save other stuff before running this, it might just crach your computer** 
```
cd banned-subs
# Approximate 3 min
python quarantined-subs.py
```