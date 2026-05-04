import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr, trim, when

from pipeline.utils.db import execute_sql

JDBC_PACKAGE = "com.microsoft.sqlserver:mssql-jdbc:12.8.1.jre11"

def get_jdbc_url() -> str:
    host = os.getenv("MSSQL_HOST", "mssql")
    port = os.getenv("MSSQL_PORT", "1433")
    database = os.getenv("MSSQL_DB", "master")

    return (
        f"jdbc:sqlserver://{host}:{port};"
        f"databaseName={database};"
        "encrypt=false;"
        "trustServerCertificate=true"
    )

def create_spark_session() -> SparkSession:
    return (
        SparkSession.builder
        .appName("production-quality-pipeline")
        .master('local[*]')
        .config("spark.jars.packages", JDBC_PACKAGE)
        .getOrCreate()
    )

def get_jdbc_properties() -> dict:
    return {
        "user": os.getenv("MSSQL_USER", "sa"),
        "password": os.getenv("MSSQL_PASSWORD"),
        "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
    }

def read_raw_events(spark: SparkSession):
    jdbc_url = get_jdbc_url()
    jdbc_properties = get_jdbc_properties()

    return (
        spark.read
        .jdbc(
            url=jdbc_url,
            table="raw.machine_events_raw",
            properties=jdbc_properties
        )
    )

if __name__ == "__main__":
    spark = create_spark_session()
    raw_df = read_raw_events(spark)
    print('Rows in RAW:',raw_df.count())
    raw_df.show(10,truncate=False)
    spark.stop()