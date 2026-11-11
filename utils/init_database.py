
import os
import time
import pyodbc
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

def initialize_database():
    server = os.getenv("DB_SERVER", "127.0.0.1")
    port = os.getenv("DB_PORT", "1433")
    username = os.getenv("DB_USER", "sa")
    password = os.getenv("DB_PASSWORD")

    if not password:
        raise ValueError("DB_PASSWORD is missing")

    connection_string = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={server},{port};"
        "DATABASE=master;"
        f"UID={username};"
        f"PWD={password};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )

    # Wait for SQL Server to become available
    for attempt in range(30):
        try:
            connection = pyodbc.connect(
                connection_string,
                timeout=5,
                autocommit=True
            )
            break
        except pyodbc.Error:
            if attempt == 29:
                raise
            print("Waiting for SQL Server...")
            time.sleep(2)

    try:
        for filename in ["schema.sql", "seed_data.sql"]:
            script_path = PROJECT_ROOT / "database" / filename
            script = script_path.read_text(encoding="utf-8")

            # SQL Server GO statements separate batches
            import re
            batches = re.split(
                r"(?im)^\s*GO\s*$",
                script
            )

            cursor = connection.cursor()

            for batch in batches:
                if batch.strip():
                    cursor.execute(batch)

                    # Consume all result sets before next batch
                    while cursor.nextset():
                        pass

            cursor.close()
            print(f"Executed {filename}")

    finally:
        connection.close()

    print("Database initialization completed")


if __name__ == "__main__":
    initialize_database()
