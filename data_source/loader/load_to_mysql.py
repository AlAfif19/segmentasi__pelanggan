import sys
import os
from pathlib import Path

import pandas as pd
from werkzeug.security import generate_password_hash

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from load_customers import load_customers
from load_transactions import load_transactions
from repositories import mysql_repository
from utils.database import execute, execute_many, execute_sql_file


def clean_value(value):
    if pd.isna(value):
        return None
    if hasattr(value, "to_pydatetime"):
        return value.to_pydatetime()
    if isinstance(value, str):
        return value.strip()
    return value


def truncate_text(value, limit=1000):
    value = clean_value(value)
    if value is None:
        return None
    return str(value)[:limit]


def normalized_name(value):
    if not isinstance(value, str):
        return ""
    return " ".join(value.lower().split())


def init_database():
    execute_sql_file(ROOT / "database/schema.sql", include_database=False)
    execute_sql_file(ROOT / "database/indexes.sql", include_database=True)
    execute_sql_file(ROOT / "database/views.sql", include_database=True)
    mysql_repository.ensure_runtime_schema()
    for table in [
        "cluster_results",
        "lrfmc_transformations",
        "evaluation_metrics",
        "model_results",
        "transactions",
        "customers",
        "datasets",
    ]:
        execute(f"DELETE FROM {table}")
    execute(
        """
        INSERT INTO data_analysts (username, password_hash, role)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE password_hash = VALUES(password_hash), role = VALUES(role)
        """,
        (
            os.getenv("ANALYST_USERNAME", "data_analyst"),
            generate_password_hash(os.getenv("ANALYST_PASSWORD", "change_this_password")),
            "Data Analyst",
        ),
    )


def load_customer_rows(customers):
    rows = []
    for _, row in customers.iterrows():
        customer_id = clean_value(row.get("customer_id"))
        name = clean_value(row.get("name"))
        if not customer_id or not name:
            continue
        rows.append(
            (
                str(customer_id),
                str(name),
                clean_value(row.get("active_date")),
                clean_value(row.get("category")),
                clean_value(row.get("monthly_fee")) or 0,
            )
        )
    execute_many(
        """
        INSERT INTO customers (customer_id, name, active_date, category, monthly_fee)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
          name = VALUES(name),
          active_date = VALUES(active_date),
          category = VALUES(category),
          monthly_fee = VALUES(monthly_fee)
        """,
        rows,
    )
    execute(
        """
        INSERT INTO datasets (filename, row_count)
        VALUES (%s, %s)
        """,
        ("exported_data.xlsx", len(rows)),
    )
    return rows


def load_transaction_rows(transactions, customer_rows):
    name_to_id = {normalized_name(name): customer_id for customer_id, name, *_ in customer_rows}
    rows = []
    for _, row in transactions.iterrows():
        customer_name = clean_value(row.get("customer_name"))
        customer_id = name_to_id.get(normalized_name(customer_name))
        transaction_date = clean_value(row.get("transaction_date"))
        if not transaction_date:
            continue
        rows.append(
            (
                customer_id,
                customer_name,
                transaction_date,
                clean_value(row.get("transaction_type")),
                clean_value(row.get("payment_method")),
                clean_value(row.get("bank")),
                truncate_text(row.get("raw_description")),
                clean_value(row.get("money_in")) or 0,
                clean_value(row.get("money_out")) or 0,
            )
        )
    execute_many(
        """
        INSERT INTO transactions (
          customer_id, customer_name, transaction_date, transaction_type,
          payment_method, bank, raw_description, money_in, money_out
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        rows,
    )
    execute(
        """
        INSERT INTO datasets (filename, row_count)
        VALUES (%s, %s)
        """,
        ("exported_data_mutasi.xlsx", len(rows)),
    )
    return rows


def main():
    init_database()
    customers = load_customers()
    transactions = load_transactions()
    customer_rows = load_customer_rows(customers)
    transaction_rows = load_transaction_rows(transactions, customer_rows)
    print(f"Inserted/updated {len(customer_rows)} customers")
    print(f"Inserted {len(transaction_rows)} transactions")


if __name__ == "__main__":
    main()
