import os
import sqlite3

def list_db_files():
    db_files = [file for file in os.listdir('.') if file.endswith('.db')]
    if db_files:
        print("Existing .db files found in the directory:")
        for db_file in db_files:
            print(f"- {db_file}")
        return True
    else:
        print("No existing .db files found in the directory.")
        return False

def delete_database():
    if os.path.exists('recommendations.db'):
        delete = input("Database file 'recommendations.db' already exists. Do you want to delete it? (yes/no): ").strip().lower()
        if delete == 'yes':
            os.remove('recommendations.db')
            print("Existing database file deleted.")
            exit()

def create_tables():
    conn = sqlite3.connect('recommendations.db')
    cursor = conn.cursor()

    # Create new tables
    cursor.execute('''
    CREATE TABLE Users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password_hash TEXT NOT NULL
    );
    ''')

    cursor.execute('''
    CREATE TABLE Recommendations (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        content_id INTEGER NOT NULL,
        content_type TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES Users(id)
    );
    ''')

    conn.commit()
    conn.close()
    print("Tables created successfully!")

if __name__ == '__main__':
    if not list_db_files():
        create_tables()
    delete_database()
