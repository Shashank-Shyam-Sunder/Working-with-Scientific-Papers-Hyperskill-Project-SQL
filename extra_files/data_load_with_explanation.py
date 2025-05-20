import json  # Import JSON module to load and parse the JSON file
import psycopg2  # PostgreSQL adapter to connect Python with PostgreSQL database
from datetime import datetime  # To parse and handle date formats
from pgvector.psycopg2 import register_vector  # Registers support for the 'vector' data type in pgvector extension

# Establish a connection to the PostgreSQL database using the provided credentials
conn = psycopg2.connect(
    dbname="arxiv_db",  # The database name you created in pgAdmin
    user="postgres",  # Username for PostgreSQL (default is 'postgres')
    password="your_password",  # Password used during PostgreSQL installation
    host="localhost",  # Host server (localhost for local PostgreSQL server)
    port="5432"  # Default port PostgreSQL listens to
)

# Register the pgvector extension for this database connection
register_vector(conn)

# Create a cursor object that lets you interact with the database using SQL commands
cursor = conn.cursor()

# Path to the local JSON file containing data to be inserted into the database
json_file = r"C:\\path\\to\\your\\file.json"

# Load the JSON data into a Python dictionary/list
with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)  # Parses JSON file into Python object (usually a list of dicts)

# Loop through each entry (dictionary) in the loaded data list
for entry in data:
    try:
        # SQL command to insert a new row into the arxiv_papers table
        # If the ID already exists, skip the insert to avoid conflict
        cursor.execute("""
            INSERT INTO arxiv_papers (
                id, submitter, authors, title, comments, journal_ref, doi, report_no,
                categories, license, abstract, versions, update_date, authors_parsed, embedding
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (
            entry.get('id'),  # Paper's unique identifier
            entry.get('submitter'),  # Submitter name or ID
            entry.get('authors'),  # List of authors as string
            entry.get('title'),  # Paper title
            entry.get('comments'),  # Any comments
            entry.get('journal-ref'),  # Journal reference
            entry.get('doi'),  # DOI identifier
            entry.get('report-no'),  # Report number (if any)
            entry.get('categories'),  # Category tags
            entry.get('license'),  # Licensing info
            entry.get('abstract'),  # Abstract text
            json.dumps(entry.get('versions')),  # Convert versions list to JSON string
            datetime.strptime(entry.get('update_date'), '%Y-%m-%d').date() if entry.get('update_date') else None,  # Convert update date to Python date object
            json.dumps(entry.get('authors_parsed')),  # Convert parsed author list to JSON string
            entry.get('embedding')  # List of floats to be stored as pgvector
        ))
    except Exception as e:
        # Print error if insertion fails for a specific record
        print(f"Error inserting entry with id {entry.get('id')}: {e}")

# Commit all the successful insertions to the database
conn.commit()

# Close the cursor object to free database resources
cursor.close()

# Close the database connection
conn.close()

# Print final message once data has been loaded
print("Data loaded successfully!")
