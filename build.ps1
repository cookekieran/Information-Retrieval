Write-Host "Starting data preparation..."
python ETL.py

Write-Host "Starting indexing process..."
python -m pyserini.index -collection JsonCollection -generator DefaultLuceneDocumentGenerator -threads 1 -input data_json -index indexes/trec_covid_bm25_baseline -storeRaw

Write-Host "Documents have been indexed."