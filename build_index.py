index = {} # word: {doc_id: {"title": frequency, "body": frequency}}
doc_length_dict = {} # doc_id: {"title": len, "body": len}

import ir_datasets
import spacy
from tqdm import tqdm
import pickle

dataset = ir_datasets.load("cord19/trec-covid/round1")

nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

def update_counts(spacy_doc, field, doc_id):
    doc_length_dict[doc_id][field] = len(spacy_doc)
    
    for token in spacy_doc:
        if not token.is_stop and (token.is_alpha or token.text in ["-"]):
            word = token.lemma_.lower()
            
            if word not in index:
                index[word] = {}
            if doc_id not in index[word]:
                index[word][doc_id] = {"title": 0, "body": 0}
            
            index[word][doc_id][field] += 1


docs = list(dataset.docs_iter())
titles = [d.title for d in docs]
abstracts = [d.abstract for d in docs]

print("Processing documents...")

n = 0
for doc_obj, title_doc, abs_doc in tqdm(zip(docs, nlp.pipe(titles), nlp.pipe(abstracts)), total=len(docs)):
    n += 1
    if n > 5:
        break
    doc_id = doc_obj.doc_id
    
    doc_length_dict[doc_id] = {"title": 0, "body": 0}
    
    update_counts(title_doc, "title", doc_id)
    update_counts(abs_doc, "body", doc_id)

print(f"Index built with {len(index)} unique terms.")


data_to_save = {
    "index": index,
    "doc_length_dict": doc_length_dict
}

print("Saving index to disk...")
with open('inverted_index.pkl', 'wb') as f:
    pickle.dump(data_to_save, f, protocol=pickle.HIGHEST_PROTOCOL)

print("Done! File saved as inverted_index.pkl")