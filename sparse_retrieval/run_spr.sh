#!/bin/bash

#preprocess
python preprocess.py -i ../preprocessed_data -o ./spr_docs

#encode
python -m pyserini.index -collection JsonCollection \
                         -generator DefaultLuceneDocumentGenerator \
                         -threads 1 \
                         -input  spr_docs \
                         -index dindex-docs-spr \
                         -storePositions -storeDocvectors -storeRaw

#search
python main.py \
    --doc_dir dindex-docs-spr \
    --train_dir ../preprocessed_data/train_query \
    --test_dir ../preprocessed_data/test_query \
    --output_dir ../output/

#eval
cd ../
python eval.py data/train_ans.csv output/spr_train.csv