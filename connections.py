__author__ = 'Mihail Mihaylov'

import os
from contextlib import contextmanager
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv

load_dotenv()


pool = SimpleConnectionPool(minconn=1, maxconn=10, dsn=os.environ['DATABASE_URI'])


@contextmanager
def get_connection():
    """"Cache database connections """
    connection = pool.getconn()

    try:
        yield connection
    finally:
        pool.putconn(connection)
