# gluru-backend
Support portal backend

## Prequites
 - Postgresql
 - Python3.6
 - Pipenv
 - Redis

### Install & Configure Postgresql
Please refer to this [link](https://www.postgresql.org/download/) to install Postgresql

Configure postgresql:
```
sudo su postgres
psql
CREATE DATABASE database_name;
CREATE USER my_username WITH PASSWORD 'my_password';
GRANT ALL PRIVILEGES ON DATABASE "database_name" to my_username;
```

### Installing Python3.6 and Pipenv
Please refer to this [link](https://docs.pipenv.org/) for more details about pipenv

Installing Python3.6 and pipenv
```
sudo yum install -y python36u python36u-libs python36u-devel python36u-pip
pip3.6 install pipenv
```

### Install redis server
Pleare refer to this [link](https://redis.io/topics/quickstart) for quick overview of redis
```
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
make install
redis-server
```

## Clone and installing project
```
git clone git@github.com:GluuFederation/gluru-backend.git
cd gluru-backend
pipenv install
pipenv shell
python manage.py runserver
celery worker -A gluru_backend --loglevel=DEBUG --concurrency=4
```