import sqlite3
from prettytable import PrettyTable
import os

def display_tables():
    db_path = os.path.join(os.getcwd(), 'instance', 'recommendations.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get the list of tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    # Display the list of tables
    print("\nTables in the database:")
    for table in tables:
        print(table[0])

    # Close the connection
    conn.close()

    # Return list of table names
    return [table[0] for table in tables]

def display_table_data(table_name):
    db_path = os.path.join(os.getcwd(), 'instance', 'recommendations.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch data from the table
    cursor.execute(f'SELECT * FROM {table_name}')
    rows = cursor.fetchall()

    # Get column names and data types
    cursor.execute(f'PRAGMA table_info({table_name})')
    columns_info = cursor.fetchall()
    columns = [col[1] for col in columns_info]
    data_types = [col[2] for col in columns_info]

    # Create a PrettyTable
    table = PrettyTable(['Column Name', 'Data Type'])
    table.align = 'l'

    # Add rows to the table
    for column, data_type in zip(columns, data_types):
        table.add_row([column, data_type])

    # Display the table description
    print(f"\nData types of columns in {table_name} table:")
    print(table)

    # Display the table data
    print(f"\nData in {table_name} table:")
    print("+" + "+".join("-" * (len(name) + 2) for name in columns) + "+")
    print("| " + " | ".join(name.center(len(name) + 2) for name in columns) + " |")
    print("+" + "+".join("-" * (len(name) + 2) for name in columns) + "+")
    for row in rows:
        print("| " + " | ".join(str(value).center(len(name) + 2) for value, name in zip(row, columns)) + " |")
    print("+" + "+".join("-" * (len(name) + 2) for name in columns) + "+")

    # Close the connection
    conn.close()

if __name__ == '__main__':
    table_names = display_tables()
    while True:
        table_name = input("\nEnter the name of the table to describe or fetch (or type 'exit' to quit): ").strip()
        if table_name.lower() == 'exit':
            break
        elif table_name in table_names or any(name.startswith(table_name) for name in table_names):
            display_table_data(table_name)
        else:
            print("Please provide a valid table name.")
