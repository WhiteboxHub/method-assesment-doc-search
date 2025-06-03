import streamlit as st

# Simulated functions for demo purposes
def get_documents(query):
    return [f"Document {i+1} related to '{query}'" for i in range(3)]

def generate_answer(query, documents):
    return f"This is a generated answer for the query: '{query}'. Based on documents."

def get_metadata(query):
    return {
        "Query Length": len(query),
        "Documents Found": 3,
        "Answer Length": 50
    }

# App layout
st.title("AI Assistance")

# Stage 1: Input Query
query = st.text_input("Enter your query:")

if query:
    # Stage 2: Show Output Documents
    st.subheader("Documents Retrieved:")
    documents = get_documents(query)
    for doc in documents:
        st.write(f"- {doc}")
    
    # Stage 3: Ask to Generate Answer
    if st.button("Generate Answer"):
        answer = generate_answer(query, documents)
        st.subheader("Generated Answer:")
        st.write(answer)

    if st.button("Generate Meta Data"):
        answer = generate_answer(query, documents)
        st.subheader("Generated Meta data:")
        st.write(answer)    

            # Stage 4: Show Metadata
        st.subheader("Metadata:")
        metadata = get_metadata(query)
        for key, value in metadata.items():
            st.write(f"{key}: {value}")
