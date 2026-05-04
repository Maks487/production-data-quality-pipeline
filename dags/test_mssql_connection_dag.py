from datetime import datetime

import pymssql
from airflow.decorators import dag, task


@dag(
    dag_id="test_mssql_connection",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["test", "mssql"],
)
def test_mssql_connection():

    @task
    def create_test_table():
        conn = pymssql.connect(
            server="mssql",
            user="de_user",
            password="DeUser123!",
            database="master",
        )

        cursor = conn.cursor()

        cursor.execute("""
        IF OBJECT_ID('dbo.airflow_test', 'U') IS NULL
        CREATE TABLE dbo.airflow_test (
            id INT IDENTITY(1,1) PRIMARY KEY,
            message VARCHAR(255),
            created_at DATETIME DEFAULT GETDATE()
        )
        """)

        cursor.execute("""
        INSERT INTO dbo.airflow_test (message)
        VALUES ('Hello from Airflow')
        """)

        conn.commit()
        conn.close()

    create_test_table()


test_mssql_connection()
