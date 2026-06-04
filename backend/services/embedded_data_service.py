from repositories import mysql_repository


EMPTY_SUMMARY = {
    "customers": 0,
    "transactions": 0,
    "loaded_at": None,
    "algorithm": "K-Means Plus",
    "segment_levels": ["Low", "Medium", "High"],
}


def get_summary():
    if mysql_repository.is_ready():
        summary = mysql_repository.get_summary()
        if summary:
            return summary
    return EMPTY_SUMMARY


def preview_sources():
    database_ready = mysql_repository.is_ready()
    return {
        "raw_files": ["exported_data.xlsx", "exported_data_mutasi.xlsx"],
        "source": "MySQL",
        "database_ready": database_ready,
        "summary": get_summary(),
        "data_understanding": mysql_repository.get_data_understanding() if database_ready else {},
        "preview": mysql_repository.get_embedded_preview() if database_ready else {"customers": [], "transactions": []},
    }
