import os
import sys
from urllib.parse import urlparse

import psycopg

try:
    url = urlparse(os.getenv("DATABASE_URI", ""))
    psycopg.connect(
        dbname=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port,
    )
except psycopg.OperationalError:
    print("- PostgreSQL unavaliable - waiting")
    sys.exit(-1)
sys.exit(0)
