import sqlite3

def create_tables():
    conn = sqlite3.connect('recommendations.db')
    cursor = conn.cursor()
    
    # Check if tables already exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Users'")
    users_table_exists = cursor.fetchone()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Recommendations'")
    recommendations_table_exists = cursor.fetchone()
    
    if users_table_exists and recommendations_table_exists:
        override = input("Tables 'Users' and 'Recommendations' already exist. Do you want to override them? (yes/no): ").strip().lower()
        if override == 'yes':
            # Drop existing tables
            cursor.execute("DROP TABLE IF EXISTS Users")
            cursor.execute("DROP TABLE IF EXISTS Recommendations")
            print("Existing tables dropped successfully.")
        else:
            print("Tables were not created. Exiting.")
            conn.close()
            return

    # Create new tables
    cursor.execute('''
    CREATE TABLE Users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
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

if __name__ == '__main__':
    create_tables()
    print("Tables created successfully!")
