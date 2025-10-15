import os

from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from google import genai
import chromadb

from configurations.configs import get_embeddings_client_api_key, get_vector_db_collection_name, get_embedding_model


class EmbeddingUtils:

    def __init__(self):
        load_dotenv()
        self.embeddings_client = genai.Client(api_key=get_embeddings_client_api_key())
        db_client = chromadb.Client()
        self.collection = db_client.get_or_create_collection(get_vector_db_collection_name())
        self.embedding_model = get_embedding_model()

    def create_embedding(self, text: str):
        """
        Creates chunk of the string and creates its embedding
        :param text: the text to be embedded
        :return: list of embeddings and text chunks
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,  # you can tune this
            chunk_overlap=50,  # slight overlap helps retain context
        )
        # create chunks
        chunks = text_splitter.split_text(text)
        # we'll store embeddings
        embeddings = []
        texts = []
        # pass chunks to llm to create embedding
        for chunk in chunks:
            response = self.embeddings_client.models.embed_content(
                model=self.embedding_model,  # Gemini embedding model
                contents=chunk
            )
            # extract embedding from response and store
            texts.append(chunk)
            embeddings.append(response.embeddings[0].values)
        return embeddings, texts

    def store_embeddings(self, embeddings: list, texts: list):
        """
        Stroes the embeddings in vector databse
        :param embeddings: Embeddings to be saved
        :param texts: Chunks against those embeddings
        :return:
        """
        # add ids to embeddings
        ids = [str(i) for i in range(len(embeddings))]
        # Add embeddings to Chroma
        self.collection.add(ids=ids, embeddings=embeddings, documents=texts)

    def query_embeddings(self, user_query: str):
        """
        Queries the embeddings for a user query
        :param user_query:
        :return:
        """
        query_response = self.embeddings_client.models.embed_content(
            model=self.embedding_model,
            contents=user_query,
        )
        query_vector = query_response.embeddings[0].values

        return self.collection.query(query_embeddings=[query_vector], n_results=4)
