import os
import argparse
from pathlib import Path
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
import json
import pandas as pd

def get_args():
    
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--in_dir', type=str, default='../../preprocessed_data_ab')
    parser.add_argument('-o', '--out_dir', type=str, default='spr_docs')

    return parser.parse_args()

def load_data(data_dir, return_filenames=True):
    docs = []

    filenames = sorted(os.listdir(data_dir))
    for filename in filenames:
        with open(os.path.join(data_dir, filename), 'r') as f:
            docs.append(f.read())

    if return_filenames:
        return docs, filenames
    else:
        return docs

def preprocess_docs(data_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    outfile = os.path.join(out_dir, 'docs.jsonl')
    filenames = sorted(os.listdir(os.path.join(data_dir, 'doc')))
    with open(outfile, 'w') as fout:
        for filename in tqdm(filenames):
            with open(os.path.join(data_dir, 'doc', filename), 'r') as fin:
                obj = { 
                        "id": int(filename),
                        "contents": fin.read() 
                }
                json.dump(obj, fout)
                fout.write('\n')

def preprocess_queries(data_dir, out_dir):
     train_queries, train_names = load_data(os.path.join(data_dir, 'train_query'))
     test_queries, test_names = load_data(os.path.join(data_dir, 'test_query'))
     
     train_outfile = 'train_queries.tsv'
     test_outfile = 'test_queries.tsv'
     
     train_df = pd.DataFrame(list(zip(train_names, train_queries)))
     test_df = pd.DataFrame(list(zip(test_names, test_queries)))
     
     train_df.to_csv(train_outfile, sep='\t', index=False)
     test_df.to_csv(test_outfile, sep='\t', index=False)
    
               
def main():
    args = get_args()
    preprocess_docs(args.in_dir, args.out_dir)
    preprocess_queries(args.in_dir, args.out_dir)



if __name__ == '__main__':
    main()