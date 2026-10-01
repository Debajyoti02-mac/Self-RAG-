from Graph import graph

question = "What is the main topic discussed in the document?"

for chunks in graph.stream({
    "query": question
}):
    print(chunks)