#!/bin/bash

in_data_root=data
out_data_root=preprocessed_data

doc_dirs=('doc')
query_dirs=('test_query' 'train_query')

for dir in ${doc_dirs[@]}; do

    mkdir -p $out_data_root/$dir

    python preprocess_doc.py \
        -i $in_data_root/$dir \
        -o $out_data_root/$dir \
        -t document
done

for dir in ${query_dirs[@]}; do

    mkdir -p $out_data_root/$dir 

    python preprocess_doc.py \
        -i $in_data_root/$dir \
        -o $out_data_root/$dir \
        -t query
done
