import ir_datasets
import json
import os
import spacy

dataset = ir_datasets.load("cord19/trec-covid/round1")
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])


os.makedirs('raw_data_json', exist_ok=True)
os.makedirs('cleaned_data_json', exist_ok=True)

with open('raw_data_json/documents.jsonl', 'w') as f:
    for doc in dataset.docs_iter():
        doc_data = {
            "id": doc.doc_id,
            "title": f"{doc.title}",
            "abstract": f"{doc.abstract}",
            "date": f"{doc.date}",
            "doi": f"{doc.doi}",
            "contents": f"{doc.title}. {doc.abstract}"
        }
        f.write(json.dumps(doc_data) + '\n')

print("ETL pipeline complete.")



with open('cleaned_data_json/cleaned_documents.jsonl', 'w', encoding='utf-8') as f:
    for doc in dataset.docs_iter():
        t_lemmas = " ".join([t.lemma_.lower() for t in nlp(doc.title) if not t.is_stop and not t.is_punct])
        a_lemmas = " ".join([t.lemma_.lower() for t in nlp(doc.abstract) if not t.is_stop and not t.is_punct])
        
        doc_data = {
            "id": doc.doc_id,
            "title": t_lemmas,
            "abstract": a_lemmas,
            "contents": f"{t_lemmas} {a_lemmas}"
        }
        f.write(json.dumps(doc_data) + '\n')

print("Cleaned ETL pipeline complete.")