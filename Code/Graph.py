from langgraph.graph import StateGraph, START, END 
from LLM import LLM 
from answer_generate import LLM_connection 
from State_connection import State 
from RAG import Hybrid_RAG 
from grader import grader ,check_grounded

 

builder = StateGraph(State)

builder.add_node("retrieval", Hybrid_RAG)
builder.add_node("llm", LLM_connection)
builder.add_node("grader", grader)

builder.add_edge(START, "retrieval")
builder.add_edge("retrieval", "llm")
builder.add_edge("llm", "grader")

builder.add_conditional_edges(
    "grader",
    check_grounded,
    {
        "end": END,
        "retry": "retrieval"
    }
)

graph = builder.compile()