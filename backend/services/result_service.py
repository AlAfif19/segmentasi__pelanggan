from repositories import mysql_repository
from services.embedded_data_service import get_summary
from services.evaluation_service import calculate_metrics


def get_results(page=1, per_page=10, keyword="", category="name", segment="all", payment_status="all"):
    if mysql_repository.is_ready():
        page = max(int(page), 1)
        per_page = min(max(int(per_page), 1), 100)
        offset = (page - 1) * per_page
        summary = mysql_repository.get_summary()
        evaluation = mysql_repository.get_latest_evaluation()
        clusters = mysql_repository.get_clusters()
        customers = mysql_repository.get_customers(
            limit=per_page,
            offset=offset,
            keyword=keyword,
            category=category,
            segment=segment,
            payment_status=payment_status,
        )
        total = mysql_repository.count_customers_result(keyword, category, segment, payment_status)
        return {
            "summary": summary or get_summary(),
            "evaluation": evaluation or calculate_metrics(),
            "clusters": clusters,
            "customers": customers,
            "cluster_profile": mysql_repository.get_cluster_profile(),
            "k_evaluation": mysql_repository.get_k_evaluation_history(),
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "total_pages": (total + per_page - 1) // per_page if per_page else 1,
            },
            "database_ready": True,
        }
    return {
        "summary": get_summary(),
        "evaluation": calculate_metrics(),
        "clusters": [],
        "customers": [],
        "cluster_profile": [],
        "k_evaluation": [],
        "pagination": {"page": 1, "per_page": per_page, "total": 0, "total_pages": 1},
        "database_ready": False,
    }
