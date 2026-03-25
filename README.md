# Information Retrieval Project: TREC-COVID Search

This project implements a modular Information Retrieval pipeline using **Pyserini (Anserini/Lucene)** and **BM25**.

---

## Project Structure

To keep the project organized, we use the following directory structure:

```text
project/
├── indexing/           # Scripts to build the Lucene index
│   └── ETL.py
│   └── build_index.ps1
├── retrieval/          # Search algorithms (BM25, BM25F, RM3)
│   └── bm25.py
│   └── bm25f.py
├── reranking/          
│   └── colbert.py
├── fusion/         
│   └── rrf.py
├── evaluation/          
│   └── evaluate.py
├── interface/         
│   └── app.py   
├── indexes/            # Lucene index files (Not in Git)
│   └── trec_covid_lemmatized/
├── main.py             # Main entry point to run searches
└── requirements.txt    # Python dependencies
```

---

## Setup & Installation

### 1. Java Runtime (Critical)

Pyserini requires Java 21. If you are using Conda, install the correct OpenJDK version:

```bash
conda activate your_env_name
conda install -c conda-forge openjdk=21
```

---

### 2. Python Dependencies

Install the required libraries and the spaCy language model:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

---

### 3. Data & Indexing

The Lucene index is not included in Git due to its size.

If you want to build the index from scratch, follow these steps. This process lemmatizes the raw data and then builds a Lucene index with stored vectors for BM25.

From the project root, run the PowerShell script:

```powershell
./build_index.ps1

**OR**

- Ensure you have the `trec_covid_lemmatized` folder  
- Place it inside an `indexes/` directory at the root of this project  

---

## How to Run

To run a search from the project root, execute:

```bash
python main.py
```

---

## Note on Warnings

When running the search, you may see the following warning:

```
WARNING: Using incubator modules: jdk.incubator.vector
```

**Why**
- This is a performance feature in Java 21 used by Apache Lucene.

**Action**
- This warning can be safely ignored. The search will still execute correctly.