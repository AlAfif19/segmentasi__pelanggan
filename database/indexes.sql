USE segmentasi_pelanggan;

CREATE INDEX idx_transactions_customer_date ON transactions(customer_id, transaction_date);
CREATE INDEX idx_lrfmc_customer ON lrfmc_transformations(customer_id);
CREATE INDEX idx_cluster_segment ON cluster_results(segment_label, cluster);
