USE segmentasi_pelanggan;

INSERT INTO data_analysts (username, password_hash, role)
VALUES ('data_analyst', 'pbkdf2:sha256:1000000$replace_with_generated_hash', 'Data Analyst')
ON DUPLICATE KEY UPDATE role = VALUES(role);
