from abc import ABC, abstractmethod


class VectorDbServicesAbstract(ABC):from abc import abstractmethod

@abstractmethod
def get_namespace_list(self):
    pass

@abstractmethod
def create_embedding(self, text):
    """
    Create embeddings for the input text
    
    Args:
        text (str): The text to create embeddings for
        
    Returns:
        list: The embedding vector
    """
    pass

@abstractmethod
def insert_embedding(self, embedding, metadata, namespace):
    """
    Insert an embedding into the vector database
    
    Args:
        embedding (list): The embedding vector to insert
        metadata (dict): Additional metadata to store with the embedding
        namespace (str): The namespace/collection to store the embedding in
        
    Returns:
        bool: Success status of the insertion
    """
    pass

@abstractmethod
def search_similar(self, query_embedding, namespace, limit=5):
    """
    Search for similar vectors in the database
    
    Args:
        query_embedding (list): The query embedding vector
        namespace (str): The namespace/collection to search in
        limit (int): Maximum number of results to return
        
    Returns:
        list: List of similar items with their similarity scores
    """
    pass

@abstractmethod
def delete_embedding(self, id, namespace):
    """
    Delete an embedding from the database
    
    Args:
        id: The identifier of the embedding to delete
        namespace (str): The namespace/collection containing the embedding
        
    Returns:
        bool: Success status of the deletion
    """
    pass
