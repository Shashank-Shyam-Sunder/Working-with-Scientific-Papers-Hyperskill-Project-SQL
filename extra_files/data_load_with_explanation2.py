import json  # To parse JSON data from file
import os  # For working with file paths and environment variables

import psycopg2  # PostgreSQL adapter for Python
from datetime import datetime  # To convert string dates into Python date objects
from dotenv import load_dotenv  # To load environment variables from a .env file
from pgvector.psycopg2 import register_vector  # Enables use of the 'vector' data type with psycopg2

# %%
# Construct the full path to the JSON file in the current working directory
json_file = os.path.join(os.getcwd(), 'ml-arxiv-embeddings_1000.json')

# %%
# Load environment variables from a .env file (e.g., credentials)
load_dotenv()
postgre_passcode = os.environ.get('POSTGRE_PASSCODE')  # Safely retrieve PostgreSQL password from environment

# %%
# Establish connection to PostgreSQL database using psycopg2
conn = psycopg2.connect(
    dbname="arxiv_db",  # Name of the database you created in pgAdmin
    user="postgres",  # PostgreSQL username
    password=postgre_passcode,  # Password pulled from .env
    host="localhost",  # Host address (localhost for local database)
    port="5432"  # PostgreSQL default port
)

register_vector(conn)  # Enable support for pgvector extension
cursor = conn.cursor()  # Create cursor for executing SQL commands

# Open and load the JSON dataset
with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)  # Load JSON data as Python list of dictionaries

# Loop through each entry in the dataset and insert it into the database
for entry in data:
    try:
        cursor.execute("""
        INSERT INTO arxiv_papers (
            id, submitter, authors, title, comments, journal_ref, doi, report_no,
            categories, license, abstract, versions, update_date, authors_parsed, embedding
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING  -- Prevent duplicate inserts by skipping if ID already exists
        """, (
            entry.get('id'),  # Unique paper ID
            entry.get('submitter'),  # Name or handle of the submitter
            entry.get('authors'),  # Authors string
            entry.get('title'),  # Paper title
            entry.get('comments'),  # Optional comments
            entry.get('journal-ref'),  # Reference to journal if published
            entry.get('doi'),  # DOI identifier
            entry.get('report-no'),  # Technical report number
            entry.get('categories'),  # Subject classification tags
            entry.get('license'),  # Licensing info (e.g., CC BY-SA)
            entry.get('abstract'),  # Abstract content
            json.dumps(entry.get('versions')),  # Convert list of versions to JSON string
            datetime.strptime(entry.get('update_date'), '%Y-%m-%d').date() if entry.get('update_date') else None,  # Convert date string to date object
            json.dumps(entry.get('authors_parsed')),  # Convert parsed author details to JSON string
            entry.get('embedding')  # Embedding vector (used by pgvector)
        ))
    except Exception as e:
        # Log any errors that occur during insertion
        print(f"Error inserting entry with id {entry.get('id')}: {e}")

# Finalize all insert operations
conn.commit()

# Clean up: close cursor and database connection
cursor.close()
conn.close()

# Indicate completion
print("Data loaded successfully!")
