import argparse
from pathlib import Path
from bs4 import BeautifulSoup as bs
from tqdm.auto import tqdm
import re

def get_args():
    
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--in-dir')
    parser.add_argument('-o', '--out-dir')
    parser.add_argument('-t', '--type', choices={'document', 'query'})

    return parser.parse_args()

def preprocess_doc(file):
    d = bs(open(file), 'lxml')
    
    s = ' '.join([p.get_text() for p in d.find('body').findAll('p')])
    s = s.replace('\n', ' ')
    s = s.replace('\t', '')
    s = s.strip()

    s = s.replace('\n', ' ')
    s = s.replace('\t', '')
    s = s.strip()
    
    return s

def preprocess_query(file):

    d = bs(open(file), 'lxml')
    s = ' '.join([d.find('summary').get_text()])

    return s
    
def main():
    args = get_args()

    preprocesser = preprocess_doc if args.type == 'document' else preprocess_query

    for file in tqdm(list(Path(args.in_dir).glob('*'))):
    
        result = preprocesser(file)

        with open(Path(args.out_dir)/file.name, 'w') as f:
            print(result, file=f)


if __name__ == '__main__':
    main()