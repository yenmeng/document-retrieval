import os
import argparse
from pathlib import Path
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
import json

def get_args():
    
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--in_dir', type=str, default='../preprocessed_data/doc')
    parser.add_argument('-o', '--out_dir', type=str, default='dpr_docs')

    return parser.parse_args()

def preprocess(data_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    outfile = 'docs.jsonl'
    filenames = sorted(os.listdir(data_dir))
    with open(os.path.join(out_dir, outfile), 'w') as fout:
        for filename in tqdm(filenames):
            with open(os.path.join(data_dir, filename), 'r') as fin:
                obj = { 
                        "id": int(filename),
                        "contents": fin.read() 
                }
                json.dump(obj, fout)
                fout.write('\n')
               
def main():
    args = get_args()
    preprocess(args.in_dir, args.out_dir)

    


if __name__ == '__main__':
    main()