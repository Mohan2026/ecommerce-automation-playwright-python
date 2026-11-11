
import os
import pyodbc
from pathlib import Path
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


def get_db_connection():
    server = os.getenv("DB_SERVER", "127.0.0.1")
    port = os.getenv("DB_PORT", "1433")
    database = os.getenv("DB_NAME")
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    if not all([database, username, password]):
        raise ValueError("Missing database settings in .env")

    connection_string = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={server},{port};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )

    return pyodbc.connect(connection_string, timeout=10)


def get_test_customer(test_case_id):
    with get_db_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT FirstName, LastName, PostalCode
            FROM TestCustomers
            WHERE TestCaseID = ?
              AND IsActive = 1
            """,
            (test_case_id,)
        )

        row = cursor.fetchone()
        cursor.close()

    if row is None:
        raise ValueError(
            f"No active customer found for {test_case_id}"
        )

    return {
        "FirstName": row[0],
        "LastName": row[1],
        "PostalCode": row[2]
    }


def get_product_price(product_name):
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT ExpectedPrice
            FROM dbo.TestProducts
            WHERE ProductName = ?
              AND IsActive = 1
            """,
            (product_name,)
        )

        row = cursor.fetchone()

        if row is None:
            raise ValueError(
                f"Product not found in database: {product_name}"
            )

        return row[0]

    finally:
        connection.close()
