# document-retrieval
NTU-2021Fall-IR

#### In this project, we utilize the [pyserini toolkit](https://github.com/castorini/pyserini)

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
$ pip install pyserini
```

Data Preprocess 
---
#### step1. download the data
place `./data` int the root of this repository, the structure of `./data` should be as follows:
```
.
└── data
    ├── docs
    ├── train_query
    └── test_query
```
#### step2. preprocess the data (extract xml file)

Run Retrieval 
---

Dense Retrieval 
```
$ bash run_dpr.sh
```
Sparse Retrieval (lucene-bm25)
```
$ bash run_spr.sh
```
