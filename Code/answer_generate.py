from State_connection import State 
from LLM import LLM 

def LLM_connection(state:State):
    prompt = f""" 
    context : {state['context']}
    question : {state['query']}
    """
    response = LLM.invoke(prompt)
    return {'answer':response.content}