# import modules
import snowflake.connector
import os

def main() -> None:
    conn = snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        database=os.environ["SNOWFLAKE_DATABASE"],
        schema=os.environ["SNOWFLAKE_SCHEMA"],
    )

    try:
        cur = conn.cursor()
        cur.execute("SELECT CURRENT_VERSION(), CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA()")
        row = cur.fetchone()
        print("Connected successfully.")
        print(f"Snowflake version: {row[0]}")
        print(f"Warehouse: {row[1]}")
        print(f"Database: {row[2]}")
        print(f"Schema: {row[3]}")
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()