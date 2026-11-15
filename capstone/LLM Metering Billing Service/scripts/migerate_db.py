import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_PATH = PROJECT_ROOT / "metering.db"


def migrate():
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        connection.execute("PRAGMA foreign_keys = OFF")

        columns = {
            row[1]
            for row in connection.execute(
                "PRAGMA table_info(usage_records)"
            ).fetchall()
        }

        if not columns:
            raise RuntimeError(
                "usage_records table was not found. "
                "Check DATABASE_PATH before migrating."
            )

        if "cost_microdollars" in columns:
            print("Migration already applied; no changes made.")
            return

        required_columns = {
            "id",
            "customer_id",
            "model",
            "input_tokens",
            "output_tokens",
            "cost",
            "created_at",
            "idempotency_key",
        }

        if not required_columns.issubset(columns):
            raise RuntimeError(
                "Unexpected usage_records schema. "
                "Migration stopped without changing the database."
            )

        connection.execute("BEGIN IMMEDIATE")

        connection.execute("""
            CREATE TABLE usage_records_new (
                id INTEGER NOT NULL PRIMARY KEY,
                customer_id VARCHAR NOT NULL,
                idempotency_key VARCHAR(255),
                model VARCHAR NOT NULL,
                input_tokens INTEGER NOT NULL,
                cached_input_tokens INTEGER NOT NULL DEFAULT 0,
                output_tokens INTEGER NOT NULL,
                reasoning_tokens INTEGER NOT NULL DEFAULT 0,
                cost_microdollars INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                CONSTRAINT uq_usage_customer_idempotency
                    UNIQUE (customer_id, idempotency_key)
            )
        """)

        connection.execute("""
            INSERT INTO usage_records_new (
                id,
                customer_id,
                idempotency_key,
                model,
                input_tokens,
                cached_input_tokens,
                output_tokens,
                reasoning_tokens,
                cost_microdollars,
                created_at
            )
            SELECT
                id,
                customer_id,
                idempotency_key,
                model,
                input_tokens,
                0,
                output_tokens,
                0,
                CAST(ROUND(cost * 1000000) AS INTEGER),
                created_at
            FROM usage_records
        """)

        old_count = connection.execute(
            "SELECT COUNT(*) FROM usage_records"
        ).fetchone()[0]

        new_count = connection.execute(
            "SELECT COUNT(*) FROM usage_records_new"
        ).fetchone()[0]

        if old_count != new_count:
            raise RuntimeError(
                f"Record count mismatch: old={old_count}, new={new_count}"
            )

        connection.execute("DROP TABLE usage_records")
        connection.execute(
            "ALTER TABLE usage_records_new RENAME TO usage_records"
        )

        connection.execute("""
            CREATE INDEX ix_usage_records_customer_id
            ON usage_records (customer_id)
        """)

        connection.execute("""
            CREATE INDEX ix_usage_records_id
            ON usage_records (id)
        """)

        connection.commit()

        print(f"Migration successful. Preserved {new_count} records.")

        records = connection.execute("""
            SELECT id, customer_id, cost_microdollars
            FROM usage_records
            ORDER BY id
        """).fetchall()

        for record in records:
            print(record)

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    migrate()
