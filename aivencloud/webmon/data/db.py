from kafka import logging
from psycopg2 import sql, connect as ps_connect
from psycopg2 import extensions, errors


class DB:
    """Database proxy class.

    Helps to manage database operations, such creating tables and insert formatted records.

    Arguments
        connection_string (str): database connection string with user, password, hostname, port.
    """

    def __init__(self, connection_string):
        self.__connection_string = connection_string
        self.__connection = None

    def __db_connection(self):
        if not self.__connection or self.__connection.status == extensions.STATUS_READY:
            self.__connection = ps_connect(self.__connection_string)
        return self.__connection

    def create_webmon_table(self, table):
        """
        Create webmon table in database with given name.

        Commit ROLLBACK in case DuplicateTable error, using lazy function to make db connection.

        Arguments
            table (str): table name.
        """
        connection = self.__db_connection()

        try:
            connection.cursor().execute(
                f"""
                    create table {table}
                    (
                        timestamp timestamp with time zone primary key,
                        url varchar,
                        status_code integer,
                        response_time float,
                        regex_match varchar
                    );
                """
            )
            connection.commit()
        except errors.DuplicateTable:
            connection.cursor().execute("ROLLBACK")
            connection.commit()

    def insert_webmon_record(self, table, message):
        """Insert monitoring record into table.

        Using lazy function to make db connection.

        Arguments
            table (str): table name to insert record
            message (dict): record data.

        Returns
            bool: result flag.
        """
        connection = self.__db_connection()

        try:
            names = [
                "timestamp",
                "url",
                "status_code",
                "response_time",
                "regex_match"
            ]

            query = sql.SQL("insert into {} ({}) values({})").format(
                sql.Identifier(table),
                sql.SQL(", ").join(map(sql.Identifier, names)),
                sql.SQL(", ").join(map(sql.Placeholder, names))
            )

            connection.cursor().execute(query, message)
            connection.commit()
            return True
        except AttributeError as err:
            logging.error(f"Broken message format: {message}!")
        except errors.UndefinedTable:
            logging.error(f"Table {table} doesn't exist!")
        except errors.SyntaxError as err:
            logging.error(err.pgerror)

        return False

    def close(self):
        """Close database connection."""
        return self.__connection.close()
