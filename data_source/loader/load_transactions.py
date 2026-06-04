from pathlib import Path
import re

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
RAW_FILE = ROOT / "data_source/raw/exported_data_mutasi.xlsx"


def extract_customer_name(description):
    if not isinstance(description, str):
        return None
    match = re.search(r"\ban\s+(.+?)/", description, flags=re.IGNORECASE)
    if not match:
        return None
    return " ".join(match.group(1).split())


def load_transactions():
    df = pd.read_excel(RAW_FILE)
    df = df.rename(
        columns={
            "TANGGAL": "transaction_date",
            "TRANSAKSI": "transaction_type",
            "PEMBAYARAN": "payment_method",
            "BANK": "bank",
            "KETERANGAN": "raw_description",
            "UANG MASUK": "money_in",
            "UANG KELUAR": "money_out",
        }
    )
    df["customer_name"] = df["raw_description"].apply(extract_customer_name)
    return df


if __name__ == "__main__":
    df = load_transactions()
    print(f"Loaded transactions: {len(df)} rows")
