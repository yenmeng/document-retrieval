#!/bin/bash

# #preprocess
# python preprocess.py -i ../preprocessed_data/doc -o ./dpr_docs
#
# #encode
# python -m pyserini.encode input   --corpus  dpr_docs \
#                           output  --embeddings dindex-docs-dpr-multi --to-faiss \
#                           encoder --encoder facebook/dpr-ctx_encoder-multiset-base --batch-size 32 \
#
# #search
# python main.py \
#     --train_dir ../preprocessed_data/train_query \
#     --test_dir ../preprocessed_data/test_query \
#     --output_csv ../output/dpr.csv

#eval
cd ../
python eval.py data/train_ans.csv output/dpr.csv
