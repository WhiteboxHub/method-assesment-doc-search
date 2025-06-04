import streamlit as st
from src.agents import find_doc_agent,metadata,qa_agent,rag
# Simulated functions for demo purposes

# def get_documents(query):
#     return [f"Document {i+1} related to '{query}'" for i in range(3)]

# def generate_answer(query, documents):
#     return f"This is a generated answer for the query: '{query}'. Based on documents."

# def get_metadata(query):
#     return {
#         "Query Length": len(query),
#         "Documents Found": 3,
#         "Answer Length": 50
#     }

# App layout
st.title("AI Assistance")

# Stage 1: Input Query
query = st.text_input("Enter your query:")

if query:
    # Stage 2: Show Output Documents
    st.subheader("Documents Retrieved:")
    data = rag.data_retriver(query)

    documents = find_doc_agent.find_docs(data)
    for doc in documents:
        st.write(f"- {doc}")
    
    # Stage 3: Ask to Generate Answer
    if st.button("Generate Answer"):
        answer = qa_agent.QAagent(query, data)
        st.subheader("Generated Answer:")
        st.write(answer)

    if st.button("Generate Meta Data"):
        st.subheader("Generated Meta data:")
        st.write(data)    

            # Stage 4: Show Metadata
        st.subheader("Metadata:")
        answer = data

        for a in answer:
            for key, value in a.items():
                st.write(f"{key}: {value}")
