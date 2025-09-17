import sqlite3
import pandas as pd
import os


def create_db(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        age INTEGER NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        sale_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        item TEXT NOT NULL,
        quantity TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
    )
    ''')

    customers = [
        (1, 21),
        (2, 23),
        (3, 35),
        (4, 40),  # not in age range
        (5, 17)   # not in age range
    ]

    sales = [
        (1, 1, 'x', '7'),
        (2, 1, 'x', '3'),
        (3, 1, 'y', None),
        (4, 1, 'z', '0'),
        (5, 2, 'x', '1'),
        (6, 2, 'y', '1'),
        (7, 2, 'z', '1'),
        (8, 3, 'z', '1'),
        (9, 3, 'z', '1'),
        (10, 3, 'x', None),
        (11, 4, 'x', '5'),
        (12, 5, 'y', '3')
    ]

    cursor.executemany('INSERT INTO customers VALUES (?, ?)', customers)
    cursor.executemany('INSERT INTO sales VALUES (?, ?, ?, ?)', sales)

    conn.commit()
    conn.close()


def get_sql_output(db_file):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT
            c.customer_id as Customer,
            c.age as Age,
            s.item as Item,
            SUM(CAST(s.quantity AS INTEGER)) as Quantity
        FROM customers c
        JOIN sales s ON c.customer_id = s.customer_id
        WHERE c.age BETWEEN 18 AND 35
            AND s.quantity IS NOT NULL
            AND s.quantity != ''
            AND CAST(s.quantity AS INTEGER) > 0
        GROUP BY c.customer_id, c.age, s.item
        ORDER BY c.customer_id, s.item;
        """)
        results = cursor.fetchall()
        conn.commit()
        conn.close()
        print(f"{len(results)} records in result")
        return results
    except sqlite3.Error as e:
        print(f"Error executing SQL query: {e}")
        return []


def get_pandas_output(db_file):
    try:
        conn = sqlite3.connect(db_file)
        customers_df = pd.read_sql_query("SELECT * FROM customers", conn)
        sales_df = pd.read_sql_query("SELECT * FROM sales", conn)

        customers_filtered = customers_df[
            (customers_df['age'] >= 18) & (customers_df['age'] <= 35)
        ]

        merged_df = pd.merge(customers_filtered, sales_df, on='customer_id')
        merged_df = merged_df[
            (merged_df['quantity'].notna()) &
            (merged_df['quantity'] != '') &
            (merged_df['quantity'] != '0')
        ]

        merged_df['quantity'] = pd.to_numeric(merged_df['quantity'], errors='coerce')
        merged_df = merged_df[merged_df['quantity'] > 0]
        merged_df['quantity'] = merged_df['quantity'].astype(int)

        result_df = merged_df.groupby(['customer_id', 'age', 'item'])['quantity'].sum().reset_index()

        result_df.columns = ['Customer', 'Age', 'Item', 'Quantity']

        result_df = result_df.sort_values(['Customer', 'Item']).reset_index(drop=True)
        conn.close()
        return result_df
    except Exception as e:
        print(f"Error in Pandas solution: {e}")
        return pd.DataFrame()

def write_to_csv(data, filename, method='pandas'):
    try:
        if method == 'sql':
            df = pd.DataFrame(data, columns=['Customer', 'Age', 'Item', 'Quantity'])
        else:
            df = data
        df.to_csv(filename, sep=';', index=False)
    except Exception as e:
        print(f"Error writing to CSV: {e}")


def main():
    # DB File and output path
    try:
        db_file = os.environ.get('DATABASE_PATH', "/data/company.db")
        output_dir = os.environ.get('OUTPUT_PATH', "/output")

        os.makedirs(os.path.dirname(db_file), exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)

        if not os.path.exists(db_file):
            create_db(db_file)

        # Solution 1 from SQL
        sql_result = get_sql_output(db_file)
        if sql_result:
            sql_output_path = os.path.join(output_dir, "sql_output.csv")
            write_to_csv(sql_result, sql_output_path, method='sql')

        # Solution 2 from pandas
        panads_result = get_pandas_output(db_file)
        if not panads_result.empty:
            pandas_output_path = os.path.join(output_dir, "pandas_output.csv")
            write_to_csv(panads_result, pandas_output_path, method='pandas')

        print("Output files generated:")
        print(f"- {sql_output_path} (Pure SQL solution)")
        print(f"- {pandas_output_path} (Pandas solution)")
        print(f"- Database: {db_file}")
    except Exception as err:
        print("Something wrong", err)

if __name__ == "__main__":
    main()
