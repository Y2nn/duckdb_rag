# Import the necessary Python package with the functions.
import duckdb


if __name__ == '__main__':
    # To create the persistent database, you just have to use the connect function and provide it with the database name
    # It will create a database base file in your local directory.
    con = duckdb.connect('datacamp.duckdb')

    # To load the CSV file, you have to create a Table first using SQL
    # Then use the read_csv() function within the SQL script to load the file.
    con.execute("""
        CREATE TABLE IF NOT EXISTS bank AS
        SELECT * FROM read_csv('data/bank-marketing.csv')
    """)

    # Validate our table by executing the SQL script that shows all of the tables within the database
    # Use the fetchdf function to display the result as a pandas DataFrame.
    print(con.execute("SHOW ALL TABLES").fetchdf())

    # Run a beginner-level query to analyze the data and display the result as a DataFrame.
    print(con.execute("SELECT * FROM bank WHERE duration < 100 LIMIT 5").fetchdf())

    rel = con.table("bank")
    print(rel.columns)


    """Load the csv file and apply functions"""
    # Load a CSV file to create the DuckDB relation.
    bank_duck = duckdb.read_csv('data/bank-marketing.csv', sep=',')

    # Chain the filter and limit functions.
    print(bank_duck.filter("duration < 100").limit(3))
    print(bank_duck.filter("duration < 100").limit(3).df())

    # Run multiple functions to analyze the data (project function: select columns from the table).
    print(bank_duck.filter("duration < 100").project("job,education,loan"))


    """Query to the database"""
    # Run the SQL query to find out the job titles of clients over the age of 30,
    # count the number of clients contacted for each job, and calculate the average duration of the campaign.
    res = duckdb.query("""
        SELECT 
            job,
            COUNT(*) AS total_clients_contacted,
            AVG(duration) AS avg_campaign_duration,
        FROM 
            'data/bank-marketing.csv'
        WHERE
            age > 30
        GROUP BY
            job
        ORDER BY
            total_clients_contacted DESC;
    """)
    print(res.df())
    print(res)


    """"Close the connection"""
    # Close the connection to the database and release any resources associated with that connection,
    # preventing potential memory and file handle leaks.
    con.close()