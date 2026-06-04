from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
RAW_FILE = ROOT / "data_source/raw/exported_data.xlsx"


def load_customers():
    df = pd.read_excel(RAW_FILE)
    return df.rename(
        columns={
            "NOPEL": "customer_id",
            "NAMA PELANGGAN": "name",
            "TGL AKTIF": "active_date",
            "PAKET": "category",
            "TOTAL TARIF": "monthly_fee",
        }
    )


if __name__ == "__main__":
    df = load_customers()
    print(f"Loaded customers: {len(df)} rows")
