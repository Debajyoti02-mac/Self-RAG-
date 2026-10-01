from LLM import LLM 
from State_connection import State 

# Output structure 
from pydantic import BaseModel , Field 
class Grade(BaseModel):
    grounded : bool = Field(description="Whether the answer is supported by the context")
    
grader_llm = LLM.with_structured_output(
    Grade,
    method="json_schema"
)

def grader(state:State):
    prompt = f"""
    Check whether the answer is supported by the provided context.

    Context:
    {state['context']}

    Question:
    {state['query']}

    Answer:
    {state['answer']}

    Return only:
    YES
    or
    NO
    """
    
    response = grader_llm.invoke(prompt)
    
    # result = response.content.strip().upper()
    
    return {
        "grounded":response.grounded
    }
    
def check_grounded(state:State):
    if state['grounded']:return "end"
    return "retry"
