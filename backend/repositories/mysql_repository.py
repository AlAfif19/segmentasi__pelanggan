from utils.database import database_available, execute, execute_many, fetch_all, fetch_one


def is_ready():
    return database_available()


def ensure_runtime_schema():
    if not is_ready():
        return
    monthly_fee_column = fetch_one(
        """
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME = 'customers'
          AND COLUMN_NAME = 'monthly_fee'
        """
    )
    if not monthly_fee_column:
        execute("ALTER TABLE customers ADD COLUMN monthly_fee DECIMAL(18, 2) NULL AFTER category")

    category_score_column = fetch_one(
        """
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME = 'lrfmc_transformations'
          AND COLUMN_NAME = 'category_score'
        """
    )
    if not category_score_column:
        execute("ALTER TABLE lrfmc_transformations ADD COLUMN category_score FLOAT NULL AFTER category")


def get_summary():
    row = fetch_one(
        """
        SELECT
          (SELECT COUNT(*) FROM customers) AS customers,
          (SELECT COUNT(*) FROM transactions) AS transactions,
          (SELECT COALESCE(SUM(money_in), 0) FROM transactions) AS total_revenue,
          (SELECT MAX(loaded_at) FROM datasets) AS loaded_at
        """
    )
    if not row:
        return None
    return {
        "customers": row["customers"] or 0,
        "transactions": row["transactions"] or 0,
        "total_revenue": float(row["total_revenue"] or 0),
        "loaded_at": str(row["loaded_at"]) if row["loaded_at"] else None,
        "algorithm": "K-Means Plus",
        "segment_levels": ["Low", "Medium", "High"],
    }


def get_latest_evaluation():
    row = fetch_one(
        """
        SELECT
          e.elbowmethod,
          e.davies_bouldin,
          e.calinski_harabasz,
          e.silhouette_avg,
          m.segment_level_count AS optimal_k,
          m.iteration
        FROM evaluation_metrics e
        LEFT JOIN model_results m ON m.id_model = (
          SELECT id_model FROM model_results ORDER BY id_model DESC LIMIT 1
        )
        ORDER BY e.id_eval DESC
        LIMIT 1
        """
    )
    if not row:
        return None
    return {
        "inertia_sse": row["elbowmethod"],
        "dbi": row["davies_bouldin"],
        "chi": row["calinski_harabasz"],
        "silhouette_score": row["silhouette_avg"],
        "segment_level_count": row["optimal_k"] or 3,
        "optimal_k": row["optimal_k"] or 3,
        "iteration": row["iteration"] or 0,
    }


def get_clusters():
    ensure_runtime_schema()
    rows = fetch_all(
        """
        SELECT
          cr.cluster,
          cr.segment_label,
          AVG(l.recency) AS avg_recency,
          AVG(l.frequency) AS avg_frequency,
          AVG(l.monetary) AS avg_monetary,
          AVG(l.loyalty) AS avg_loyalty,
          AVG(l.category_score) AS avg_category,
          COUNT(*) AS customer_count
        FROM cluster_results cr
        LEFT JOIN lrfmc_transformations l ON l.customer_id = cr.customer_id
        GROUP BY cr.cluster, cr.segment_label
        ORDER BY cr.cluster
        """
    )
    result = []
    for row in rows:
        label = row["segment_label"]
        if "High" in label:
            interpretation = "Prioritas loyalitas dan layanan premium."
        elif "Medium" in label:
            interpretation = "Potensi dikembangkan melalui retensi."
        else:
            interpretation = "Jarang transaksi dan nilai transaksi rendah."
        result.append(
            {
                "cluster": row["cluster"],
                "segment_label": label,
                "avg_recency": float(row["avg_recency"] or 0),
                "avg_frequency": float(row["avg_frequency"] or 0),
                "avg_monetary": float(row["avg_monetary"] or 0),
                "avg_loyalty": float(row["avg_loyalty"] or 0),
                "avg_category": float(row["avg_category"] or 0),
                "customer_count": row["customer_count"],
                "interpretation": interpretation,
            }
        )
    return result


def get_cluster_profile():
    rows = get_clusters()
    profile = []
    for row in rows:
        label = row["segment_label"]
        if label == "High-Value":
            detail = {
                "headline": "Prioritaskan program loyalitas, SLA penanganan cepat, dan penawaran upgrade yang relevan.",
                "actions": [
                    "Pertahankan pelanggan prioritas dengan loyalty reward dan respons gangguan lebih cepat.",
                    "Tawarkan upgrade atau add-on hanya pada pelanggan dengan transaksi dan tier paket tinggi.",
                    "Kirim reminder pembayaran ringan sebelum jatuh tempo agar pola pembayaran tetap stabil.",
                ],
                "risk": "Risiko utama adalah churn pelanggan bernilai tinggi jika kualitas layanan menurun.",
            }
        elif label == "Medium-Value":
            detail = {
                "headline": "Dorong pelanggan naik kelas melalui bundling paket dan benefit pembayaran tepat waktu.",
                "actions": [
                    "Berikan promo upgrade bertahap yang tidak terlalu agresif.",
                    "Gunakan reminder pembayaran personal untuk pelanggan yang mulai jarang transaksi.",
                    "Pantau pelanggan yang frequency dan monetary-nya mendekati High-Value untuk kampanye upsell.",
                ],
                "risk": "Risiko utama adalah pelanggan stagnan atau turun ke Low-Value jika tidak ada dorongan retensi.",
            }
        else:
            detail = {
                "headline": "Aktifkan kampanye reaktivasi dengan evaluasi kebutuhan layanan atau paket yang lebih sesuai.",
                "actions": [
                    "Prioritaskan follow-up pelanggan dengan jarak transaksi terakhir paling lama.",
                    "Tawarkan paket hemat, diskon terbatas, atau penyesuaian layanan sebelum promosi besar.",
                    "Hentikan kampanye mahal bila tidak ada respons atau transaksi ulang.",
                ],
                "risk": "Risiko utama adalah pelanggan tidak aktif permanen atau hanya bertahan di paket rendah.",
            }
        profile.append(
            {
                "cluster": row["cluster"],
                "segment_label": label,
                "customer_count": row["customer_count"],
                "loyalty": row["avg_loyalty"],
                "recency": row["avg_recency"],
                "frequency": row["avg_frequency"],
                "monetary": row["avg_monetary"],
                "category": row["avg_category"],
                "business_recommendation": detail["headline"],
                "recommendation_detail": detail,
            }
        )
    return profile


def _payment_summary_join():
    return """
        LEFT JOIN (
          SELECT
            payment_rows.customer_id,
            COUNT(*) AS total_payments,
            SUM(CASE WHEN payment_rows.due_date IS NOT NULL AND payment_rows.transaction_date <= payment_rows.due_date THEN 1 ELSE 0 END) AS on_time_payments,
            SUM(CASE WHEN payment_rows.due_date IS NOT NULL AND payment_rows.transaction_date > payment_rows.due_date THEN 1 ELSE 0 END) AS late_payments
          FROM (
            SELECT
              customer_id,
              transaction_date,
              STR_TO_DATE(SUBSTRING(REGEXP_SUBSTR(raw_description, '[0-9]{8}-[0-9]{8}'), 10, 8), '%d%m%Y') AS due_date
            FROM transactions
            WHERE money_in > 0
              AND transaction_date IS NOT NULL
              AND (
                UPPER(COALESCE(transaction_type, '')) LIKE '%%TAGIHAN%%'
                OR UPPER(COALESCE(transaction_type, '')) LIKE '%%PEMBAYARAN%%'
                OR UPPER(COALESCE(transaction_type, '')) LIKE '%%BAYAR%%'
              )
          ) payment_rows
          GROUP BY payment_rows.customer_id
        ) ps ON ps.customer_id = cr.customer_id
    """


def _payment_status_expression():
    return """
        CASE
          WHEN COALESCE(ps.total_payments, 0) = 0
            OR COALESCE(ps.late_payments, 0) + COALESCE(ps.on_time_payments, 0) = 0
          THEN 'Belum teridentifikasi'
          WHEN COALESCE(ps.late_payments, 0) > COALESCE(ps.on_time_payments, 0)
          THEN 'Sering terlambat'
          ELSE 'Tepat waktu'
        END
    """


def _customer_filter_clause(keyword="", category="name", segment="all", payment_status="all"):
    field = "c.customer_id" if category == "customer_id" else "c.name"
    clauses = [f"{field} LIKE %s"]
    params = [f"%{keyword or ''}%"]
    if segment != "all":
        clauses.append("cr.segment_label = %s")
        params.append(segment)
    if payment_status == "late":
        clauses.append("COALESCE(ps.late_payments, 0) > COALESCE(ps.on_time_payments, 0)")
    elif payment_status == "on_time":
        clauses.append(
            "COALESCE(ps.total_payments, 0) > 0 "
            "AND COALESCE(ps.late_payments, 0) + COALESCE(ps.on_time_payments, 0) > 0 "
            "AND COALESCE(ps.late_payments, 0) <= COALESCE(ps.on_time_payments, 0)"
        )
    elif payment_status == "unknown":
        clauses.append(
            "COALESCE(ps.total_payments, 0) = 0 "
            "OR COALESCE(ps.late_payments, 0) + COALESCE(ps.on_time_payments, 0) = 0"
        )
    return " AND ".join(f"({clause})" for clause in clauses), params


def count_customers_result(keyword="", category="name", segment="all", payment_status="all"):
    where_clause, params = _customer_filter_clause(keyword, category, segment, payment_status)
    row = fetch_one(
        f"""
        SELECT COUNT(*) AS total
        FROM cluster_results cr
        JOIN customers c ON c.customer_id = cr.customer_id
        {_payment_summary_join()}
        WHERE {where_clause}
        """,
        tuple(params),
    )
    return row["total"] if row else 0


def get_k_evaluation_history():
    latest = get_latest_evaluation()
    if not latest:
        return []
    optimal = latest.get("optimal_k") or 3
    return [
        {
            "k": optimal,
            "inertia_sse": latest.get("inertia_sse"),
            "silhouette_score": latest.get("silhouette_score"),
            "davies_bouldin_index": latest.get("dbi"),
            "calinski_harabasz_index": latest.get("chi"),
            "iteration": latest.get("iteration"),
            "selected": True,
        }
    ]


def get_customers(limit=10, offset=0, keyword="", category="name", segment="all", payment_status="all"):
    ensure_runtime_schema()
    where_clause, params = _customer_filter_clause(keyword, category, segment, payment_status)
    params.extend([limit, offset])
    payment_status_sql = _payment_status_expression()
    return fetch_all(
        f"""
        SELECT
          c.customer_id,
          c.name,
          c.monthly_fee,
          l.loyalty,
          l.recency,
          l.frequency,
          l.monetary,
          l.category,
          l.category_score,
          l.lrfmc_combination,
          cr.cluster,
          cr.segment_label,
          COALESCE(ps.total_payments, 0) AS payment_total,
          COALESCE(ps.on_time_payments, 0) AS on_time_payments,
          COALESCE(ps.late_payments, 0) AS late_payments,
          {payment_status_sql} AS payment_status,
          CASE
            WHEN cr.segment_label LIKE 'High%%' THEN 'Prioritas loyalitas dan layanan premium.'
            WHEN cr.segment_label LIKE 'Medium%%' THEN 'Potensi dikembangkan melalui retensi.'
            ELSE 'Jarang transaksi dan nilai transaksi rendah.'
          END AS cluster_interpretation,
          CASE
            WHEN cr.segment_label LIKE 'High%%' THEN 'Pertahankan pelanggan prioritas dengan loyalty reward, SLA cepat, dan penawaran upgrade.'
            WHEN cr.segment_label LIKE 'Medium%%' THEN 'Dorong retensi dengan bundling, reminder pembayaran, dan penawaran paket menengah.'
            ELSE 'Aktifkan kembali pelanggan dengan kampanye reaktivasi dan evaluasi kebutuhan layanan.'
          END AS business_recommendation,
          CASE
            WHEN cr.segment_label LIKE 'High%%' THEN 'Prioritas loyalty reward.'
            WHEN cr.segment_label LIKE 'Medium%%' THEN 'Retensi dan penawaran paket menengah.'
            ELSE 'Kampanye reaktivasi pelanggan.'
          END AS recommendation
        FROM cluster_results cr
        JOIN customers c ON c.customer_id = cr.customer_id
        LEFT JOIN lrfmc_transformations l ON l.customer_id = cr.customer_id
        {_payment_summary_join()}
        WHERE {where_clause}
        ORDER BY cr.id_result DESC
        LIMIT %s OFFSET %s
        """,
        tuple(params),
    )


def has_segmentation_results():
    row = fetch_one("SELECT COUNT(*) AS total FROM cluster_results")
    return bool(row and row["total"])


def search_customers(keyword="", category="name", segment="all", limit=200):
    ensure_runtime_schema()
    where_clause, params = _customer_filter_clause(keyword, category, segment)
    params.append(limit)
    payment_status_sql = _payment_status_expression()
    return fetch_all(
        f"""
        SELECT
          c.customer_id,
          c.name,
          c.monthly_fee,
          l.loyalty,
          l.recency,
          l.frequency,
          l.monetary,
          l.category,
          l.category_score,
          l.lrfmc_combination,
          cr.cluster,
          cr.segment_label,
          COALESCE(ps.total_payments, 0) AS payment_total,
          COALESCE(ps.on_time_payments, 0) AS on_time_payments,
          COALESCE(ps.late_payments, 0) AS late_payments,
          {payment_status_sql} AS payment_status,
          CASE
            WHEN cr.segment_label LIKE 'High%%' THEN 'Prioritas loyalitas dan layanan premium.'
            WHEN cr.segment_label LIKE 'Medium%%' THEN 'Potensi dikembangkan melalui retensi.'
            ELSE 'Jarang transaksi dan nilai transaksi rendah.'
          END AS cluster_interpretation,
          CASE
            WHEN cr.segment_label LIKE 'High%%' THEN 'Pertahankan pelanggan prioritas dengan loyalty reward, SLA cepat, dan penawaran upgrade.'
            WHEN cr.segment_label LIKE 'Medium%%' THEN 'Dorong retensi dengan bundling, reminder pembayaran, dan penawaran paket menengah.'
            ELSE 'Aktifkan kembali pelanggan dengan kampanye reaktivasi dan evaluasi kebutuhan layanan.'
          END AS business_recommendation,
          CASE
            WHEN cr.segment_label LIKE 'High%%' THEN 'Prioritas loyalty reward.'
            WHEN cr.segment_label LIKE 'Medium%%' THEN 'Retensi dan penawaran paket menengah.'
            ELSE 'Kampanye reaktivasi pelanggan.'
          END AS recommendation
        FROM cluster_results cr
        JOIN customers c ON c.customer_id = cr.customer_id
        LEFT JOIN lrfmc_transformations l ON l.customer_id = cr.customer_id
        {_payment_summary_join()}
        WHERE {where_clause}
        ORDER BY c.name
        LIMIT %s
        """,
        tuple(params),
    )


def create_model_result(iteration=0):
    return create_model_result_with_k(3, iteration)


def create_model_result_with_k(optimal_k, iteration=0):
    return execute(
        "INSERT INTO model_results (algorithm_name, iteration, segment_level_count) VALUES (%s, %s, %s)",
        ("K-Means Plus", iteration, optimal_k),
    )


def create_evaluation_metrics(metrics):
    return execute(
        """
        INSERT INTO evaluation_metrics (elbowmethod, davies_bouldin, calinski_harabasz, silhouette_avg)
        VALUES (%s, %s, %s, %s)
        """,
        (
            metrics.get("elbowmethod"),
            metrics.get("dbi"),
            metrics.get("chi"),
            metrics.get("silhouette_score"),
        ),
    )


def latest_dataset_id():
    row = fetch_one("SELECT id_dataset FROM datasets ORDER BY id_dataset DESC LIMIT 1")
    return row["id_dataset"] if row else None


def find_user_by_username(username):
    return fetch_one(
        """
        SELECT id_data_analyst, username, password_hash, role
        FROM data_analysts
        WHERE username = %s
        LIMIT 1
        """,
        (username,),
    )


def get_lrfmc_source_rows():
    ensure_runtime_schema()
    return fetch_all(
        """
        SELECT
          c.customer_id,
          c.name,
          c.active_date,
          c.category,
          c.monthly_fee,
          COUNT(CASE
            WHEN t.money_in > 0
              AND t.transaction_date IS NOT NULL
              AND (
                UPPER(COALESCE(t.transaction_type, '')) LIKE '%TAGIHAN%'
                OR UPPER(COALESCE(t.transaction_type, '')) LIKE '%PEMBAYARAN%'
                OR UPPER(COALESCE(t.transaction_type, '')) LIKE '%BAYAR%'
              )
            THEN 1
          END) AS frequency,
          COALESCE(SUM(CASE
            WHEN t.money_in > 0
              AND t.transaction_date IS NOT NULL
              AND (
                UPPER(COALESCE(t.transaction_type, '')) LIKE '%TAGIHAN%'
                OR UPPER(COALESCE(t.transaction_type, '')) LIKE '%PEMBAYARAN%'
                OR UPPER(COALESCE(t.transaction_type, '')) LIKE '%BAYAR%'
              )
            THEN t.money_in ELSE 0
          END), 0) AS monetary,
          MAX(CASE
            WHEN t.money_in > 0
              AND t.transaction_date IS NOT NULL
              AND (
                UPPER(COALESCE(t.transaction_type, '')) LIKE '%TAGIHAN%'
                OR UPPER(COALESCE(t.transaction_type, '')) LIKE '%PEMBAYARAN%'
                OR UPPER(COALESCE(t.transaction_type, '')) LIKE '%BAYAR%'
              )
            THEN t.transaction_date
          END) AS last_transaction
        FROM customers c
        LEFT JOIN transactions t ON t.customer_id = c.customer_id
        GROUP BY c.customer_id, c.name, c.active_date, c.category, c.monthly_fee
        ORDER BY c.customer_id
        """
    )


def get_data_understanding():
    ensure_runtime_schema()
    customer_rows = fetch_all(
        """
        SELECT
          'customers' AS table_name,
          COUNT(*) AS row_count,
          SUM(customer_id IS NULL OR customer_id = '') AS missing_customer_id,
          SUM(name IS NULL OR name = '') AS missing_name,
          SUM(active_date IS NULL) AS missing_active_date,
          SUM(category IS NULL OR category = '') AS missing_category,
          SUM(monthly_fee IS NULL) AS missing_monthly_fee
        FROM customers
        """
    )
    transaction_rows = fetch_all(
        """
        SELECT
          'transactions' AS table_name,
          COUNT(*) AS row_count,
          SUM(customer_id IS NULL OR customer_id = '') AS missing_customer_id,
          SUM(customer_name IS NULL OR customer_name = '') AS missing_customer_name,
          SUM(transaction_date IS NULL) AS missing_transaction_date,
          SUM(money_in IS NULL) AS missing_money_in
        FROM transactions
        """
    )
    duplicate_customer_id = fetch_one(
        """
        SELECT COUNT(*) AS duplicate_count
        FROM (
          SELECT customer_id
          FROM customers
          GROUP BY customer_id
          HAVING COUNT(*) > 1
        ) d
        """
    )
    duplicate_name = fetch_one(
        """
        SELECT COUNT(*) AS duplicate_count
        FROM (
          SELECT name
          FROM customers
          GROUP BY name
          HAVING COUNT(*) > 1
        ) d
        """
    )
    category_distribution = fetch_all(
        """
        SELECT COALESCE(category, 'Tidak ada') AS label, COUNT(*) AS value
        FROM customers
        GROUP BY COALESCE(category, 'Tidak ada')
        ORDER BY value DESC
        LIMIT 12
        """
    )
    transaction_distribution = fetch_all(
        """
        SELECT COALESCE(transaction_type, 'Tidak ada') AS label, COUNT(*) AS value
        FROM transactions
        GROUP BY COALESCE(transaction_type, 'Tidak ada')
        ORDER BY value DESC
        LIMIT 12
        """
    )
    payment_distribution = fetch_all(
        """
        SELECT COALESCE(payment_method, 'Tidak ada') AS label, COUNT(*) AS value
        FROM transactions
        GROUP BY COALESCE(payment_method, 'Tidak ada')
        ORDER BY value DESC
        LIMIT 12
        """
    )
    relevant = fetch_one(
        """
        SELECT COUNT(*) AS total
        FROM transactions
        WHERE money_in > 0
          AND transaction_date IS NOT NULL
          AND customer_id IS NOT NULL
          AND (
            UPPER(COALESCE(transaction_type, '')) LIKE '%TAGIHAN%'
            OR UPPER(COALESCE(transaction_type, '')) LIKE '%PEMBAYARAN%'
            OR UPPER(COALESCE(transaction_type, '')) LIKE '%BAYAR%'
          )
        """
    )
    return {
        "structure": [*customer_rows, *transaction_rows],
        "duplicates": {
            "customer_id": duplicate_customer_id["duplicate_count"] if duplicate_customer_id else 0,
            "name": duplicate_name["duplicate_count"] if duplicate_name else 0,
        },
        "distributions": {
            "category": category_distribution,
            "transaction_type": transaction_distribution,
            "payment_method": payment_distribution,
        },
        "relevant_transactions": relevant["total"] if relevant else 0,
    }


def get_embedded_preview(limit=10):
    customers = fetch_all(
        """
        SELECT customer_id, name, active_date, category, monthly_fee
        FROM customers
        ORDER BY customer_id
        LIMIT %s
        """,
        (limit,),
    )
    transactions = fetch_all(
        """
        SELECT customer_id, customer_name, transaction_date, transaction_type, payment_method, money_in, money_out
        FROM transactions
        ORDER BY id_transaction
        LIMIT %s
        """,
        (limit,),
    )
    return {
        "customers": customers,
        "transactions": transactions,
    }


def get_analysis_date():
    row = fetch_one("SELECT COALESCE(MAX(transaction_date), CURRENT_DATE()) AS analysis_date FROM transactions")
    return row["analysis_date"] if row else None


def save_segmentation(lrfmc_rows, cluster_rows, metrics, optimal_k=3, iteration=0):
    ensure_runtime_schema()
    execute("DELETE FROM cluster_results")
    execute("DELETE FROM lrfmc_transformations")
    model_id = create_model_result_with_k(optimal_k, iteration)
    eval_id = create_evaluation_metrics(metrics)
    dataset_id = latest_dataset_id() or execute(
        "INSERT INTO datasets (filename, row_count) VALUES (%s, %s)",
        ("mysql_embedded_data", len(lrfmc_rows)),
    )

    execute_many(
        """
        INSERT INTO lrfmc_transformations (
          customer_id, loyalty, recency, frequency, monetary, category, category_score, lrfmc_combination
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        [
            (
                row["customer_id"],
                row["loyalty"],
                row["recency"],
                row["frequency"],
                row["monetary"],
                row["category"],
                row.get("category_score"),
                row["lrfmc_combination"],
            )
            for row in lrfmc_rows
        ],
    )
    execute_many(
        """
        INSERT INTO cluster_results (
          customer_id, id_model, id_eval, id_dataset, cluster, segment_label, file_result
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        [
            (
                row["customer_id"],
                model_id,
                eval_id,
                dataset_id,
                row["cluster"],
                row["segment_label"],
                None,
            )
            for row in cluster_rows
        ],
    )
    return {"model_id": model_id, "eval_id": eval_id, "dataset_id": dataset_id}
