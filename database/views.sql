USE segmentasi_pelanggan;

CREATE OR REPLACE VIEW v_segmentation_results AS
SELECT
  cr.id_result,
  c.customer_id,
  c.name,
  l.recency,
  l.frequency,
  l.monetary,
  l.lrfmc_combination,
  cr.cluster,
  cr.segment_label,
  cr.created_at
FROM cluster_results cr
JOIN customers c ON c.customer_id = cr.customer_id
LEFT JOIN lrfmc_transformations l ON l.customer_id = cr.customer_id;
