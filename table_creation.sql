-- drop table if exists arxiv_papers;

CREATE TABLE arxiv_papers (
    id VARCHAR(255) PRIMARY KEY,
    submitter VARCHAR(255),
    authors TEXT,
    title TEXT,
    comments TEXT,
    journal_ref VARCHAR(300),
    doi TEXT,
    report_no TEXT,
    categories TEXT,
    license TEXT,
    abstract TEXT,
    versions JSON, 
    update_date DATE,
    authors_parsed JSON, 
    embedding vector(1536)
);