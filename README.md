# document-retrieval
NTU-2021Fall-IR

#### In this project, we utilize the [pyserini toolkit](https://github.com/castorini/pyserini)

File Structure
---
```
document_retrieval
     ├──sparse_retrieval
     │    └── ...
     ├──dense_retrieval
     │    └── ...
     ├── eval.py #evaluation on train query
     ├── preprocess_doc.py #overall preprocess
     └── run_preprocess.sh #script to run preprocess_doc.py
 
```

Environment Setup
---
create a conda environment
```
$ conda create -n pyserini python=3.7
$ conda activate pyserini
```
packages
```
$ conda install -c conda-forge openjdk=11
$ conda install -c conda-forge pyjnius 
$ conda install faiss-cpu -c pytorch
$ conda install pytorch torchvision torchaudio -c pytorch
$ pip install pyserini beautifulsoup4 lxml
```

Data Preprocess 
---
#### step1. download the data
place `./data` int the root of this repository, the structure of `./data` should be as follows: 
```
document_retrieval
     ├── ...
     └── data
          ├── docs
          ├── train_query
          └── test_query
```
#### step2. preprocess the data (extract xml file)
run this command to extract the the content from the xml files (this step may take a few minutes) \
in our baseline, we use  "abstract" for query, and "body" for document

```
$ bash run_preprocess.sh
```
the default input directory is `./data` and the output directory is `./preprocessed_data` \
(the names and paths can be modified inside `run_preprocess.sh`)

Run Retrieval 
---

[Sparse Passage Retrieval](https://github.com/castorini/pyserini#how-do-i-index-and-search-my-own-documents) (lucene-bm25) ⟶ our baseline
```
$ cd sparse_retrieval
$ bash run_spr.sh
```
`run_spr.sh` includes converting docs/queries to jsonl format, indexing, searching and evaluation.

[Dense Passage Retrieval](https://github.com/castorini/pyserini/blob/master/docs/experiments-dpr.md) (facebookresearch DPR)
```
$ cd dense_retrieval
$ bash run_dpr.sh
```
`run_dpr.sh` includes converting docs/queries to jsonl format, indexing, searching and evaluation.


Results
---
(experiment results can be updated here)

| Model       | mapk@50     | approx run time |
| ----------- | ----------- | --------------- |
| SPR (body & summary, bm25(2.45, 0.5), rm3(50, 50, 0.7)) | 0.2111 | 10 min |
| SPR (body & summary, bm25(4.46, 0.82), rm3(100, 100, 0.7)) | 0.2046 | 10 min |
