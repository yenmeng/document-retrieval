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
    
    # bm25 args
    parser.add_argument('--k1', type=float, default=2.45)
    parser.add_argument('--b', type=float, default=0.5)
    
    #rm3 args
    parser.add_argument('--use_rm3', action='store_true', default=True)
    parser.add_argument('--fb_terms', type=int, default=50, help='RM3 parameter for number of expansion terms.')
    parser.add_argument('--fb_docs', type=int, default=50, help='RM3 parameter for number of expansion documents.')
    parser.add_argument('--original_query_weight', type=float, default=0.7, help='RM3 parameter for weight to assign to the original query.')

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
    
    searcher = SimpleSearcher(args.doc_dir)
    searcher.set_bm25(k1=args.k1, b=args.b)
    if args.use_rm3:
        searcher.set_rm3(fb_terms=args.fb_terms, fb_docs=args.fb_docs, original_query_weight=args.original_query_weight)
       
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