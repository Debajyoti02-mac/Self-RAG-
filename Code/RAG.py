from State_connection import State 
from backend import collection , chunks 
from hybrid_connection import token_corpus

def Hybrid_RAG(state:State) :
    query = state['query']
    result = collection.query(query_texts=[query],n_results=3)
    documents = result['documents'][0]
    distances = result['distances'][0] 
    print(distances)
    
    threshold = 1.6
    dense_chunks = []
    for i , docs in zip(distances,documents):
        if i < threshold:
            dense_chunks.append(docs)
            
    scores = token_corpus.get_scores(query.lower().split())
    def get_index(score,k=10):
        index = list(enumerate(score))
        sorted_index = sorted(index,key=lambda x:x[1], reverse=True)
        return [doc for doc , i in sorted_index[:k]]

    keyword_corpus= get_index(score=scores,k=10)
    chunks_corpus = [chunks[i] for i in keyword_corpus]
    
    rrf_tokens = {}
    for rank , doc in enumerate(dense_chunks):
        rrf_tokens[doc] = rrf_tokens.get(doc,0.0)+1.0/(rank+60)
    for rank , doc in enumerate(chunks_corpus):
        rrf_tokens[doc] = rrf_tokens.get(doc,0.0)+1.0/(rank+60) 
        
    marge = sorted(rrf_tokens.items(),key=lambda x:x[1],reverse=True)
    
    top_docs = [i for i , doc in marge[:5]]
    
    return {'context' : top_docs}
