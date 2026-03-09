import ir_datasets
import json
import os

dataset = ir_datasets.load("cord19/trec-covid/round1")


os.makedirs('data_json', exist_ok=True)

with open('data_json/documents.jsonl', 'w') as f:
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