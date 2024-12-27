# Flask SQL Lineage App

This Flask application allows users to:

1. Format and reindent SQL queries.
2. Extract lineage information (source and target tables) from SQL queries using `sqllineage`.

The application also supports fallback dialects for handling SQL syntax and formatting errors.

## Features

### 1. Format SQL Queries
- **Input**: SQL query.
- **Action**: Formats the SQL query with placeholders replaced by random dates.
- **Error Handling**: Provides user-friendly error messages for SQL formatting issues.

### 2. Extract Lineage Information
- **Input**: SQL query.
- **Action**: Extracts source and target table information using `sqllineage`.
- **Error Handling**: Attempts lineage extraction with multiple dialects if the primary dialect fails.

## File Structure

- **`app.py`**: Main application file containing routes and logic for SQL formatting and lineage extraction.
- **`templates/index.html`**: HTML file for the web interface.

## Dependencies

### Python Libraries
- Flask
- SQLLineage
- SQLParse

### Installation
```bash
pip install flask sqllineage sqlparse
```

## Configuration

### Default SQL Query
```sql
insert into dwh.target_table 
select orders.id 
from src.orders as orders
left join src.order_item as order_item
on orders.id = order_item.id
where orders.created_at between '{START_TIME}' AND '{END_TIME}' ;
```

- The `{START_TIME}` and `{END_TIME}` placeholders are replaced with random dates.

### Random Date Generator
- Generates a random date between a specified `start_date` and `end_date`.

### Lineage Extraction
- Primary Dialect: `sparksql`.
- Fallback Dialects: `redshift`, `athena`, `mysql`, `postgres`.

## Running the App

1. Clone the repository.
2. Install dependencies.
3. Run the Flask app:
   ```bash
   python app.py
   ```
4. Open `http://127.0.0.1:5000` in your web browser.

## Building in Docker

```bash
docker build -t flask-sql-lineage .
docker tag flask-sql-lineage isranhabibi/flask-sql-lineage:latest
docker push isranhabibi/flask-sql-lineage:latest
```

## Web Interface

- **SQL Input Field**: Accepts the SQL query.
- **Action Buttons**:
  - Format SQL
  - Extract Lineage
- **Output Section**:
  - Formatted SQL query.
  - Source and Target tables.
  - Intermediate tables (if any).
  - Used dialect for lineage extraction.
- **Error Messages**: Displays any issues encountered during processing.

## Notes

- The app uses SQLLineage to analyze SQL lineage. Ensure your SQL query is valid and matches the expected syntax for the selected dialect.
- Default host is `0.0.0.0` and default port is `5000`. Modify as needed in `app.run()`.

## Example Usage

### Input SQL
```sql
insert into dwh.target_table 
select orders.id 
from src.orders as orders
left join src.order_item as order_item
on orders.id = order_item.id
where orders.created_at between '{START_TIME}' AND '{END_TIME}' ;
```

### Actions
1. **Format SQL**:
   - Outputs a properly indented SQL query with replaced dates.
2. **Extract Lineage**:
   - Outputs:
     - Source Tables: `['src.orders', 'src.order_item']`
     - Target Tables: `['dwh.target_table']`
     - Intermediate Tables: `[]`
     - Used Dialect: `sparksql` (or fallback dialect if needed).
