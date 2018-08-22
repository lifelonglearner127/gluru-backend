# gluru-backend
Support portal backend

## Prequites
 - Postgresql
 - Python3.6
 - Pipenv
 - RabbitMQ

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

### Install RabbitMQ
Pleare refer to this [link](http://www.rabbitmq.com/download.html) for quick overview of RabbitMQ
I used Redis as a broker first, but replace it by RabbitMQ.
Redis was created with a different intentions and not for being a message broker.

Installing Erlang:
```
wget https://packages.erlang-solutions.com/erlang-solutions-1.0-1.noarch.rpm
rpm -Uvh erlang-solutions-1.0-1.noarch.rpm
sudo yum install erlang
```

Install RabbitMQ Server:
```
curl -s https://packagecloud.io/install/repositories/rabbitmq/rabbitmq-server/script.rpm.sh | sudo bash
```

Run RabbitMQ Server:
```
sudo rabbitmq-server
```
 > `Important!` In order for this project to work properly, you need to start rabbitmq server first. For sms and email notification, signal is used to send messages to task queue. This means that the request context involve sending messages to task queue. If rabbitmq server not running at that time, it might lead to time out error.

## Clone and installing project
```
git clone git@github.com:GluuFederation/gluru-backend.git
cd gluru-backend
pipenv install
pipenv shell
python manage.py runserver
celery worker -A gluru_backend --loglevel=DEBUG --concurrency=4
```

Starting the Scheduler:
```
celery -A gluru_backend beat -l info
```

 > `Important!` Beat does not execute tasks, it just sends the messages.
 > You need both a beat instance and a worker instance!

Management Commands related to haystack:
```
python manage.py rebuild_index
python manage.py update_index
python manage.py clear_index
```
 > `Note!` We use [drf-haystack](https://drf-haystack.readthedocs.io/en/latest/index.html) and `whoosh` as a search engine

## Contribution
 - Create a new branch
 - Commit your changes and make a PR to master
 > `Important!` Before commit your changes, you need to run flake8 for code styling