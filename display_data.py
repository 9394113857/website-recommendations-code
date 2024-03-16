import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('recommendations.db')
cursor = conn.cursor()

# Define a function to display records in a table format
def display_table(table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    records = cursor.fetchall()

    if len(records) == 0:
        print(f"No records found in the '{table_name}' table.")
        return

    column_names = [description[0] for description in cursor.description]

    # Print table header
    print(f"\n{table_name.capitalize()} Table:")
    print("|", end="")
    for column_name in column_names:
        print(f" {column_name} |", end="")
    print("")

    # Print table rows
    for record in records:
        print("|", end="")
        for value in record:
            print(f" {value} |", end="")
        print("")

# Display records for Users table
display_table("users")

# Display records for Recommendations table
display_table("recommendations")

# Close the database connection
conn.close()
