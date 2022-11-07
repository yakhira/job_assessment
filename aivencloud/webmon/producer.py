import json
import logging.config
import time
import re
import os
import requests
from datetime import datetime
from config import KAFKA_HOST, KAFKA_CERT_FILE, KAFKA_CA_FILE, \
    KAFKA_KEY_FILE, KAFKA_TOPIC, DEFAULT_LOGGING, MONITOR_INTERVAL, MONITOR_URLS_FILE
from data.broker import Broker

logging.config.dictConfig(DEFAULT_LOGGING)


def poll_site(item):
    url = item.get("url")
    regex = item.get("regex")

    try:
        response = requests.get(url)
        match = regex and re.search(regex, response.text)

        result = {
            'timestamp': str(datetime.now()),
            'url': url,
            'status_code': response.status_code,
            'response_time': response.elapsed.total_seconds(),
            'regex_match': match and match.group(0),
        }
    except requests.exceptions.RequestException as err:
        result = {
            'timestamp': str(datetime.now()),
            'url': url,
            'status_code': 500,
            'response_time': -1,
            'regex_match': None,
        }
        logging.error(err)

    return result

def main():
    monitoring_urls = []
    broker = Broker(
        KAFKA_HOST, KAFKA_CA_FILE, KAFKA_CERT_FILE, KAFKA_KEY_FILE
    )

    broker.create_topic(KAFKA_TOPIC)

    if os.path.exists(MONITOR_URLS_FILE):
        with open(MONITOR_URLS_FILE, "r") as fp:
            monitoring_urls = json.loads(fp.read())

    if monitoring_urls:
        try:
            while True:
                for item in monitoring_urls:
                    broker.publish(KAFKA_TOPIC, poll_site(item))
                time.sleep(MONITOR_INTERVAL)
        except KeyboardInterrupt:
            print('Exiting!')
    else:
        print("No urls found to monitor.")


if __name__ == "__main__":
    main()
