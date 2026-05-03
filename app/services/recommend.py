import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.database.db import books_collection
from bson import ObjectId

class Recommender:
    def __init__(self):
        self.books_df = None
        self.similarity_matrix = None
        self.tfidf_matrix = None

    def load_data(self):
        """Fetch books from MongoDB and prepare a DataFrame."""
        books = list(books_collection.find())
        if not books:
            return False
        
        # Prepare data for vectorization
        data = []
        for b in books:
            # Combine categories and description for better context
            categories = " ".join(b.get("category", []))
            description = b.get("description", "")
            title = b.get("title", "")
            author = b.get("author", "")
            
            combined_text = f"{title} {author} {categories} {description}"
            
            data.append({
                "_id": str(b["_id"]),
                "combined_text": combined_text.lower()
            })
        
        self.books_df = pd.DataFrame(data)
        return True

    def train(self):
        """Calculate the TF-IDF similarity matrix."""
        if not self.load_data():
            return False
            
        tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = tfidf.fit_transform(self.books_df['combined_text'])
        self.similarity_matrix = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
        return True

    def get_recommendations(self, book_id, top_n=5):
        """Return top N similar books for a given book_id."""
        if self.books_df is None or self.similarity_matrix is None:
            if not self.train():
                return []

        try:
            # Find the index of the book
            idx = self.books_df.index[self.books_df['_id'] == str(book_id)].tolist()
            if not idx:
                return []
            
            idx = idx[0]
            
            # Get similarity scores for this book
            sim_scores = list(enumerate(self.similarity_matrix[idx]))
            
            # Sort by similarity score
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            
            # Get top N (excluding the book itself)
            sim_scores = sim_scores[1:top_n+1]
            
            book_indices = [i[0] for i in sim_scores]
            recommended_ids = self.books_df.iloc[book_indices]['_id'].tolist()
            
            # Fetch full book details from DB
            recommended_books = []
            for rid in recommended_ids:
                book = books_collection.find_one({"_id": ObjectId(rid)})
                if book:
                    recommended_books.append({
                        "_id": str(book["_id"]),
                        "title": book.get("title"),
                        "author": book.get("author"),
                        "cover": book.get("cover"),
                        "rating": book.get("rating"),
                        "category": book.get("category")
                    })
            
            return recommended_books
        except Exception as e:
            print(f"Recommendation error: {e}")
            return []

# Singleton instance
recommender = Recommender()
