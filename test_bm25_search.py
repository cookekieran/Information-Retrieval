# test BM25 search

from pyserini.search.lucene import LuceneSearcher

searcher = LuceneSearcher('indexes/trec_covid_bm25_baseline')

query = 'covid-19 in kids'
hits = searcher.search(query)

print(f"Results for query: '{query}'\n")
for i in range(min(3, len(hits))):
    docid = hits[i].docid
    score = hits[i].score
    
    doc = searcher.doc(docid)
    
    print(f"Rank {i+1}: {docid}")
    print(f"Score: {score:.5f}")
    
    print(f"Raw Content: {doc.raw()[:200]}...") 
    print("-" * 30)