import ssl
import json
import logging

from kafka import KafkaConsumer, consumer
from kafka import KafkaProducer
from kafka import KafkaAdminClient
from kafka.admin import NewTopic


class Broker:
    """Broker proxy class.

    Creates producer and consumer objects, manages topic and secure connection.

    Arguments
        host (str): broker hostname with port in format host:port
        ca_file (str): CA file path
        cert_file (str): certificate file path
        cert_key (str): secret key file path
        group_name (str): optional group name to poll messages, default is group-1.
    """

    def __init__(self, host, ca_file, cert_file, cert_key, group_name="group-1"):
        self.__ssl_context = None
        self.__ca_file = ca_file
        self.__cert_file = cert_file
        self.__cert_key = cert_key
        self.__host = host
        self.__group_name = group_name
        self.__producer = None
        self.__consumer = None

    def __set_ssl_context(self):
        if not self.__ssl_context:
            self.__ssl_context = ssl.create_default_context(
                purpose=ssl.Purpose.CLIENT_AUTH,
                cafile=self.__ca_file,
            )
            self.__ssl_context.load_cert_chain(
                certfile=self.__cert_file,
                keyfile=self.__cert_key,
            )
        return self.__ssl_context

    def create_topic(self, topic):
        """Create topic, ignores any exception rises.

        Arguments
            topic (str): topic to create.
        """
        try:
            admin = KafkaAdminClient(
                bootstrap_servers=self.__host,
                security_protocol="SSL",
                ssl_context=self.__set_ssl_context()
            )
            new_topic = NewTopic(
                name=topic,
                num_partitions=1,
                replication_factor=2
            )
            admin.create_topics([new_topic])
        except Exception:
            pass

    def __init_consumer(self):
        if not self.__consumer:
            self.__consumer = KafkaConsumer(
                bootstrap_servers=self.__host,
                security_protocol="SSL",
                ssl_context=self.__set_ssl_context(),
                value_deserializer=lambda bs: json.loads(bs.decode("utf-8")),
                auto_offset_reset="earliest",
                enable_auto_commit=False,
                group_id=self.__group_name
            )
        return self.__consumer

    def __init_producer(self):
        if not self.__producer:
            self.__producer = KafkaProducer(
                bootstrap_servers=self.__host,
                security_protocol="SSL",
                ssl_context=self.__set_ssl_context(),
                max_block_ms=5000,
            )
        return self.__producer

    def subscribe(self, topic):
        """Subscribe to topic, using lazy function to init consumer.

        Arguments
            topic (str): topic to subscribe consumer.

        Returns
            Consumer object.
        """
        consumer = self.__init_consumer()
        consumer.subscribe(topic)
        return consumer

    def __on_send_error(self, excp):
        logging.error(excp)

    def publish(self, topic, message):
        """Publish message to topic, using lazy function to init producer.

        Arguments
            topic (str): Topic to publish message.
            message (str or dict): Message to publish (dict converted to json string).

        Returns
            FutureRecordMetadata: resolves to RecordMetadata.
        """
        try:
            message = json.dumps(message)
        except json.JSONDecodeError:
            pass

        producer = self.__init_producer()
        future = producer.send(topic, message.encode('ascii'))
        future.add_errback(self.__on_send_error)
        producer.flush()
        return future
