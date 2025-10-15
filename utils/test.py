from chromadb import Client

from configurations.configs import get_vector_db_collection_name

client = Client()
collection = client.get_collection(get_vector_db_collection_name())

data = collection.get()
print(data)