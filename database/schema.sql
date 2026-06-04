CREATE DATABASE IF NOT EXISTS segmentasi_pelanggan;
USE segmentasi_pelanggan;

CREATE TABLE IF NOT EXISTS data_analysts (
  id_data_analyst INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(50) NOT NULL DEFAULT 'Data Analyst',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS logins (
  id_login INT AUTO_INCREMENT PRIMARY KEY,
  id_data_analyst INT NOT NULL,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_data_analyst) REFERENCES data_analysts(id_data_analyst)
);

CREATE TABLE IF NOT EXISTS datasets (
  id_dataset INT AUTO_INCREMENT PRIMARY KEY,
  filename VARCHAR(255) NOT NULL,
  row_count INT NOT NULL DEFAULT 0,
  loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS customers (
  customer_id VARCHAR(50) PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  active_date DATE NULL,
  category VARCHAR(100) NULL,
  monthly_fee DECIMAL(18, 2) NULL
);

CREATE TABLE IF NOT EXISTS transactions (
  id_transaction BIGINT AUTO_INCREMENT PRIMARY KEY,
  customer_id VARCHAR(50) NULL,
  customer_name VARCHAR(255) NULL,
  transaction_date DATE NOT NULL,
  transaction_type VARCHAR(100) NULL,
  payment_method VARCHAR(100) NULL,
  bank VARCHAR(255) NULL,
  raw_description TEXT NULL,
  money_in DECIMAL(18, 2) NOT NULL DEFAULT 0,
  money_out DECIMAL(18, 2) NOT NULL DEFAULT 0,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS lrfmc_transformations (
  id_lrfmc BIGINT AUTO_INCREMENT PRIMARY KEY,
  customer_id VARCHAR(50) NOT NULL,
  loyalty FLOAT NOT NULL,
  recency FLOAT NOT NULL,
  frequency INT NOT NULL,
  monetary FLOAT NOT NULL,
  category VARCHAR(100) NULL,
  category_score FLOAT NULL,
  lrfmc_combination VARCHAR(100) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS model_results (
  id_model INT AUTO_INCREMENT PRIMARY KEY,
  algorithm_name VARCHAR(100) NOT NULL DEFAULT 'K-Means Plus',
  iteration INT NOT NULL DEFAULT 0,
  segment_level_count INT NOT NULL DEFAULT 3,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS evaluation_metrics (
  id_eval INT AUTO_INCREMENT PRIMARY KEY,
  elbowmethod FLOAT NULL,
  davies_bouldin FLOAT NULL,
  calinski_harabasz FLOAT NULL,
  silhouette_avg FLOAT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cluster_results (
  id_result BIGINT AUTO_INCREMENT PRIMARY KEY,
  customer_id VARCHAR(50) NOT NULL,
  id_model INT NOT NULL,
  id_eval INT NOT NULL,
  id_dataset INT NOT NULL,
  cluster INT NOT NULL,
  segment_label VARCHAR(50) NOT NULL,
  file_result VARCHAR(255) NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
  FOREIGN KEY (id_model) REFERENCES model_results(id_model),
  FOREIGN KEY (id_eval) REFERENCES evaluation_metrics(id_eval),
  FOREIGN KEY (id_dataset) REFERENCES datasets(id_dataset)
);
