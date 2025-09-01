# DuckDB RAG (Retrieval Augmented Generation)

## What is DuckDB ?
DuckDB is a modern, high-performance, in-memory analytical database management system (DBMS) designed to support complex analytical queries. It is a relational DBMS that supports the Structured Query Language (SQL). 

DuckDB combines the simplicity and ease of use of SQLite with the high-performance capabilities required for analytical workloads, making it an excellent choice.

## Setting up 
Install all the necessary Python packages that will be used to create and retrieve the index. 

```Python
pip install duckdb
pip install llama-index
pip install duckdb --upgrade
pip install llama-index-vector-stores-duckdb
```

## Building a RAG Application with DuckDB
- Using DuckDB as a vector database.
- Creating a simple RAG application.
- Creating a RAG chatbot with memory.

## Building a DuckDB SQL Query Engine Using an LLM
- Loading the DuckDB database
- Building the SQL query engine