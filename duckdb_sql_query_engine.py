# Import the necessary Python package with the functions.
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.llms.openai import OpenAI
from llama_index.core import SQLDatabase

from dotenv import find_dotenv, load_dotenv

from sqlalchemy import create_engine

import os

# duckdb-engine

# Get the OpenAI API KEY
_ = load_dotenv(find_dotenv())
api_key = os.environ.get('OPENAI_API_KEY')  # Buy budget to use a model

# To create the large language model (LLM) client, you just have to provide a model name and API key.
llm = OpenAI(model='gpt-4o', api_key=api_key)


if __name__ == '__main__':
    # Load the DuckDB database using the create_engine function
    engine = create_engine('duckdb:///datacamp.duckdb')

    # Run a simple SQL query to check whether it is successfully loaded.
    with engine.connect() as connection:
        # Run the duckdb_tutorial.py file to get the table bank in the datacamp.duckdb database if needed
        cursor = connection.exec_driver_sql('SELECT * FROM bank LIMIT 3')
        print(cursor.fetchall())

        # Create a database Tool using the SQLDatabase function
        sql_database = SQLDatabase(engine, include_tables=['bank'])

        # Create the SQL query engine using the NLSQLTableQueryEngine function
        # by providing it with the LlamaIndex SQL database object.
        query_engine = NLSQLTableQueryEngine(sql_database)

        # Ask the question from the query engine about the “bank” table in the natural language.
        response = query_engine.query('Which is the longest running campaign?')
        # In response, we will get the answer to your query in natural languages. This is awesome, don't you think?
        print(response.response)

        # Let's ask a complex question.
        response = query_engine.query("Which type of job has the most housing loan?")
        # The answer is precise, with additional information.
        print(response.response)

        # To check what is going on on the back end, we will print the metadata.
        # GPT-4o generates the SQL query, runs the query to get the result, and uses the result to generate the response.
        print(response.metadata)

        # Close the engine when you are done with the project.
        engine.close()