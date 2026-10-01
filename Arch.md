
                 ┌─────────────────┐
                 │   User Query    │
                 └────────┬────────┘
                          ↓
                 ┌─────────────────┐
                 │ Retrieval Needed?│
                 └───────┬─────────┘
                     Yes │ No
                         ↓
                 ┌─────────────────┐
                 │    Retriever    │
                 └────────┬────────┘
                          ↓
                 ┌─────────────────┐
                 │    Generator    │
                 └────────┬────────┘
                          ↓
                 ┌─────────────────┐
                 │ Answer Grounded?│
                 └───────┬─────────┘
                    No   │   Yes
                     ↓   │
              ┌──────────┘
              │
              ↓
       Retrieve again /
       improve query
              │
              └──────→ Generator

                          ↓
                   Final Answer
