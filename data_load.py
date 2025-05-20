import json
import os

import psycopg2
from datetime import datetime
from dotenv import load_dotenv
from pgvector.psycopg2 import register_vector
import os
# %%
# Do not forget here to the PATH to the json file(dataset)
json_file = os.path.join(os.getcwd(), 'ml-arxiv-embeddings_1000.json')
# json_file = r"PATH TO FILE"
# # Do not forget here to add your database credentials
load_dotenv()
postgre_passcode = os.environ.get('POSTGRE_PASSCODE')
# print(postgre_passcode) # for debudding only


# %%
conn = psycopg2.connect(
    dbname="arxiv_db",
    user="postgres",
    password=postgre_passcode,
    host="localhost",
    port="5432"
)
register_vector(conn)
cursor = conn.cursor()

with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

for entry in data:
    try:
        cursor.execute("""
        INSERT INTO arxiv_papers (
            id, submitter, authors, title, comments, journal_ref, doi, report_no,
            categories, license, abstract, versions, update_date, authors_parsed, embedding
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
        """, (
            entry.get('id'),
            entry.get('submitter'),
            entry.get('authors'),
            entry.get('title'),
            entry.get('comments'),
            entry.get('journal-ref'),
            entry.get('doi'),
            entry.get('report-no'),
            entry.get('categories'),
            entry.get('license'),
            entry.get('abstract'),
            json.dumps(entry.get('versions')),  # Convert to JSON string
            datetime.strptime(entry.get('update_date'), '%Y-%m-%d').date() if entry.get('update_date') else None,
            json.dumps(entry.get('authors_parsed')),  # Convert to JSON string
            entry.get('embedding')  # Use vector format directly
        ))
    except Exception as e:
        print(f"Error inserting entry with id {entry.get('id')}: {e}")

conn.commit()
cursor.close()
conn.close()

print("Data loaded successfully!")
