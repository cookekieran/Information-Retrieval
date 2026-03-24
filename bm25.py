import spacy
from pyserini.search.lucene import LuceneSearcher

searcher = LuceneSearcher('indexes/trec_covid_lemmatized')
searcher.set_bm25(k1=0.9, b=0.4)
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

def search_trec_covid(query, k=5):
    """
    Cleans a raw query and searches the lemmatized Lucene index.
    
    Args:
        query (str): The natural language query.
        k (int): Number of documents to return.
        
    Returns:
        list: A list of pyserini.search.lucene.JHit objects.
    """
    clean_query = " ".join([
        t.lemma_.lower() for t in nlp(query) 
        if not t.is_stop and not t.is_punct
    ])
    
    hits = searcher.search(clean_query, k=k)
    return hits

raw_query = "covid-19 in kids"
results = search_trec_covid(raw_query, k=10)

print(f"Top results for: {raw_query}")
for i, hit in enumerate(results):
    print(f'{i+1:2} {hit.docid:15} {hit.score:.5f}')