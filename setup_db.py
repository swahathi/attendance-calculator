import mysql.connector
from mysql.connector import Error
from pathlib import Path
from config import MYSQL_CONFIG

def setup_database():
    """Reads schema.sql and initializes the database."""
    schema_path = Path("database") / "schema.sql"
    
    if not schema_path.exists():
        print(f"Error: {schema_path} not found.")
        return

    try:
        # Connect without database first to create it
        conn = mysql.connector.connect(
            host=MYSQL_CONFIG['host'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password']
        )
        cursor = conn.cursor()
        
        # Read and execute schema
        with open(schema_path, 'r') as f:
            sql_commands = f.read().split(';')
            
            for command in sql_commands:
                if command.strip():
                    cursor.execute(command)
        
        conn.commit()
        print("Database schema initialized successfully.")
        
        # Add a sample college
        cursor.execute("USE attendance_system")
        cursor.execute("INSERT IGNORE INTO colleges (college_name, college_code, email) VALUES (%s, %s, %s)", 
                       ("Sample College", "SC001", "admin@sample.edu"))
        conn.commit()
        print("Sample college added.")
        
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    setup_database()
