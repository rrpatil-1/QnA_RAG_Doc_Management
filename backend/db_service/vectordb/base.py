from abc import ABC, abstractmethod


class VectorDbServicesAbstract(ABC):

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
    def insert_embedding(self, Document_list):
        """
        Insert an embedding into the vector database
        
        Args:
            document_list (list): List of documents to insert into the database
            
            
        Returns:
            bool: Success status of the insertion
        """
        pass

    @abstractmethod
    def search_similar_doc(self, query,limit=5):
        """
        Search for similar documents in the database
        querying with the input text   
        default limit is 5
        returns the top k similar documents
        """
        pass

    @abstractmethod
    def delete_embedding(self, id):
        """
        Delete an embedding from the database
        
        Args:
            id: The identifier of the embedding to delete
            namespace (str): The namespace/collection containing the embedding
            
        Returns:
            bool: Success status of the deletion
        """
        pass
