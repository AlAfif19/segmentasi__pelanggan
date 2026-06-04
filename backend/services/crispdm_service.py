from repositories import mysql_repository
from services.evaluation_service import calculate_metrics
from services.kmeansplus_service import run_kmeansplus
from services.lrfmc_service import build_combination
from services.preprocessing_service import run_preprocessing
from services.result_service import get_results


def _days_between(later, earlier, default=0):
    if not later or not earlier:
        return default
    return max((later - earlier).days, 0)


def _minmax(values, invert=False):
    low = min(values)
    high = max(values)
    if high == low:
        return [0.0 for _ in values]
    normalized = [(value - low) / (high - low) for value in values]
    if invert:
        return [1 - value for value in normalized]
    return normalized


def _package_score(category):
    text = str(category or "").upper()
    package_order = {
        "GRATIS": 0,
        "FREE": 0,
        "G": 0,
        "G-10MBPS": 1,
        "GH": 1,
        "PAKET 1": 1,
        "PAKET1": 1,
        "PAKET 2": 2,
        "PAKET2": 2,
        "PAKET 3": 3,
        "PAKET3": 3,
        "PAKET 4": 4,
        "PAKET4": 4,
        "PAKET 5": 5,
        "PAKET5": 5,
        "SRP": 6,
    }
    compact = "".join(text.split())
    if text in package_order:
        return float(package_order[text])
    if compact in package_order:
        return float(package_order[compact])
    for number in range(1, 8):
        if f"PAKET {number}" in text or f"PAKET{number}" in text:
            return float(number)
    if "SRP" in text:
        return 6.0
    if "GH" in text:
        return 1.0
    return 1.0


def _tariff_score(monthly_fee, avg_payment=0):
    fee = float(monthly_fee or 0)
    if fee <= 0:
        fee = float(avg_payment or 0)
    if fee <= 0:
        return 0.0
    if fee <= 100000:
        return 2.0
    if fee <= 150000:
        return 3.0
    if fee <= 200000:
        return 4.0
    if fee <= 250000:
        return 5.0
    return 6.0


def _category_score(category, monthly_fee, avg_payment=0):
    package = _package_score(category)
    tariff = _tariff_score(monthly_fee, avg_payment)
    if tariff <= 0:
        return package
    # C naik kuat ketika paket dan biaya sama-sama tinggi, tetapi mismatch tetap dimoderasi.
    return round((package * 0.55) + (tariff * 0.45), 4)


def _elbow_k(evaluation_rows):
    if len(evaluation_rows) <= 2:
        return evaluation_rows[0]["k"]
    xs = [row["k"] for row in evaluation_rows]
    ys = [row["inertia_sse"] for row in evaluation_rows]
    x1, y1 = xs[0], ys[0]
    x2, y2 = xs[-1], ys[-1]
    denom = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5 or 1
    distances = []
    for x, y in zip(xs, ys):
        distance = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1) / denom
        distances.append(distance)
    return xs[distances.index(max(distances))]


def _feature_status(code, arrow):
    if code in ["L", "F", "M", "C"]:
        return "baik" if arrow == "naik" else "rendah"
    if code == "R":
        return "baik" if arrow == "naik" else "rendah"
    return "-"


def _recommendation_detail(segment_label, metrics, overall):
    recency_gap = metrics["recency"] - overall["recency"]
    frequency_gap = metrics["frequency"] - overall["frequency"]
    monetary_gap = metrics["monetary"] - overall["monetary"]
    category_gap = metrics["category"] - overall["category"]

    if segment_label == "High-Value":
        actions = [
            "Prioritaskan program loyalitas, SLA penanganan cepat, dan penawaran upgrade yang relevan.",
            "Jaga ritme pembayaran dengan reminder ringan sebelum jatuh tempo agar nilai pelanggan tetap stabil.",
            "Tawarkan add-on atau paket premium pada pelanggan dengan monetary dan category di atas rata-rata.",
        ]
        risk = "Risiko utama adalah churn pelanggan bernilai tinggi jika kualitas layanan atau respons gangguan menurun."
    elif segment_label == "Medium-Value":
        actions = [
            "Dorong pelanggan naik kelas melalui bundling paket, promo upgrade bertahap, dan benefit pembayaran tepat waktu.",
            "Gunakan reminder pembayaran yang lebih personal untuk pelanggan dengan recency rendah atau mulai jarang transaksi.",
            "Tandai pelanggan yang frequency dan monetary-nya mendekati High-Value untuk kampanye upsell.",
        ]
        risk = "Risiko utama adalah pelanggan stagnan atau turun ke Low-Value jika tidak ada dorongan retensi."
    else:
        actions = [
            "Aktifkan kampanye reaktivasi dengan evaluasi kebutuhan layanan, diskon terbatas, atau paket yang lebih sesuai.",
            "Prioritaskan follow-up untuk pelanggan dengan recency rendah karena transaksi terakhir sudah lama.",
            "Hindari biaya promosi besar sebelum ada sinyal transaksi ulang atau respons dari pelanggan.",
        ]
        risk = "Risiko utama adalah pelanggan tidak aktif permanen atau hanya bertahan di paket rendah."

    if recency_gap < 0:
        actions.append("Tambahkan reminder lebih awal karena rata-rata recency segmen ini lebih rendah dari keseluruhan data.")
    if frequency_gap < 0:
        actions.append("Buat pemicu transaksi ulang karena frekuensi pembayaran segmen ini masih di bawah rata-rata.")
    if monetary_gap < 0:
        actions.append("Gunakan paket hemat atau bundling kecil karena kontribusi pembayaran masih di bawah rata-rata.")
    if category_gap > 0 and segment_label != "Low-Value":
        actions.append("Pertahankan kualitas layanan paket karena tier kategori segmen ini relatif tinggi.")

    return {
        "headline": actions[0],
        "actions": actions,
        "risk": risk,
    }


def _preparation_flow(data_understanding=None, model_config=None):
    data_understanding = data_understanding or {}
    duplicates = data_understanding.get("duplicates", {})
    model_config = model_config or {}
    return [
        {
            "title": "Standarisasi Kolom",
            "description": "Kolom Excel master dan mutasi diseragamkan menjadi struktur MySQL.",
            "processes": ["NOPEL -> customer_id", "NAMA PELANGGAN -> name", "PAKET -> category", "TOTAL TARIF -> monthly_fee"],
            "output": "customers dan transactions siap dibaca pipeline.",
        },
        {
            "title": "Pembersihan Nilai",
            "description": "Tanggal, nilai uang, teks nama pelanggan, dan nilai kosong dibersihkan.",
            "processes": ["Parsing tanggal aktif dan transaksi", "Konversi uang masuk/keluar", "Trim teks kategori dan nama"],
            "output": "Nilai numerik dan tanggal valid untuk agregasi.",
        },
        {
            "title": "Validasi Struktur",
            "description": "Sistem mengecek missing value dan duplikasi dasar sebelum modelling.",
            "processes": [
                f"Duplikasi NOPEL: {duplicates.get('customer_id', 0)}",
                f"Duplikasi nama: {duplicates.get('name', 0)}",
                f"Transaksi relevan: {data_understanding.get('relevant_transactions', 0)}",
            ],
            "output": "Kualitas data awal tercatat.",
        },
        {
            "title": "Filter Transaksi Relevan",
            "description": "Hanya transaksi pembayaran/tagihan dengan money_in positif yang dipakai untuk LRFMC.",
            "processes": ["money_in > 0", "transaction_date valid", "jenis transaksi mengandung TAGIHAN/PEMBAYARAN/BAYAR"],
            "output": "Transaksi pembayaran pelanggan terpilih.",
        },
        {
            "title": "Agregasi Pelanggan",
            "description": "Transaksi digabung per pelanggan untuk membentuk frequency, monetary, dan last payment.",
            "processes": ["COUNT pembayaran -> F", "SUM uang masuk -> M", "MAX tanggal pembayaran -> R"],
            "output": "Satu baris fitur per pelanggan.",
        },
        {
            "title": "Feature Engineering LRFMC",
            "description": "L, R, F, M, dan C dibentuk dari master pelanggan dan transaksi.",
            "processes": ["L dari lama aktif", "R dari jarak pembayaran terakhir", "C dari paket + biaya bulanan/avg payment"],
            "output": "Dataset LRFMC lengkap.",
        },
        {
            "title": "Scaling dan Outlier",
            "description": "Fitur numerik dikondisikan agar jarak Euclidean K-Means stabil.",
            "processes": [
                f"Transform: {model_config.get('transform', '-')}",
                f"Scaler: {model_config.get('scaler', '-')}",
                f"Winsor: {model_config.get('winsor', '-')}",
            ],
            "output": "Matriks fitur siap clustering.",
        },
        {
            "title": "Evaluasi K dan Model Final",
            "description": "K-Means++ diuji pada beberapa nilai K, lalu konfigurasi terbaik dipilih.",
            "processes": ["Elbow inertia", "Silhouette", "Davies-Bouldin", "Calinski-Harabasz"],
            "output": f"K optimal: {model_config.get('optimal_k', '-')}",
        },
    ]


def _run_mysql_segmentation():
    source_rows = mysql_repository.get_lrfmc_source_rows()
    if not source_rows:
        return None

    analysis_date = mysql_repository.get_analysis_date()
    loyalty_days = [
        _days_between(analysis_date, row["active_date"], default=0)
        for row in source_rows
    ]
    observed_recency = [
        _days_between(analysis_date, row["last_transaction"], default=None)
        for row in source_rows
        if row["last_transaction"]
    ]
    recency_fill = (max(observed_recency) + 30) if observed_recency else 999
    recency_days = [
        _days_between(analysis_date, row["last_transaction"], default=recency_fill)
        for row in source_rows
    ]
    frequencies = [float(row["frequency"] or 0) for row in source_rows]
    monetary = [float(row["monetary"] or 0) for row in source_rows]
    avg_payments = [
        (float(row["monetary"] or 0) / float(row["frequency"] or 1)) if float(row["frequency"] or 0) > 0 else 0.0
        for row in source_rows
    ]
    category_scores = [
        _category_score(row["category"], row.get("monthly_fee"), avg_payments[index])
        for index, row in enumerate(source_rows)
    ]

    loyalty_norm = _minmax(loyalty_days)
    recency_scores = _minmax(recency_days, invert=True)
    frequency_norm = _minmax(frequencies)
    monetary_norm = _minmax(monetary)
    category_norm = _minmax(category_scores)

    lrfmc_rows = []
    model_features = []
    business_features = []
    raw_lrfmc = []
    for index, row in enumerate(source_rows):
        lrfmc_combination = build_combination(
            recency_scores[index],
            frequency_norm[index],
            monetary_norm[index],
        )
        lrfmc_rows.append(
            {
                "customer_id": row["customer_id"],
                "loyalty": float(loyalty_days[index]),
                "recency": float(recency_scores[index]),
                "frequency": int(frequencies[index]),
                "monetary": float(monetary[index]),
                "category": row["category"],
                "monthly_fee": float(row.get("monthly_fee") or 0),
                "category_score": float(category_scores[index]),
                "lrfmc_combination": lrfmc_combination,
            }
        )
        model_features.append(
            [
                float(loyalty_days[index]),
                float(recency_scores[index]),
                frequencies[index],
                monetary[index],
                category_scores[index],
            ]
        )
        business_features.append(
            [loyalty_norm[index], recency_scores[index], frequency_norm[index], monetary_norm[index], category_norm[index]]
        )
        raw_lrfmc.append(
            {
                "customer_id": row["customer_id"],
                "loyalty": float(loyalty_days[index]),
                "recency": float(recency_scores[index]),
                "frequency": frequencies[index],
                "monetary": monetary[index],
                "category": category_scores[index],
            }
        )

    try:
        import numpy as np
        from sklearn.cluster import KMeans
        from sklearn.decomposition import PCA
        from sklearn.metrics import calinski_harabasz_score, davies_bouldin_score, silhouette_score
        from sklearn.preprocessing import RobustScaler, StandardScaler

        base_matrix = np.array(model_features, dtype=float)
        candidate_configs = [
            {"name": "baseline_standard", "transform": "raw", "scaler": "StandardScaler", "winsor": 0.01},
            {"name": "logfm_standard", "transform": "log1p_frequency_monetary", "scaler": "StandardScaler", "winsor": 0.01},
            {"name": "logfm_robust", "transform": "log1p_frequency_monetary", "scaler": "RobustScaler", "winsor": 0.01},
            {"name": "raw_robust", "transform": "raw", "scaler": "RobustScaler", "winsor": 0.01},
            {"name": "logfm_standard_winsor2", "transform": "log1p_frequency_monetary", "scaler": "StandardScaler", "winsor": 0.02},
        ]
        evaluated_configs = []
        max_k = min(10, len(base_matrix) - 1)
        for config in candidate_configs:
            model_ready = base_matrix.copy()
            if config["transform"] == "log1p_frequency_monetary":
                model_ready[:, 2] = np.log1p(model_ready[:, 2])
                model_ready[:, 3] = np.log1p(model_ready[:, 3])
            winsor = config["winsor"]
            for col_idx in range(model_ready.shape[1]):
                lower = np.quantile(model_ready[:, col_idx], winsor)
                upper = np.quantile(model_ready[:, col_idx], 1 - winsor)
                if lower < upper:
                    model_ready[:, col_idx] = np.clip(model_ready[:, col_idx], lower, upper)
            scaler = RobustScaler() if config["scaler"] == "RobustScaler" else StandardScaler()
            scaled_candidate = scaler.fit_transform(model_ready)
            evaluation_rows_candidate = []
            fitted_by_k = {}
            for k in range(2, max_k + 1):
                candidate = KMeans(n_clusters=k, init="k-means++", random_state=42, n_init=30)
                candidate_labels = candidate.fit_predict(scaled_candidate)
                fitted_by_k[k] = (candidate, candidate_labels)
                evaluation_rows_candidate.append(
                    {
                        "k": k,
                        "inertia_sse": float(candidate.inertia_),
                        "silhouette_score": float(silhouette_score(scaled_candidate, candidate_labels)),
                        "davies_bouldin_index": float(davies_bouldin_score(scaled_candidate, candidate_labels)),
                        "calinski_harabasz_index": float(calinski_harabasz_score(scaled_candidate, candidate_labels)),
                        "iteration": int(candidate.n_iter_),
                    }
                )
            selected_k = _elbow_k(evaluation_rows_candidate)
            selected_model, selected_labels = fitted_by_k[selected_k]
            evaluated_configs.append(
                {
                    **config,
                    "optimal_k": selected_k,
                    "model": selected_model,
                    "labels": selected_labels,
                    "scaled": scaled_candidate,
                    "evaluation_rows": evaluation_rows_candidate,
                    "inertia_sse": float(selected_model.inertia_),
                    "silhouette_score": float(silhouette_score(scaled_candidate, selected_labels)),
                    "davies_bouldin_index": float(davies_bouldin_score(scaled_candidate, selected_labels)),
                    "calinski_harabasz_index": float(calinski_harabasz_score(scaled_candidate, selected_labels)),
                    "iteration": int(selected_model.n_iter_),
                }
            )

        sil_values = [row["silhouette_score"] for row in evaluated_configs]
        dbi_values = [row["davies_bouldin_index"] for row in evaluated_configs]
        chi_values = [row["calinski_harabasz_index"] for row in evaluated_configs]
        min_sil, max_sil = min(sil_values), max(sil_values)
        min_dbi, max_dbi = min(dbi_values), max(dbi_values)
        min_chi, max_chi = min(chi_values), max(chi_values)

        def norm(value, low, high, invert=False):
            normalized = 0.5 if high == low else (value - low) / (high - low)
            return 1 - normalized if invert else normalized

        for row in evaluated_configs:
            row["selection_score"] = (
                norm(row["silhouette_score"], min_sil, max_sil) * 0.45
                + norm(row["davies_bouldin_index"], min_dbi, max_dbi, invert=True) * 0.35
                + norm(row["calinski_harabasz_index"], min_chi, max_chi) * 0.20
            )

        best_config = max(evaluated_configs, key=lambda row: row["selection_score"])
        optimal_k = best_config["optimal_k"]
        model = best_config["model"]
        labels = best_config["labels"]
        scaled = best_config["scaled"]
        evaluation_rows = [
            {**row, "selected": int(row["k"]) == int(optimal_k)}
            for row in best_config["evaluation_rows"]
        ]
        raw_metrics = {
            "k_optimal_elbow": optimal_k,
            "elbowmethod": float(model.inertia_),
            "dbi": float(davies_bouldin_score(scaled, labels)),
            "chi": float(calinski_harabasz_score(scaled, labels)),
            "silhouette_score": float(silhouette_score(scaled, labels)),
        }
        iteration = int(model.n_iter_)
        pca_2d = PCA(n_components=2, random_state=42).fit_transform(scaled)
        pca_3d = PCA(n_components=3, random_state=42).fit_transform(scaled)
        model_config = {
            "name": best_config["name"],
            "transform": best_config["transform"],
            "scaler": best_config["scaler"],
            "winsor": f"{int(best_config['winsor'] * 100)}%-{int((1 - best_config['winsor']) * 100)}%",
            "optimal_k": optimal_k,
            "selection_score": best_config["selection_score"],
        }
        model_candidates = [
            {
                "name": row["name"],
                "transform": row["transform"],
                "scaler": row["scaler"],
                "winsor": f"{int(row['winsor'] * 100)}%-{int((1 - row['winsor']) * 100)}%",
                "optimal_k": row["optimal_k"],
                "silhouette_score": row["silhouette_score"],
                "davies_bouldin_index": row["davies_bouldin_index"],
                "calinski_harabasz_index": row["calinski_harabasz_index"],
                "selection_score": row["selection_score"],
                "selected": row["name"] == best_config["name"],
            }
            for row in evaluated_configs
        ]
    except Exception:
        scores = [feature[2] + feature[3] for feature in business_features]
        sorted_scores = sorted(scores)
        low_boundary = sorted_scores[int(len(sorted_scores) * 0.33)]
        high_boundary = sorted_scores[int(len(sorted_scores) * 0.66)]
        labels = [
            0 if score <= low_boundary else 1 if score <= high_boundary else 2
            for score in scores
        ]
        raw_metrics = {
            "k_optimal_elbow": 3,
            "elbowmethod": None,
            "dbi": None,
            "chi": None,
            "silhouette_score": None,
        }
        iteration = 0
        optimal_k = 3
        evaluation_rows = []
        pca_2d = [[feature[0], feature[2]] for feature in business_features]
        pca_3d = [[feature[0], feature[2], feature[3]] for feature in business_features]
        model_config = {"name": "fallback_business_score", "transform": "minmax_business_score", "scaler": "-", "winsor": "-", "optimal_k": optimal_k}
        model_candidates = []

    cluster_scores = {}
    for label, feature in zip(labels, business_features):
        business_score = (feature[0] + feature[1] + feature[2] + feature[3] + feature[4]) / 5
        cluster_scores.setdefault(int(label), []).append(business_score)
    ranked_clusters = sorted(cluster_scores, key=lambda cluster: sum(cluster_scores[cluster]) / len(cluster_scores[cluster]))
    cluster_to_segment = {}
    for rank, cluster in enumerate(ranked_clusters):
        ratio = rank / max(len(ranked_clusters) - 1, 1)
        if ratio <= 0.34:
            cluster_to_segment[cluster] = "Low-Value"
        elif ratio <= 0.67:
            cluster_to_segment[cluster] = "Medium-Value"
        else:
            cluster_to_segment[cluster] = "High-Value"

    feature_specs = [
        ("loyalty", "L", "Loyalty (L)", "L naik = loyalitas lebih lama."),
        ("recency", "R", "Recency (R)", "R naik = transaksi lebih baru."),
        ("frequency", "F", "Frequency (F)", "F naik = transaksi lebih sering."),
        ("monetary", "M", "Monetary (M)", "M naik = kontribusi lebih besar."),
        ("category", "C", "Category (C)", "C naik = kategori paket lebih tinggi."),
    ]
    overall_lrfmc = {
        key: sum(row[key] for row in raw_lrfmc) / len(raw_lrfmc)
        for key, _, _, _ in feature_specs
    }

    cluster_rows = []
    scatter_2d = []
    scatter_3d = []
    for idx, (row, label) in enumerate(zip(lrfmc_rows, labels)):
        cluster_rows.append(
            {
                "customer_id": row["customer_id"],
                "cluster": int(label),
                "segment_label": cluster_to_segment[int(label)],
            }
        )
        scatter_2d.append(
            {
                "customer_id": row["customer_id"],
                "name": source_rows[idx].get("name"),
                "cluster": int(label),
                "segment_label": cluster_to_segment[int(label)],
                "x": float(pca_2d[idx][0]),
                "y": float(pca_2d[idx][1]),
            }
        )
        scatter_3d.append(
            {
                "customer_id": row["customer_id"],
                "name": source_rows[idx].get("name"),
                "cluster": int(label),
                "segment_label": cluster_to_segment[int(label)],
                "x": float(pca_3d[idx][0]),
                "y": float(pca_3d[idx][1]),
                "z": float(pca_3d[idx][2]),
            }
        )

    profile = []
    for cluster in sorted(set(int(label) for label in labels)):
        indexes = [idx for idx, label in enumerate(labels) if int(label) == cluster]
        metrics = {
            "loyalty": sum(raw_lrfmc[idx]["loyalty"] for idx in indexes) / len(indexes),
            "recency": sum(raw_lrfmc[idx]["recency"] for idx in indexes) / len(indexes),
            "frequency": sum(raw_lrfmc[idx]["frequency"] for idx in indexes) / len(indexes),
            "monetary": sum(raw_lrfmc[idx]["monetary"] for idx in indexes) / len(indexes),
            "category": sum(raw_lrfmc[idx]["category"] for idx in indexes) / len(indexes),
        }
        segment_label = cluster_to_segment[cluster]
        recommendation_detail = _recommendation_detail(segment_label, metrics, overall_lrfmc)
        arrow_summary = {}
        for key, code, _, _ in feature_specs:
            arrow = "naik" if metrics[key] >= overall_lrfmc[key] else "turun"
            arrow_summary[code] = {
                "value": round(metrics[key], 2),
                "arrow": arrow,
                "status": _feature_status(code, arrow),
            }
        profile.append(
            {
                "cluster": cluster,
                "segment_label": segment_label,
                "customer_count": len(indexes),
                **metrics,
                "business_recommendation": recommendation_detail["headline"],
                "recommendation_detail": recommendation_detail,
                "arrow_summary": arrow_summary,
            }
        )

    segment_order = ["High-Value", "Medium-Value", "Low-Value"]
    feature_overview = []
    for key, code, label, note in feature_specs:
        segment_values = []
        for segment_label in segment_order:
            matching_profiles = [item for item in profile if item["segment_label"] == segment_label]
            if not matching_profiles:
                continue
            total_customers = sum(item["customer_count"] for item in matching_profiles) or 1
            value = sum(item[key] * item["customer_count"] for item in matching_profiles) / total_customers
            arrow = "naik" if value >= overall_lrfmc[key] else "turun"
            segment_values.append(
                {
                    "segment": segment_label,
                    "value": value,
                    "arrow": arrow,
                    "status": _feature_status(code, arrow),
                }
            )
        feature_overview.append(
            {
                "feature": label,
                "code": code,
                "mean": overall_lrfmc[key],
                "direction": note,
                "segments": segment_values,
            }
        )

    saved = mysql_repository.save_segmentation(lrfmc_rows, cluster_rows, raw_metrics, optimal_k=optimal_k, iteration=iteration)
    return {
        "rows_processed": len(lrfmc_rows),
        "evaluation": raw_metrics,
        "k_evaluation": evaluation_rows,
        "optimal_k": optimal_k,
        "model_config": model_config,
        "model_candidates": model_candidates,
        "cluster_profile": profile,
        "scatter_2d": scatter_2d[:250],
        "scatter_3d": scatter_3d[:250],
        "feature_overview": feature_overview,
        "saved": saved,
    }


def run_pipeline():
    mysql_result = None
    database_ready = mysql_repository.is_ready()
    if database_ready:
        mysql_result = _run_mysql_segmentation()
    data_understanding = mysql_repository.get_data_understanding() if database_ready else {}
    result = get_results(page=1, per_page=1)
    logs = [
        "Business Understanding",
        "Data Understanding",
        *run_preprocessing(),
        *run_kmeansplus()["steps"],
        "Calculating evaluation metrics",
        "Saving clustering, labeling, and evaluation",
        "Deployment result ready",
    ]
    return {
        "status": "completed" if mysql_result else "database_unavailable" if not database_ready else "no_data",
        "logs": logs,
        "evaluation": mysql_result["evaluation"] if mysql_result else calculate_metrics(),
        "k_evaluation": mysql_result["k_evaluation"] if mysql_result else [],
        "optimal_k": mysql_result["optimal_k"] if mysql_result else None,
        "model_config": mysql_result["model_config"] if mysql_result else {},
        "model_candidates": mysql_result["model_candidates"] if mysql_result else [],
        "cluster_profile": mysql_result["cluster_profile"] if mysql_result else [],
        "scatter_2d": mysql_result["scatter_2d"] if mysql_result else [],
        "scatter_3d": mysql_result["scatter_3d"] if mysql_result else [],
        "feature_overview": mysql_result["feature_overview"] if mysql_result else [],
        "data_understanding": data_understanding,
        "preparation_flow": _preparation_flow(data_understanding, mysql_result["model_config"] if mysql_result else {}),
        "segment_levels": ["Low", "Medium", "High"],
        "source": "mysql",
        "rows_processed": mysql_result["rows_processed"] if mysql_result else result["summary"].get("customers", 0),
        "database_ready": database_ready,
    }
