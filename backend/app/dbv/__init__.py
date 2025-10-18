from contextlib import contextmanager
from typing import Generator
from urllib.parse import urlparse

from pymilvus import Connections, MilvusClient, connections
from pymilvus.exceptions import MilvusException, MilvusUnavailableException

from app.core.config import settings


@contextmanager
def dbv_client() -> Generator[MilvusClient, None, None]:
    try:
        dbv: MilvusClient = MilvusClient(
            uri=settings.VECTOR_DATABASE_URI,
            token="root:Milvus",
        )
        yield dbv

    except (MilvusUnavailableException, MilvusException):
        raise
    finally:
        dbv.close()


@contextmanager
def dbv_connection(db_name: str = "default") -> Generator[Connections, None, None]:
    try:
        url = urlparse(settings.VECTOR_DATABASE_URI)

        dbv: Connections = connections.connect(
            db_name=db_name, host=url.hostname, port=url.port
        )
        yield dbv

    except (MilvusUnavailableException, MilvusException):
        raise
    finally:
        dbv.disconnect(db_name)
