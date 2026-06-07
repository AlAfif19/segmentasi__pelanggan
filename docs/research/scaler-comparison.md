# Perbandingan Scaler Global

Transformasi kedua kandidat sama: `log1p` pada Frequency dan Monetary, winsorization 1%.

| Periode | Scaler | K | Silhouette | DBI | CHI | Skor periode |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 1 bulan | StandardScaler | 4 | 0.5174 | 0.7350 | 706.31 | 0.2000 |
| 1 bulan | RobustScaler | 5 | 0.5545 | 0.6552 | 677.80 | 0.8000 |
| 3 bulan | StandardScaler | 4 | 0.6009 | 0.5787 | 1074.82 | 0.8000 |
| 3 bulan | RobustScaler | 5 | 0.5474 | 0.6393 | 10633.60 | 0.2000 |
| 6 bulan | StandardScaler | 4 | 0.6686 | 0.5069 | 1255.23 | 0.8000 |
| 6 bulan | RobustScaler | 6 | 0.5924 | 0.5193 | 8317.67 | 0.2000 |
| 1 tahun | StandardScaler | 4 | 0.6965 | 0.4557 | 1334.86 | 0.8000 |
| 1 tahun | RobustScaler | 5 | 0.6092 | 0.5475 | 7133.65 | 0.2000 |

## Skor Global

- RobustScaler: 0.3500
- StandardScaler: 0.6500

**Scaler terpilih: StandardScaler**
