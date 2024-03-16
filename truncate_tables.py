import sqlite3

def truncate_table(table_name):
    conn = sqlite3.connect('recommendations.db')
    cursor = conn.cursor()

    cursor.execute(f'DELETE FROM {table_name};')
    
    conn.commit()
    conn.close()

def main():
    while True:
        table_name = input("Enter the name of the table to truncate (Users/Recommendations): ").strip().capitalize()
        
        if table_name == 'Users' or table_name == 'Recommendations':
            truncate_table(table_name)
            print(f'Data truncated from {table_name} table successfully!')
        else:
            print("Invalid table name. Please enter either 'Users' or 'Recommendations'.")

        choice = input("Do you want to truncate another table? (yes/no): ").strip().lower()
        if choice != 'yes':
            break

    print("Exiting the script.")

if __name__ == '__main__':
    main()
