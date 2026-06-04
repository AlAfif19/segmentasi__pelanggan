from repositories import mysql_repository


def search_customers(keyword="", category="name", segment="all"):
    if mysql_repository.is_ready() and mysql_repository.has_segmentation_results():
        return mysql_repository.search_customers(keyword, category, segment)
    return []
