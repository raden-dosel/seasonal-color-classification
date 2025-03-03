import sqlite3
import nltk
from nltk.corpus import wordnet as wn
nltk.download('wordnet')

def initialize_database():
    conn = sqlite3.connect("garments.db")
    
    # Create FTS5 virtual table (no need for load_extension)
    conn.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS garments_index 
        USING fts5(category, type, design, season, filename)
    ''')
    
    # Insert sample data
    sample_garments = [
        ("dresses", "casual flowy", "floral v-neck", "summer", "garment1001.gltf"),
        ("shirts", "polo", "striped", "spring", "garment2001.gltf"),
    ]
    conn.executemany('''
        INSERT INTO garments_index (category, type, design, season, filename) 
        VALUES (?, ?, ?, ?, ?)
    ''', sample_garments)
    conn.commit()
    return conn

def get_synonyms(term):
    """Retrieve synonyms for a term using WordNet."""
    synonyms = set()
    for synset in wn.synsets(term):
        for lemma in synset.lemmas():
            synonyms.add(lemma.name().replace('_', ' '))  # Normalize underscores
    return synonyms

def expand_query(query):
    """Generate an FTS5-friendly search query with synonyms."""
    terms = query.lower().split()
    expanded_terms = []
    for term in terms:
        synonyms = get_synonyms(term)
        expanded_terms.extend(synonyms)
        expanded_terms.append(term)  # Include original term
    unique_terms = list(set(expanded_terms))
    # Construct an 'OR' query with wildcards
    return ' OR '.join([f'"{term}*"' for term in unique_terms])

def search_garments(conn, query):
    """Search garments using an expanded query and rank results by relevance."""
    cursor = conn.cursor()
    
    # Generate expanded query with synonyms
    expanded_query = expand_query(query)
    # Execute with parameter substitution to prevent SQL injection
    cursor.execute('''
        SELECT filename, rank 
        FROM garments_index 
        WHERE garments_index MATCH ? 
        ORDER BY rank  -- FTS5 ranks more relevant matches first
    ''', (expanded_query,))
    
    # Extract filenames and ranks
    results = cursor.fetchall()
    return [row[0] for row in results]  # Return filenames in order of relevance

# Example usage
if __name__ == "__main__":
    conn = initialize_database()
    results = search_garments(conn, "casual summer dresses")
    print(f"Matching 3D garments (ranked): {results}")