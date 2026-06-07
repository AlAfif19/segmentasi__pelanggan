import sys
from pathlib import Path

import pandas as pd
import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "data_source" / "loader"))

from load_customers import find_customer_file, load_customers


def test_find_customer_file_selects_newest_supported_file(tmp_path):
    xlsx = tmp_path / "exported_data.xlsx"
    csv = tmp_path / "exported_data.csv"
    xlsx.write_bytes(b"old")
    csv.write_bytes(b"new")
    xlsx.touch()
    csv.touch()
    xlsx_mtime = 1_700_000_000
    csv_mtime = xlsx_mtime + 10
    import os

    os.utime(xlsx, (xlsx_mtime, xlsx_mtime))
    os.utime(csv, (csv_mtime, csv_mtime))

    assert find_customer_file(tmp_path) == csv


def test_load_customers_reads_latest_csv_export(tmp_path):
    csv = tmp_path / "exported_data.csv"
    csv.write_text(
        'sep=,\n'
        'No,"No Pelanggan",Nama,Paket,Total\n'
        '1,"=""10337831""","Dessy Rahayu","Paket 2",100000\n',
        encoding="utf-8-sig",
    )

    customers = load_customers(csv)

    assert customers.attrs["source_file"] == "exported_data.csv"
    assert customers.loc[0, "customer_id"] == "10337831"
    assert customers.loc[0, "name"] == "Dessy Rahayu"
    assert customers.loc[0, "category"] == "Paket 2"
    assert customers.loc[0, "monthly_fee"] == 100000
    assert pd.isna(customers.loc[0, "active_date"])


def test_load_customers_reads_legacy_xlsx_export(tmp_path):
    xlsx = tmp_path / "exported_data.xlsx"
    pd.DataFrame(
        [
            {
                "NOPEL": "1001",
                "NAMA PELANGGAN": "Pelanggan A",
                "TGL AKTIF": "2025-01-10",
                "PAKET": "Paket 3",
                "TOTAL TARIF": 150000,
            }
        ]
    ).to_excel(xlsx, index=False)

    customers = load_customers(xlsx)

    assert customers.attrs["source_file"] == "exported_data.xlsx"
    assert customers.loc[0, "customer_id"] == "1001"
    assert customers.loc[0, "active_date"] == pd.Timestamp("2025-01-10")


def test_load_customers_rejects_missing_required_columns(tmp_path):
    csv = tmp_path / "exported_data.csv"
    csv.write_text("sep=,\nNo,Nama\n1,Pelanggan A\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Kolom wajib"):
        load_customers(csv)
