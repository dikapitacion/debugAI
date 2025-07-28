import os
from dotenv import load_dotenv

# Import the core LangChain component for Gemini Embeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Imports for the full example
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter

# --- Step 1: Load the API Key ---
# Load environment variables from .env file
load_dotenv()

# Check if the API key is loaded correctly
if "GOOGLE_API_KEY" not in os.environ:
    raise ValueError("Google API Key not found. Please set it in your .env file.")

print("API Key loaded successfully.")

# --- Step 2: Initialize the Gemini Embedding Model ---
# The model "models/embedding-001" is currently the recommended model for text embeddings.
try:
    gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    print("Gemini Embeddings model initialized successfully.")
except Exception as e:
    print(f"Error initializing the embedding model: {e}")
    exit()


# --- PRACTICAL USAGE: INTEGRATION WITH A VECTOR STORE (FOR YOUR LOGAI PROJECT) ---
print("\n--- Practical Usage: Building a Vector Store with Log Data ---")

# 1. Sample log data (in your project, this will come from your log files)
log_data = [
    "2025-07-27T10:00:15Z INFO: User 'alex' successfully logged in.",
    "2025-07-27T10:01:05Z ERROR: Authentication failed for user 'admin'. Invalid password attempt.",
    "2025-07-27T10:02:30Z DEBUG: Database connection pool size: 5.",
    "2025-07-27T10:03:45Z WARN: High CPU usage detected on server-web-01.",
    "2025-07-27T10:05:00Z ERROR: Payment gateway timeout for transaction id 98765.",
]

# In a real scenario, you'd use a more sophisticated splitter like RecursiveCharacterTextSplitter
text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=0)
documents = text_splitter.create_documents(log_data)

print(f"\nSplit {len(log_data)} log entries into {len(documents)} documents.")

# 2. Create and populate the vector store using the Gemini embeddings
# This single command does all the heavy lifting:
# - It iterates through each document.
# - It uses the `gemini_embeddings` model to create a vector for each one.
# - It stores the documents and their corresponding vectors in FAISS.
print("\nCreating vector store using Gemini embeddings... (This may take a moment)")
vector_store = FAISS.from_documents(documents, gemini_embeddings)
print("Vector store created successfully.")

# 3. Test the vector store by asking a question
print("\nTesting the vector store with a similarity search...")
question = "Were there any auth errors?"
retrieved_docs = vector_store.similarity_search(question, k=2)

print(f"\nTop {len(retrieved_docs)} most relevant logs for the question: '{question}'")
for doc in retrieved_docs:
    print(f"  - {doc.page_content}")