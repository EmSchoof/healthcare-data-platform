# import modules
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import snowflake.connector
from dotenv import load_dotenv
load_dotenv()
import os

# dynamically load passkey
with open("rsa_key.p8", "rb") as key_file:
    p_key = serialization.load_pem_private_key(
        key_file.read(),
        password=os.getenv("SNOWFLAKE_PASSKEY_ENCRYPT").encode(),
        backend=default_backend()
    )

pkb = p_key.private_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

def main() -> None:
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        private_key=pkb,
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("SNOWFLAKE_ROLE")
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
    print("ACCOUNT =", os.getenv("SNOWFLAKE_USER"))
    main()