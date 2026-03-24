from collections import defaultdict
import spacy
import numpy as np
from functions import load_index

index, doc_length_dict = load_index()

# index statistics
n_documents = len(doc_length_dict)
doc_length = sum(doc['body'] for doc in doc_length_dict.values())
avgdl = doc_length / n_documents

# pre-processor
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

def calc_bm25(tf, idf, doc_id, field, k=1.5, b=0.75):
    numerator = tf * (k + 1)
    denominator = tf + k * (1 - b + b * (doc_length_dict[doc_id][field] / avgdl))
    bm25_score = idf * (numerator / denominator)  
    return bm25_score    


def run_bm25_search(query, index, n_documents, nlp=nlp, top_n=10):
    """
    Processes a query and returns a ranked list of documents using BM25.
    """
    # 1. Preprocess the query
    doc = nlp(query)
    query_processed_tokens = [token.lemma_.lower() for token in doc if not token.is_stop]
    
    final_scores = defaultdict(lambda: {"body": 0.0, "title": 0.0})

    # 2. Calculate scores per word
    for word in query_processed_tokens:
        if word not in index:
            continue

        # Document Frequency calculations
        n_q_title = sum(counts.get('title', 0) for counts in index[word].values())
        n_q_body = sum(counts.get('body', 0) for counts in index[word].values())

        # IDF calculations
        idf_title = np.log(((n_documents - n_q_title + 0.5) / (n_q_title + 0.5)) + 1)
        idf_body = np.log(((n_documents - n_q_body + 0.5) / (n_q_body + 0.5)) + 1)
        
        print(f"Word: {word} | Title DF: {n_q_title} | Body DF: {n_q_body}")

        for doc_id, tf in index[word].items():
            tf_body = tf.get("body", 0)
            tf_title = tf.get("title", 0)

            # Calculate BM25 for body and title
            body_bm25_score = calc_bm25(tf_body, idf_body, doc_id, "body")
            title_bm25_score = calc_bm25(tf_title, idf_title, doc_id, "title")

            final_scores[doc_id]["body"] += body_bm25_score
            final_scores[doc_id]["title"] += title_bm25_score

    # 3. Sort and Display Results
    print("\n--- Final BM25 Ranking ---\n")
    print(f"{'Doc ID':<12} | {'Body Score':<12} | {'Title Score':<12} | {'Total Score'}")
    print("-" * 60)

    sorted_results = sorted(
        final_scores.items(), 
        key=lambda x: x[1]['body'] + x[1]['title'], 
        reverse=True
    )

    # Print only the top_n results
    for doc_id, scores in sorted_results[:top_n]:
        body = scores['body']
        title = scores['title']
        total = body + title
        print(f"{doc_id:<12} | {body:<12.4f} | {title:<12.4f} | {total:.4f}")

    return sorted_results

results = run_bm25_search("find allow reflecting", index, n_documents, nlp, top_n=5)