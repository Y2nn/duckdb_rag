# Import the necessary Python package with the functions.
from llama_index.core.chat_engine import CondensePlusContextChatEngine
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.duckdb import DuckDBVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core import StorageContext
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings

from dotenv import find_dotenv, load_dotenv

import duckdb

import os


# Get the OpenAI API KEY
_ = load_dotenv(find_dotenv())
api_key = os.environ.get('OPENAI_API_KEY')  # Buy budget to use a model

# To create the large language model (LLM) client, you just have to provide a model name and API key.
llm = OpenAI(model='gpt-4o', api_key=api_key)

# Create the embed model client using the OpenAI text-embedding-3-small model.
# Note: Providing an OpenAI API key is optional if the environment variable is set with the name “OPENAI_API_KEY”
# on your development environment.
embed_model = OpenAIEmbedding(model='text-embedding-3-small')

# We will make OpenAI LLM and Embedding models global for all LlamaIndex functions to use.
# In short, these models will be set as default.
Settings.llm = llm
Settings.embed_model = embed_model


# Install all the necessary Python packages that will be used to create and retrieve the index.
# llama-index llama-index-vector-stores-duckdb


if __name__ == '__main__':  # Using DuckDB as a vector database
    # load the PDF files from the data folder.
    # These PDF files are tutorials from DataCamp that are saved as PDF files using the browser’s print function.
    # Provide the folder directory to the SimpleDirectoryReader function and load the data.
    documents = SimpleDirectoryReader('data').load_data()

    # Create the vector store called “blog” using an existing database called “datacamp.duckdb.”
    vector_store = DuckDBVectorStore(
        database_name='datacamp.duckdb',
        table_name='blog',
        persist_dir='./',
        embed_dim=1536
    )

    # Convert the PDF's data into embeddings and store them in the vector store.
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

    # print(storage_context)

    """To check if our vector store was successfully created"""

    # Connect the database using the DuckDB Python API
    con = duckdb.connect('datacamp.duckdb')

    # Run the SQL query to display all the tables in the database.
    print(con.execute('SHOW ALL TABLES').df())

    """Creating a simple RAG application"""

    # Convert the index into the query engine.
    query_engine = index.as_query_engine()

    # To test the RAG query engine, we will ask the question about the tutorial
    # Search the vector database for similar documents and use the additional context to generate the response.
    response = query_engine.query("Who wrote 'GitHub Actions and MakeFile: A Hands-on Introduction'?")
    print(f'<b>{response}</b>')

    """Creating a RAG chatbot with memory that uses the conversation history to generate the response"""

    # Create a chat memory buffer.
    memory = ChatMemoryBuffer.from_defaults(token_limit=3900)

    # Create a chat engine with memory, LLM, and vector store retriever.
    chat_engine = CondensePlusContextChatEngine.from_defaults(
        index.as_retriever(),
        memory=memory,
        llm=llm
    )

    # Ask the chat engine how to fine-tune the Llama 3 model, it used the vector store to give a highly accurate answer.
    response = chat_engine.chat(
        "What is the easiest way of finetuning the Llama 3 model? Please provide step-by-step instructions."
    )
    print(response.response)

    # Check if the memory buffer is working correctly, ask a follow-up question.
    # The chat engine remembered the previous conversation and responded accordingly.
    response = chat_engine.chat(
        "Could you please provide more details about the Post Fine-Tuning Steps?"
    )
    print(response.response)
