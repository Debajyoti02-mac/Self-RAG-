from backend import chunks
from rank_bm25 import BM25Okapi 
tokens = [i.lower().split() for i in chunks]
token_corpus = BM25Okapi(tokens)