from pyserini.dsearch import SimpleDenseSearcher

searcher = SimpleDenseSearcher(
    'dindex-sample-dpr-multi', 'facebook/dpr-question_encoder-multiset-base'
)
hits = searcher.search('what is a lobster roll')

for i in range(0, len(hits)):
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.5f}')