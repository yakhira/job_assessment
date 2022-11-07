export KAFKA_HOST=host:port
export KAFKA_CERT_FILE=certs/service.cert
export KAFKA_KEY_FILE=certs/service.key 
export KAFKA_CA_FILE=certs/ca.pem
export PG_CONNECTION_STRING="postgres://user:pass@host:port/defaultdb?sslmode=require"

python consumer.py