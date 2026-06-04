from repositories import mysql_repository


def calculate_metrics():
    if mysql_repository.is_ready():
        metrics = mysql_repository.get_latest_evaluation()
        if metrics:
            return metrics
    return {
        "dbi": None,
        "chi": None,
        "silhouette_score": None,
        "segment_level_count": 3,
    }
