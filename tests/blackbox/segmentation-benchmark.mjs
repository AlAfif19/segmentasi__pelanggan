import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { chromium } from "playwright";

const baseUrl = process.env.BENCHMARK_URL || "http://127.0.0.1:5173";
const repetitions = Number(process.env.BENCHMARK_REPETITIONS || 5);
const outputDir = path.resolve("docs/research");
const periods = [
  ["1_month", "1 bulan"],
  ["3_months", "3 bulan"],
  ["6_months", "6 bulan"],
  ["1_year", "1 tahun"],
  ["all", "Semua data"],
];

function csvCell(value) {
  const text = value === null || value === undefined ? "" : String(value);
  return `"${text.replaceAll('"', '""')}"`;
}

function toCsv(rows) {
  if (!rows.length) return "";
  const columns = Object.keys(rows[0]);
  return [
    columns.map(csvCell).join(","),
    ...rows.map((row) => columns.map((column) => csvCell(row[column])).join(",")),
  ].join("\n");
}

function aggregateSegments(profile = []) {
  const result = { "Low-Value": 0, "Medium-Value": 0, "High-Value": 0 };
  for (const row of profile) {
    result[row.segment_label] = (result[row.segment_label] || 0) + Number(row.customer_count || 0);
  }
  return result;
}

function stats(values) {
  const sorted = [...values].sort((a, b) => a - b);
  const mean = values.reduce((sum, value) => sum + value, 0) / values.length;
  const median = sorted.length % 2
    ? sorted[(sorted.length - 1) / 2]
    : (sorted[sorted.length / 2 - 1] + sorted[sorted.length / 2]) / 2;
  const variance = values.reduce((sum, value) => sum + ((value - mean) ** 2), 0) / values.length;
  return {
    minimum_seconds: Math.min(...values).toFixed(3),
    maximum_seconds: Math.max(...values).toFixed(3),
    mean_seconds: mean.toFixed(3),
    median_seconds: median.toFixed(3),
    standard_deviation_seconds: Math.sqrt(variance).toFixed(3),
  };
}

fs.mkdirSync(outputDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ acceptDownloads: true });
const page = await context.newPage();
page.setDefaultTimeout(180_000);

const rows = [];
try {
  await page.goto(baseUrl, { waitUntil: "networkidle" });
  await page.locator('input[name="username"]').fill("data_analyst");
  await page.locator('input[name="password"]').fill("password");
  await page.getByRole("button", { name: "Login" }).click();
  await page.getByRole("button", { name: "Proses Segmentasi", exact: true }).click();
  await page.getByTestId("period-select").waitFor();

  for (const [periodCode, periodLabel] of periods) {
    await page.getByTestId("period-select").selectOption(periodCode);
    for (let run = 1; run <= repetitions; run += 1) {
      const responsePromise = page.waitForResponse(
        (response) => response.url().endsWith("/api/segmentation/run") && response.request().method() === "POST",
      );
      const startedAt = performance.now();
      await page.getByTestId("start-segmentation").click();
      const response = await responsePromise;
      const payload = await response.json();
      await page.getByTestId("segmentation-status").getByText("Segmentasi selesai").waitFor();
      const durationSeconds = (performance.now() - startedAt) / 1000;
      const data = payload.data || {};
      const segmentCounts = aggregateSegments(data.cluster_profile);
      const segmentTotal = Object.values(segmentCounts).reduce((sum, value) => sum + value, 0);
      const valid = response.ok() && data.status === "completed" && segmentTotal === Number(data.rows_processed);
      rows.push({
        period_code: periodCode,
        period_label: periodLabel,
        run,
        started_at: new Date().toISOString(),
        start_date: data.period?.start_date || "",
        end_date: data.period?.end_date || "",
        transaction_count: data.period?.transaction_count || 0,
        relevant_transaction_count: data.period?.relevant_transaction_count || 0,
        rows_processed: data.rows_processed || 0,
        duration_seconds: durationSeconds.toFixed(3),
        optimal_k: data.optimal_k ?? "",
        iteration: data.k_evaluation?.find((item) => item.selected)?.iteration ?? "",
        inertia_sse: data.evaluation?.elbowmethod ?? "",
        silhouette_score: data.evaluation?.silhouette_score ?? "",
        davies_bouldin_index: data.evaluation?.dbi ?? "",
        calinski_harabasz_index: data.evaluation?.chi ?? "",
        low_value_count: segmentCounts["Low-Value"],
        medium_value_count: segmentCounts["Medium-Value"],
        high_value_count: segmentCounts["High-Value"],
        validation_status: valid ? "PASS" : "FAIL",
        error: valid ? "" : `HTTP ${response.status()}, status=${data.status}, segment_total=${segmentTotal}`,
      });
      console.log(`${periodLabel} run ${run}/${repetitions}: ${durationSeconds.toFixed(3)}s ${valid ? "PASS" : "FAIL"}`);
    }
  }

  await page.getByRole("main").getByRole("button", { name: "Lihat Hasil" }).click();
  await page.getByRole("heading", { name: "Lihat Hasil" }).waitFor();
  await page.getByRole("button", { name: "Download Result" }).click();
  const downloadPromise = page.waitForEvent("download");
  await page.getByRole("button", { name: "Download", exact: true }).click();
  const download = await downloadPromise;
  await download.saveAs(path.join(outputDir, `blackbox-${download.suggestedFilename()}`));
} finally {
  await browser.close();
}

const summaries = periods.map(([periodCode, periodLabel]) => {
  const selected = rows.filter((row) => row.period_code === periodCode);
  return {
    period_code: periodCode,
    period_label: periodLabel,
    repetitions: selected.length,
    transaction_count: selected[0]?.transaction_count || 0,
    relevant_transaction_count: selected[0]?.relevant_transaction_count || 0,
    rows_processed: selected[0]?.rows_processed || 0,
    ...stats(selected.map((row) => Number(row.duration_seconds))),
    optimal_k: selected[0]?.optimal_k ?? "",
    silhouette_score: selected[0]?.silhouette_score ?? "",
    davies_bouldin_index: selected[0]?.davies_bouldin_index ?? "",
    calinski_harabasz_index: selected[0]?.calinski_harabasz_index ?? "",
    validation_status: selected.every((row) => row.validation_status === "PASS") ? "PASS" : "FAIL",
  };
});

fs.writeFileSync(path.join(outputDir, "benchmark-segmentasi.csv"), `${toCsv(rows)}\n`);
fs.writeFileSync(path.join(outputDir, "benchmark-segmentasi-summary.csv"), `${toCsv(summaries)}\n`);
fs.writeFileSync(
  path.join(outputDir, "benchmark-segmentasi.md"),
  [
    "# Hasil Benchmark Black-Box Segmentasi",
    "",
    `Tanggal pengujian: ${new Date().toISOString()}`,
    `Lingkungan: ${os.platform()} ${os.release()}, ${os.cpus()[0]?.model || "CPU tidak diketahui"}, RAM ${Math.round(os.totalmem() / 1024 ** 3)} GB`,
    `Browser: Playwright Chromium headless`,
    `Pengulangan: ${repetitions} kali per periode`,
    `Definisi waktu: sesaat sebelum klik Start Pipeline sampai status Segmentasi selesai terlihat di UI.`,
    "",
    "| Periode | Transaksi | Relevan | Pelanggan | Rata-rata (s) | Median (s) | Min (s) | Maks (s) | SD (s) | K | Silhouette | DBI | CHI | Validasi |",
    "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ...summaries.map((row) => `| ${row.period_label} | ${row.transaction_count} | ${row.relevant_transaction_count} | ${row.rows_processed} | ${row.mean_seconds} | ${row.median_seconds} | ${row.minimum_seconds} | ${row.maximum_seconds} | ${row.standard_deviation_seconds} | ${row.optimal_k} | ${Number(row.silhouette_score).toFixed(4)} | ${Number(row.davies_bouldin_index).toFixed(4)} | ${Number(row.calinski_harabasz_index).toFixed(2)} | ${row.validation_status} |`),
    "",
    "## Catatan Metodologi",
    "",
    "- Pengujian berinteraksi melalui halaman login, navigasi, dropdown periode, tombol proses, status UI, halaman hasil, dan tombol unduh.",
    "- Tanggal akhir dibatasi sampai 7 Juni 2026. Transaksi setelah tanggal tersebut tidak digunakan.",
    "- Backend benchmark dijalankan dengan OMP_NUM_THREADS=1, OPENBLAS_NUM_THREADS=1, dan MKL_NUM_THREADS=1 agar penggunaan thread numerik konsisten.",
    "- Data transaksi aktual dimulai 6 Juli 2025, sehingga periode 1 tahun dan semua data menggunakan baris yang sama.",
    "- CSV pelanggan tidak memiliki tanggal aktif, sehingga komponen Loyalty bernilai default nol.",
    "- File CSV mentah dan ringkasan statistik disimpan di folder yang sama.",
    "",
  ].join("\n"),
);
