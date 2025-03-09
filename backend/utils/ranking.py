
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from rank_bm25 import BM25Okapi
import numpy as np

# Download required NLTK data
nltk.download('punkt_tab')
nltk.download('stopwords')


class BM25Retriever:
    def __init__(self):
        self.bm25 = None
        self.corpus = None
        self.stop_words = set(stopwords.words('english'))
        
    def preprocess_text(self, text):
        # Tokenize and remove stopwords
        tokens = word_tokenize(text.lower())
        tokens = [token for token in tokens if token not in self.stop_words]
        return tokens
        
    def fit(self, corpus):
        # Preprocess corpus
        self.corpus = corpus
        tokenized_corpus = [self.preprocess_text(doc) for doc in corpus]
        
        # Create BM25 model
        self.bm25 = BM25Okapi(tokenized_corpus)
        
    def retrieve(self, query, top_k=5):
        # Preprocess query
        tokenized_query = self.preprocess_text(query)
        
        # Get BM25 scores
        scores = self.bm25.get_scores(tokenized_query)
        
        # Get top k document indices
        top_indices = np.argsort(scores)[::-1][:top_k]
        
        # Return top k documents and their scores
        results = [(self.corpus[i], scores[i]) for i in top_indices]
        
        return results
    def retrieve_with_threshold(self, query, corpus, threshold=0.5):
        """
        Retrieve relevant documents above a threshold score
        Args:
            query: Query text to search for
            corpus: List of documents to search in
            threshold: Minimum score threshold for retrieval (default 0.5)
        Returns:
            List of (document, score) tuples above threshold
        """
        # Fit the model on the corpus
        self.fit(corpus)
        
        # Get results using retrieve method
        results = self.retrieve(query)
        
        # Filter results above threshold
        filtered_results = [(doc, score) for doc, score in results if score >= threshold]
        
        return filtered_results
