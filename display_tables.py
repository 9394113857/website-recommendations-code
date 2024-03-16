import sqlite3
from prettytable import PrettyTable

def display_table(table_name):
    conn = sqlite3.connect('recommendations.db')
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
    
    # Display the table
    print(f"Data types of columns in {table_name} table:")
    print(table)
    
    # Close the connection
    conn.close()

if __name__ == '__main__':
    display_table('Users')
    display_table('Recommendations')
