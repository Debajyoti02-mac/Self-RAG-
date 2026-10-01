from typing import TypedDict

class State(TypedDict):
    query: str
    context: str
    answer: str
    needs_retrieval: bool
    grounded: bool