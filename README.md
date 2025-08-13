# ArXiv Scientific Papers Database with Vector Embeddings

A PostgreSQL database project for storing and querying ArXiv scientific papers with vector embeddings using pgvector extension. This project enables semantic search capabilities on scientific literature.

## 🎯 Project Overview

This project loads ArXiv paper metadata along with their vector embeddings into a PostgreSQL database. The embeddings enable semantic similarity searches across scientific papers, making it useful for research discovery and literature analysis.

## 📋 Features

- **Vector Database**: Uses PostgreSQL with pgvector extension for storing 1536-dimensional embeddings
- **ArXiv Integration**: Processes ArXiv paper metadata including titles, abstracts, authors, and categories
- **Semantic Search Ready**: Vector embeddings enable similarity-based paper recommendations
- **Conflict Handling**: Duplicate prevention with ON CONFLICT DO NOTHING
- **Robust Error Handling**: Graceful handling of data insertion errors

## 🛠️ Prerequisites

- PostgreSQL (version 12 or higher)
- pgvector extension installed
- Python 3.7+
- ArXiv dataset with embeddings (JSON format)

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd SQL_project_working_with_scientific_papers
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL database:**
   - Create a database named `arxiv_db`
   - Install and enable pgvector extension:
     ```sql
     CREATE EXTENSION vector;
     ```

4. **Create the database table:**
   ```bash
   psql -d arxiv_db -f table_creation.sql
   ```

5. **Configure environment variables:**
   - Copy `.env.example` to `.env` (if available)
   - Set your PostgreSQL password in `.env`:
     ```
     POSTGRE_PASSCODE=your_password_here
     ```

## 📊 Database Schema

The `arxiv_papers` table includes:

| Column | Type | Description |
|--------|------|-------------|
| id | VARCHAR(255) | Primary key - ArXiv paper ID |
| submitter | VARCHAR(255) | Paper submitter |
| authors | TEXT | List of authors |
| title | TEXT | Paper title |
| comments | TEXT | Additional comments |
| journal_ref | VARCHAR(300) | Journal reference |
| doi | TEXT | Digital Object Identifier |
| report_no | TEXT | Report number |
| categories | TEXT | ArXiv categories |
| license | TEXT | License information |
| abstract | TEXT | Paper abstract |
| versions | JSON | Version history |
| update_date | DATE | Last update date |
| authors_parsed | JSON | Parsed author information |
| embedding | vector(1536) | 1536-dimensional vector embedding |

## 🚀 Usage

### Basic Data Loading

1. **Prepare your dataset:**
   - Ensure you have `ml-arxiv-embeddings_1000.json` in the project root
   - The JSON should contain ArXiv papers with embeddings

2. **Run the data loader:**
   ```bash
   python data_load.py
   ```

### Example Queries

After loading data, you can perform various queries:

```sql
-- Find papers similar to a given embedding
SELECT title, abstract, embedding <-> '[0.1, 0.2, ...]' as distance 
FROM arxiv_papers 
ORDER BY distance 
LIMIT 10;

-- Search by category
SELECT title, authors, categories 
FROM arxiv_papers 
WHERE categories LIKE '%cs.AI%';

-- Count papers by year
SELECT EXTRACT(YEAR FROM update_date) as year, COUNT(*) 
FROM arxiv_papers 
GROUP BY year 
ORDER BY year DESC;
```

## 📁 Project Structure

```
SQL_project_working_with_scientific_papers/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── data_load.py                       # Main data loading script
├── table_creation.sql                 # Database schema
├── ml-arxiv-embeddings_1000.json     # Sample dataset (1000 papers)
├── dataset.zip                       # Full dataset archive
├── .env                              # Environment variables
├── .gitignore                        # Git ignore rules
├── Read_me.txt                       # Original readme (port info)
└── extra_files/                      # Additional resources
    ├── data_load_with_explanation.py  # Documented version
    └── data_load_with_explanation2.py # Alternative version
```

## 🔧 Configuration

### Database Connection

The project connects to PostgreSQL using these default settings:
- **Database**: `arxiv_db`
- **User**: `postgres`
- **Host**: `localhost`
- **Port**: `5432`
- **Password**: Set via `POSTGRE_PASSCODE` environment variable

### Environment Variables

Create a `.env` file with:
```
POSTGRE_PASSCODE=your_postgresql_password
```

## 🧪 Development

### Running with Explanations

For learning purposes, use the documented versions in `extra_files/`:
- `data_load_with_explanation.py`: Detailed comments explaining each step
- `data_load_with_explanation2.py`: Alternative implementation approach

### Error Handling

The script includes robust error handling:
- Continues processing even if individual records fail
- Reports specific errors for debugging
- Uses database transactions for data consistency

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source. Please check the individual paper licenses in the dataset.

## ⚠️ Important Notes

- Ensure pgvector extension is properly installed before running
- The embedding dimension must match your model (default: 1536)
- Large datasets may require batch processing for optimal performance
- Always backup your database before running data loading scripts

## 🔍 Troubleshooting

**Connection Issues:**
- Verify PostgreSQL is running on port 5432
- Check database credentials in `.env` file
- Ensure `arxiv_db` database exists

**pgvector Issues:**
- Confirm pgvector extension is installed: `SELECT * FROM pg_extension WHERE extname = 'vector';`
- Check vector dimension matches your embeddings

**Data Loading Issues:**
- Verify JSON file path and format
- Check for missing required fields in dataset
- Monitor console output for specific error messages

---

For questions or support, please open an issue in the repository.