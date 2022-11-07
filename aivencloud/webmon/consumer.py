import logging.config
import time
from config import KAFKA_HOST, KAFKA_CERT_FILE, KAFKA_CA_FILE, \
    KAFKA_KEY_FILE, KAFKA_TOPIC, DEFAULT_LOGGING, PG_CONNECTION_STRING, PG_TABLE
from data.broker import Broker
from data.db import DB

logging.config.dictConfig(DEFAULT_LOGGING)


def main():
    broker = Broker(
        KAFKA_HOST, KAFKA_CA_FILE, KAFKA_CERT_FILE, KAFKA_KEY_FILE
    )
    db = DB(PG_CONNECTION_STRING)

    db.create_webmon_table(PG_TABLE)
    broker.create_topic(KAFKA_TOPIC)

    consumer = broker.subscribe(KAFKA_TOPIC)

    try:
        while True:
            message_batch = consumer.poll()

            for partition_batch in message_batch.values():
                for message in partition_batch:
                    if db.insert_webmon_record(PG_TABLE, message.value):
                        consumer.commit()
            time.sleep(1)
    except KeyboardInterrupt:
        db.close()
        print('Exiting!')


if __name__ == "__main__":
    main()
