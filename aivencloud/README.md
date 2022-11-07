# Webmon

Webmon is a website status poller that uses Kafka to move info about website
status to a PostgreSQL.  These are examples of things you can do with Aiven
services.

## Requirements

Python 3.6+

## Setup

### Prepare monitoring urls

Create file monitoring.json with list of urls, regex parameter if optional and helps to check response text from monitored url.
```
[
    {
        "url": "https://httpstat.us/200",
        "regex": "200 OK"
    },
    {
        "url": "https://httpstat.us/404",
        "regex": "404.*"
    },
    {
        "url": "https://tls-v1-2.badssl.com:1012/"
    }
]
```

### Get kafka connection settings
1. Login to https://console.aiven.io
2. Go services and find kafka service
3. Find connection information
4. Copy "Service URI" and download certificates to folder webmon/certs

### Get PostgreSQL settings
1. Login to https://console.aiven.io
2. Go services and find kafka service
3. Find connection information
4. Copy "Service URI" 

## Run
```
$ export KAFKA_HOST=<kafka service uri>
$ export KAFKA_CERT_FILE=certs/service.cert
$ export KAFKA_KEY_FILE=certs/service.key 
$ export KAFKA_CA_FILE=certs/ca.pem
$ export PG_CONNECTION_STRING="<PostgreSQL service uri>"

$ pip instal -r requirements.txt
$ python consumer.py
$ python producer.py
```

## Tests
```
$ python --version
$ pip install tox
$ tox -a
$ tox -e py<version>
```