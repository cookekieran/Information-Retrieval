Write-Host "--- Step 1: Running ETL and Lemmatization ---"
python ETL.py

Write-Host "--- Building Lucene Index ---"
python -m pyserini.index.lucene `
  --collection JsonCollection `
  --input data_cleaned `
  --index indexes/trec_covid_lemmatized `
  --generator DefaultLuceneDocumentGenerator `
  --threads 4 `
  --fields title abstract `
  --analyzer whitespace `
  --storePositions --storeDocvectors --storeRaw 

Write-Host "Documents have been indexed."