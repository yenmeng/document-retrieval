import os
import argparse
from pyserini.dsearch import SimpleDenseSearcher, TctColBertQueryEncoder
from pyserini.search import SimpleSearcher, SimpleFusionSearcher
from pyserini.hsearch import HybridSearcher
from pyserini.fusion import FusionMethod
from pyserini.search.reranker import ClassifierType, PseudoRelevanceClassifierReranker
from pyserini.analysis import JDefaultEnglishAnalyzer
from tqdm import tqdm

def get_args():
    parser = argparse.ArgumentParser(description='IR Final Project^^')

    parser.add_argument('--doc_dir',    type=str, default='dindex-docs-spr')
    parser.add_argument('--train_dir',  type=str, default='../preprocessed_data/train_query')
    parser.add_argument('--test_dir',   type=str, default='../preprocessed_data/test_query')
    
    parser.add_argument('--output_dir', type=str, default='../output')
    
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
    test_querys, test_names = load_data(args.test_dir)
    
    # params = [(2.45, 0.5), (2.56, 0.59), (4.46, 0.82)]
    # dsearcher = SimpleDenseSearcher(
    # '/home/yenmeng/workdir/IR-Final/pyserini/DPR/dindex-docs-dpr-multi', 'facebook/dpr-question_encoder-multiset-base'
    # )
    # ssearcher = SimpleSearcher(args.doc_dir)
    # ssearcher.set_bm25(2.45, 0.5)
    # ssearcher.set_rm3(fb_terms=50, fb_docs=50, original_query_weight=0.7, rm3_filter_terms=False)
    
    # searcher = HybridSearcher(dsearcher, ssearcher)
    
    searcher = SimpleSearcher(args.doc_dir)
    searcher.set_bm25(2.45, 0.5)
    searcher.set_rm3(fb_terms=50, fb_docs=50, original_query_weight=0.7)
       
    output_train = []
    print('====== retrieving train ======')
    for i, query in enumerate(tqdm(train_querys)):
        # hits = searcher.search(query, k0=50, k=50, alpha=0.1, normalization=True, weight_on_dense=True)
        hits = searcher.search(query, k=50)
        
        '''for j in range(50):
            print(f'{j+1:2} {hits[j].docid:7} {hits[j].score:.5f}')'''
                
        top_k_idx = [hits[k].docid for k in range(50)]
        output_train.append((train_names[i], ' '.join(top_k_idx)))
        
    output_test = []
    print('====== retrieving test ======')   
    for i, query in enumerate(tqdm(test_querys)):
        # hits = searcher.search(query, k0=50, k=50, alpha=0.1, normalization=True, weight_on_dense=True)
        hits = searcher.search(query, k=50)
                               
        '''for j in range(50):
            print(f'{j+1:2} {hits[j].docid:7} {hits[j].score:.5f}')'''
        
        top_k_idx = [hits[k].docid for k in range(50)]
        output_test.append((test_names[i], ' '.join(top_k_idx)))
        
    return output_train, output_test

def write_csv(args, output, mode):
    os.makedirs(args.output_dir, exist_ok=True)
    output_csv = os.path.join(args.output_dir, f'spr_{mode}.csv')
    with open(output_csv, 'w') as f:
        f.write('topic,doc\n')
        for item in sorted(output, key = lambda tup: int(tup[0])):
            f.write(f'{item[0]},{item[1]}\n')

def main():
    args = get_args()
    output_train, output_test = retrieve(args)
    write_csv(args, output_train, 'train')
    write_csv(args, output_test, 'test')
    
if __name__ == '__main__':
    main()