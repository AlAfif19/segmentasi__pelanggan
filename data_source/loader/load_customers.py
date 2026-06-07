from pathlib import Path
import re

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data_source/raw"
SUPPORTED_FILES = ("exported_data.csv", "exported_data.xlsx")


def find_customer_file(raw_dir=RAW_DIR):
    raw_dir = Path(raw_dir)
    candidates = [raw_dir / name for name in SUPPORTED_FILES if (raw_dir / name).is_file()]
    if not candidates:
        expected = ", ".join(SUPPORTED_FILES)
        raise FileNotFoundError(f"Data pelanggan tidak ditemukan. Gunakan salah satu: {expected}")
    return max(candidates, key=lambda path: path.stat().st_mtime)


def _clean_exported_text(value):
    if pd.isna(value):
        return value
    text = str(value).strip()
    match = re.fullmatch(r'="(.*)"', text)
    return match.group(1) if match else text


def _read_source(path):
    if path.suffix.lower() == ".csv":
        first_line = path.open("r", encoding="utf-8-sig").readline().strip()
        return pd.read_csv(path, skiprows=1 if first_line.lower().startswith("sep=") else 0)
    if path.suffix.lower() == ".xlsx":
        return pd.read_excel(path, engine="openpyxl")
    raise ValueError("Format data pelanggan harus CSV atau XLSX")


def load_customers(source_file=None):
    source_file = Path(source_file) if source_file else find_customer_file()
    df = _read_source(source_file)
    column_map = {
        "No Pelanggan": "customer_id",
        "Nama": "name",
        "Paket": "category",
        "Total": "monthly_fee",
        "NOPEL": "customer_id",
        "NAMA PELANGGAN": "name",
        "TGL AKTIF": "active_date",
        "PAKET": "category",
        "TOTAL TARIF": "monthly_fee",
    }
    normalized = df.rename(columns=column_map)
    required = {"customer_id", "name", "category", "monthly_fee"}
    missing = sorted(required - set(normalized.columns))
    if missing:
        raise ValueError(f"Kolom wajib tidak ditemukan: {', '.join(missing)}")
    if "active_date" not in normalized:
        normalized["active_date"] = pd.NaT

    normalized = normalized[["customer_id", "name", "active_date", "category", "monthly_fee"]].copy()
    normalized["customer_id"] = normalized["customer_id"].map(_clean_exported_text)
    normalized["name"] = normalized["name"].map(_clean_exported_text)
    normalized["category"] = normalized["category"].map(_clean_exported_text)
    normalized["active_date"] = pd.to_datetime(normalized["active_date"], errors="coerce")
    normalized["monthly_fee"] = pd.to_numeric(normalized["monthly_fee"], errors="coerce")
    normalized.attrs["source_file"] = source_file.name
    return normalized


if __name__ == "__main__":
    df = load_customers()
    print(f"Loaded customers: {len(df)} rows")
