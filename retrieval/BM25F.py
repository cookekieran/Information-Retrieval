import spacy
from pyserini.search.lucene import LuceneSearcher

searcher = LuceneSearcher('indexes/trec_covid_lemmatized')
searcher.set_bm25(k1=0.9, b=0.4)
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

def search_trec_covid_bm25f(query, k=5, title_weight=2.0, abstract_weight=1.0):
    """
    Cleans a raw query and searches the lemmatized Lucene index using BM25F 
    (Fielded BM25) to weight specific fields differently.
    
    Args:
        query (str): The natural language query.
        k (int): Number of documents to return. Default is 5.
        title_weight (float): The multiplier/boost for matches found in the 
                             'title' field. Default is 2.0.
        abstract_weight (float): The multiplier/boost for matches found in the 
                                'abstract' field. Default is 1.0.
        
    Returns:
        list: A list of pyserini.search.lucene.JHit objects containing docid, 
              score, and raw content.
    """
    clean_query = " ".join([
        t.lemma_.lower() for t in nlp(query) 
        if not t.is_stop and not t.is_punct
    ])
    
    field_weights = {
        'title': title_weight,
        'abstract': abstract_weight
    }
    
    hits = searcher.search(clean_query, k=k, fields=field_weights)
    return hits

  # --- Example Usage ---
if __name__ == "__main__":
    raw_query = "covid-19 in kids"
    results = search_trec_covid_bm25f(raw_query, k=10, title_weight=10.0, abstract_weight=1.0)

    print(f"BM25F Results for: {raw_query}")
    for i, hit in enumerate(results):
        print(f'{i+1:2} {hit.docid:15} {hit.score:.5f}')