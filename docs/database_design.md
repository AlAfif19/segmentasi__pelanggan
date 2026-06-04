# Database Design

Database utama menggunakan MySQL dengan tabel:

1. `data_analysts`
2. `logins`
3. `datasets`
4. `customers`
5. `transactions`
6. `lrfmc_transformations`
7. `model_results`
8. `evaluation_metrics`
9. `cluster_results`

Kolom `lrfmc_combination` menyimpan kombinasi level LRFMC seperti `Low-Medium-High`, sedangkan `segment_label` menyimpan label akhir `Low-Value`, `Medium-Value`, atau `High-Value`.
