import os
import argparse
from pyserini.search import SimpleSearcher
from pyserini.dsearch import SimpleDenseSearcher, TctColBertQueryEncoder, DprQueryEncoder
from pyserini.hsearch import HybridSearcher
from tqdm import tqdm

def get_args():
    parser = argparse.ArgumentParser(description='IR Final Project^^')

    parser.add_argument('--doc_dir',    type=str, default='dindex-docs-dpr-multi')
    parser.add_argument('--train_dir',  type=str, default='../preprocessed_data/train_query')
    parser.add_argument('--test_dir',   type=str, default='../preprocessed_data/test_query')
    
    parser.add_argument('--output_csv', type=str, default='../output/dpr.csv')
    
    parser.add_argument('-bs', '--batch_size', type=int, default=32)

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
    
def retrieve(args):
    train_querys, train_names = load_data(args.train_dir)

    searcher = SimpleDenseSearcher(
        args.doc_dir, 'facebook/dpr-question_encoder-multiset-base'
    )
    
    output = []
    for i, query in tqdm(enumerate(train_querys)):
        hits = searcher.search(query, k=50)

        for j in range(50):
            print(f'{j+1:2} {hits[j].docid:7} {hits[j].score:.5f}')
        
        top_k_idx = [hits[k].docid for k in range(50)]
        output.append((train_names[i], ' '.join(top_k_idx)))
        
    return output

def write_csv(args, output):
    os.makedirs(os.path.dirname(args.output_csv), exist_ok=True)
    with open(args.output_csv, 'w') as f:
        f.write('topic,doc\n')
        for item in output:
            f.write(f'{item[0]},{item[1]}\n')

def main():
    args = get_args()
    output = retrieve(args)
    write_csv(args, output)
    
if __name__ == '__main__':
    main()