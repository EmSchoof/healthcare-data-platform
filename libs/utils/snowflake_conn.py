# import modules
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import snowflake.connector
from dotenv import load_dotenv
load_dotenv()
import os

# dynamically find key file in local repo
key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'rsa_key.p8')

# load passkey
with open(key_path, "rb") as key_file:
    p_key = serialization.load_pem_private_key(
        key_file.read(),
        password=os.getenv("SNOWFLAKE_PASSKEY_ENCRYPT").encode(),
        backend=default_backend()
    )

# encrypy passkey
passkey_encrypted = p_key.private_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
)

def connect_to_snowflake() -> None:
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        private_key=passkey_encrypted,
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("SNOWFLAKE_ROLE")
    )

    cur = conn.cursor()
    cur.execute("SELECT CURRENT_VERSION(), CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA()")
    row = cur.fetchone()
    print("Connected successfully.")
    print(f"Snowflake version: {row[0]}")
    print(f"Warehouse: {row[1]}")
    print(f"Database: {row[2]}")
    print(f"Schema: {row[3]}")
    return conn, cur


if __name__ == "__main__":
    print("ACCOUNT =", os.getenv("SNOWFLAKE_USER"))
    main()