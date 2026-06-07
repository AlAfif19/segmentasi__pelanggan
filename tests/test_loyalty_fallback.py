import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from services.crispdm_service import calculate_loyalty


def test_calculate_loyalty_prefers_active_date():
    result = calculate_loyalty(
        analysis_date=date(2026, 6, 7),
        active_date=date(2025, 1, 1),
        first_transaction=date(2025, 7, 1),
        last_transaction=date(2026, 6, 1),
    )

    assert result == {"days": 522, "source": "active_date"}


def test_calculate_loyalty_falls_back_to_transaction_span():
    result = calculate_loyalty(
        analysis_date=date(2026, 6, 7),
        active_date=None,
        first_transaction=date(2025, 7, 6),
        last_transaction=date(2026, 6, 7),
    )

    assert result == {"days": 336, "source": "transaction_span"}


def test_calculate_loyalty_is_zero_for_one_or_no_transaction():
    one_transaction = calculate_loyalty(
        analysis_date=date(2026, 6, 7),
        active_date=None,
        first_transaction=date(2026, 5, 1),
        last_transaction=date(2026, 5, 1),
    )
    no_transaction = calculate_loyalty(
        analysis_date=date(2026, 6, 7),
        active_date=None,
        first_transaction=None,
        last_transaction=None,
    )

    assert one_transaction == {"days": 0, "source": "transaction_span"}
    assert no_transaction == {"days": 0, "source": "unavailable"}


def test_calculate_loyalty_never_returns_negative_days():
    result = calculate_loyalty(
        analysis_date=date(2026, 6, 7),
        active_date=None,
        first_transaction=date(2026, 6, 7),
        last_transaction=date(2026, 5, 1),
    )

    assert result["days"] == 0
