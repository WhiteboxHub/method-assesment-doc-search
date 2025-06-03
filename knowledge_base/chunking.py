from nltk.tokenize import sent_tokenize
from langchain.text_splitter import RecursiveCharacterTextSplitter
import nltk

# Download NLTK tokenizer
nltk.download('punkt')

# Recursive splitter
recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=10,
)

def combined_chunker(text, max_words=40):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_word_count = 0

    for sentence in sentences:
        words = sentence.split()
        if current_word_count + len(words) <= max_words:
            current_chunk.append(sentence)
            current_word_count += len(words)
        else:
            joined = ' '.join(current_chunk)
            # If chunk is still too long in characters, split it recursively
            if len(joined) > 100:  # adjust char limit as needed
                sub_chunks = recursive_splitter.split_text(joined)
                chunks.extend(sub_chunks)
            else:
                chunks.append(joined)

            current_chunk = [sentence]
            current_word_count = len(words)

    # Handle the final chunk
    if current_chunk:
        joined = ' '.join(current_chunk)
        if len(joined) > 100:
            chunks.extend(recursive_splitter.split_text(joined))
        else:
            chunks.append(joined)

    return chunks

# # 🔹 Example Text
# text = """Tesla is known for its electric cars. The Model S is a popular model. It offers great range and performance. Tesla also focuses on self-driving technology. Charging stations are expanding rapidly. Customers appreciate the fast acceleration and clean energy design. The company continues to innovate with battery technology and software updates."""

# chunks = combined_chunker(text, max_words=25)

# # 🔸 Display
# print("Combined Sentence + Recursive Chunks:")
# for i, chunk in enumerate(chunks):
#     print(f"Chunk {i+1}: {repr(chunk)}")
