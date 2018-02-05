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

## Generate removed threads
```
cd removed-threads
source .venv/bin/activate
python get-removed-threads.py
```
## Generate banned subs
**WARNING: be careful running these scripts. The first script uses 2 GB of RAM and the second one runs 32 terminals in parallel. Save other stuff before running this, it might just crach your computer** 
```
cd banned-subreddits
# Approximate 3 min
python quarantined-subs.py
# Approximate 2 hours
bash banned-subs-parallel.sh
```
