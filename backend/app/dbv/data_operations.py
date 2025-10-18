import os

from app.agent.rag.data import load_documents
from app.agent.rag.index import DocumentIndexer
from app.core.config import settings
from app.dbv import dbv_client


def is_milvus_empty():
    with dbv_client() as client:
        collections = client.list_collections()
        collection_intersection = set(collections).intersection(
            settings.DATA_COLLECTIONS
        )

        if collection_intersection != settings.DATA_COLLECTIONS:
            print("- Milvus - missing following collections")
            print(collection_intersection)
            return True

        for collection in collections:
            if (
                client.get_collection_stats(collection_name=collection)["row_count"]
                == 0
            ):
                return True

        return False


def initialize_milvus_db():
    for collection_name in settings.DATA_COLLECTIONS:
        print(f"Loading collection -> {collection_name}")
        documents = load_documents(
            input_dir=os.path.join(settings.DATA_BASE_PATH, collection_name)
        )
        _ = DocumentIndexer(documents, collection_name)


def prune_milvus_db():
    with dbv_client() as client:
        for collection in client.list_collections():
            print(f"Dropping collection -> {collection}")
            client.drop_collection(collection_name=collection)
