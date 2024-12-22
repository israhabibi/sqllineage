from flask import Flask, request, render_template
from sqllineage.runner import LineageRunner
from sqlparse import format as sql_format
import random
from datetime import datetime, timedelta

app = Flask(__name__)

default_sql = '''insert into dwh.target_table 
select orders.id 
from src.orders as orders
left join src.order_item as order_item
on orders.id = order_item.id
where orders.created_at between '{START_TIME}' AND '{START_TIME}' ;
'''

# Function to generate a random date between two dates
def generate_random_date(start_date, end_date):
    start_timestamp = datetime.strptime(start_date, "%Y-%m-%d")
    end_timestamp = datetime.strptime(end_date, "%Y-%m-%d")
    delta = end_timestamp - start_timestamp
    random_days = random.randint(0, delta.days)
    random_date = start_timestamp + timedelta(days=random_days)
    return random_date.strftime("%Y-%m-%d")

@app.route('/', methods=['GET', 'POST'])
def index():
    sql = default_sql
    formatted_sql = ""
    response = None
    error = None

    if request.method == 'POST':
        sql = request.form.get('sql')
        action = request.form.get('action')

        if action == 'format_sql':
            if not sql:
                error = "SQL input is required."
            else:
                try:
                    # Replace placeholders with random dates using .format()
                    start_date = "2024-12-01"
                    end_date = "2024-12-31"
                    sql = sql.format(
                        START_TIME=generate_random_date(start_date, end_date),
                        END_TIME=generate_random_date(start_date, end_date)
                    )
                    
                    formatted_sql = sql_format(sql, reindent=True, keyword_case='upper')
                except Exception as e:
                    error = f"SQL Formatting Error: {str(e)}"
        
        elif action == 'lineage':
            if not sql:
                error = "SQL input is required."
            else:
                try:
                    result = LineageRunner(sql)

                    source_tables = [str(tbl) for tbl in result.source_tables]
                    target_tables = [str(tbl) for tbl in result.target_tables]

                    response = {
                        "source_tables": source_tables,
                        "target_tables": target_tables,
                        "intermediate_tables": [str(tbl) for tbl in result.intermediate_tables],
                    }
                except Exception as e:
                    error = str(e)

    return render_template('index.html', sql=sql, formatted_sql=formatted_sql, response=response, error=error)

if __name__ == '__main__':
    app.run(debug=True)
