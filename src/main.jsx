import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import { AnimatePresence, motion } from "framer-motion";
import {
  BarChart3,
  CheckCircle2,
  ChevronRight,
  Database,
  Download,
  FileJson,
  FileSpreadsheet,
  LayoutDashboard,
  Loader2,
  LogIn,
  LogOut,
  PanelLeftClose,
  PanelLeftOpen,
  Play,
  ShieldCheck,
  Workflow,
  X,
} from "lucide-react";
import "./styles.css";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:5000/api";
const PROCESS_STATE_KEY = "segmentationProcessStateV2";
const LEGACY_PROCESS_STATE_KEY = "segmentationProcessState";

const pipelineSteps = [
  "Business Understanding",
  "Data Understanding",
  "Cleaning missing values",
  "Removing duplicate data",
  "Transforming numeric data",
  "Calculating LRFMC",
  "Normalizing data",
  "Preparing 3 segment levels: Low, Medium, High",
  "Initializing first centroid",
  "Calculating D(x)^2",
  "Calculating P(x)",
  "Selecting new centroid",
  "Assigning data to centroid",
  "Updating centroid",
  "Checking convergence",
  "Calculating Elbow, DBI, CHI, Silhouette",
  "Saving clustering, labeling, and evaluation",
  "Deployment result ready",
];

const nav = [
  ["dashboard", "Dashboard", LayoutDashboard],
  ["data", "Data Tertanam", Database],
  ["process", "Proses Segmentasi", Workflow],
  ["result", "Lihat Hasil", BarChart3],
];

function cx(...classes) {
  return classes.filter(Boolean).join(" ");
}

function fmt(value) {
  if (value === null || value === undefined || value === "") return "-";
  if (Number.isFinite(Number(value))) return new Intl.NumberFormat("id-ID").format(Number(value));
  return value;
}

function decimal(value) {
  if (value === null || value === undefined || value === "") return "-";
  return Number(value).toFixed(3);
}

function pct(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) return "-";
  return `${Math.round(Number(value) * 100)}%`;
}

async function api(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(payload.message || "Request gagal");
  return payload.data ?? payload;
}

async function downloadApi(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    throw new Error(payload.message || "Download gagal");
  }
  const blob = await response.blob();
  const disposition = response.headers.get("Content-Disposition") || "";
  const filenameMatch = disposition.match(/filename="?([^"]+)"?/i);
  return {
    blob,
    filename: filenameMatch?.[1] || "segmentation_result.csv",
  };
}

function useApi(path, fallback, refreshKey = 0) {
  const [state, setState] = useState({ loading: true, error: "", data: fallback });
  useEffect(() => {
    let active = true;
    setState((current) => ({ ...current, loading: true, error: "" }));
    api(path)
      .then((data) => active && setState({ loading: false, error: "", data }))
      .catch((error) => active && setState({ loading: false, error: error.message, data: fallback }));
    return () => {
      active = false;
    };
  }, [path, refreshKey]);
  return state;
}

function Badge({ children, tone = "slate" }) {
  const tones = {
    slate: "border-slate-200 bg-slate-50 text-slate-700",
    green: "border-emerald-200 bg-emerald-50 text-emerald-700",
    amber: "border-amber-200 bg-amber-50 text-amber-700",
    red: "border-red-200 bg-red-50 text-red-700",
    blue: "border-blue-200 bg-blue-50 text-blue-700",
  };
  return <span className={cx("inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-semibold", tones[tone])}>{children}</span>;
}

function Button({ children, variant = "primary", className = "", ...props }) {
  const variants = {
    primary: "bg-slate-950 text-white hover:bg-slate-800",
    secondary: "border border-slate-200 bg-white text-slate-800 hover:bg-slate-50",
    ghost: "text-slate-600 hover:bg-slate-100 hover:text-slate-950",
    danger: "border border-red-200 bg-white text-red-700 hover:bg-red-50",
  };
  return (
    <button
      className={cx("inline-flex h-10 items-center justify-center gap-2 rounded-md px-4 text-sm font-semibold transition focus:outline-none focus:ring-2 focus:ring-slate-300 disabled:cursor-not-allowed disabled:opacity-60", variants[variant], className)}
      {...props}
    >
      {children}
    </button>
  );
}

function Card({ children, className = "" }) {
  return <section className={cx("min-w-0 rounded-lg border border-slate-200 bg-white p-5 shadow-soft", className)}>{children}</section>;
}

function CardTitle({ title, subtitle, action }) {
  return (
    <div className="mb-5 flex flex-wrap items-start justify-between gap-3">
      <div className="min-w-0">
        <h2 className="break-words text-base font-semibold text-slate-950">{title}</h2>
        {subtitle ? <p className="mt-1 break-words text-sm text-slate-500">{subtitle}</p> : null}
      </div>
      {action}
    </div>
  );
}

function Field({ label, children }) {
  return (
    <label className="grid gap-1.5">
      <span className="text-xs font-semibold text-slate-500">{label}</span>
      {children}
    </label>
  );
}

function Input(props) {
  return <input className="h-10 w-full rounded-md border border-slate-200 bg-white px-3 text-sm outline-none transition focus:border-slate-400 focus:ring-2 focus:ring-slate-100" {...props} />;
}

function Select(props) {
  return <select className="h-10 w-full rounded-md border border-slate-200 bg-white px-3 text-sm outline-none transition focus:border-slate-400 focus:ring-2 focus:ring-slate-100" {...props} />;
}

function App() {
  const [isLoggedIn, setLoggedIn] = useState(() => sessionStorage.getItem("isLoggedIn") === "true");
  const [page, setPage] = useState("dashboard");
  const [sidebarCollapsed, setSidebarCollapsed] = useState(() => sessionStorage.getItem("sidebarCollapsed") === "true");
  const [refreshKey, setRefreshKey] = useState(0);
  const [processState, setProcessState] = useState(() => {
    try {
      sessionStorage.removeItem(LEGACY_PROCESS_STATE_KEY);
      return JSON.parse(sessionStorage.getItem(PROCESS_STATE_KEY) || "null") || { running: false, done: 0, result: null, error: "" };
    } catch {
      return { running: false, done: 0, result: null, error: "" };
    }
  });

  function updateProcessState(updater) {
    setProcessState((current) => {
      const next = typeof updater === "function" ? updater(current) : updater;
      const persisted = { ...next, running: false };
      sessionStorage.setItem(PROCESS_STATE_KEY, JSON.stringify(persisted));
      return next;
    });
  }

  function toggleSidebar() {
    setSidebarCollapsed((current) => {
      const next = !current;
      sessionStorage.setItem("sidebarCollapsed", String(next));
      return next;
    });
  }

  if (!isLoggedIn) return <Login onLogin={() => setLoggedIn(true)} />;

  return (
    <div className="min-h-screen bg-slate-50 text-slate-950">
      <div className={cx("grid min-h-screen transition-[grid-template-columns]", sidebarCollapsed ? "lg:grid-cols-[76px_1fr]" : "lg:grid-cols-[280px_1fr]")}>
        <Sidebar
          page={page}
          collapsed={sidebarCollapsed}
          onToggle={toggleSidebar}
          onNavigate={setPage}
          onLogout={async () => {
            try {
              await api("/auth/logout", { method: "POST" });
            } catch {
              // The UI session should still end even if the network request fails.
            }
            sessionStorage.removeItem("isLoggedIn");
            setLoggedIn(false);
          }}
        />
        <main className="min-w-0 p-4 sm:p-6 lg:p-8">
          <AnimatePresence mode="wait">
            <motion.div className="min-w-0" key={page} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -8 }} transition={{ duration: 0.2 }}>
              {page === "dashboard" && <Dashboard setPage={setPage} refreshKey={refreshKey} />}
              {page === "data" && <DataEmbedded refreshKey={refreshKey} />}
              {page === "process" && <Process setPage={setPage} processState={processState} setProcessState={updateProcessState} onRefresh={() => setRefreshKey((key) => key + 1)} />}
              {page === "result" && <Result refreshKey={refreshKey} />}
            </motion.div>
          </AnimatePresence>
        </main>
      </div>
    </div>
  );
}

function Login({ onLogin }) {
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  return (
    <div className="grid min-h-screen place-items-center bg-white p-6">
      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="w-full max-w-md rounded-lg border border-slate-200 bg-white p-7 shadow-soft">
        <div className="mb-6 flex items-center gap-3">
          <div className="grid h-11 w-11 place-items-center rounded-md bg-slate-950 text-sm font-bold text-white">SP</div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-slate-950">Sistem Segmentasi Pelanggan</h1>
            <p className="text-sm text-slate-500">Login Data Analyst</p>
          </div>
        </div>
        {error ? <Alert tone="red">{error}</Alert> : null}
        <form
          className="grid gap-4"
          onSubmit={async (event) => {
            event.preventDefault();
            setLoading(true);
            setError("");
            const form = new FormData(event.currentTarget);
            try {
              await api("/auth/login", {
                method: "POST",
                body: JSON.stringify({ username: form.get("username"), password: form.get("password") }),
              });
              sessionStorage.setItem("isLoggedIn", "true");
              onLogin();
            } catch (err) {
              setError(err.message);
            } finally {
              setLoading(false);
            }
          }}
        >
          <Field label="Data Analyst name">
            <Input name="username" autoComplete="username" required />
          </Field>
          <Field label="Password">
            <Input name="password" type="password" autoComplete="current-password" required />
          </Field>
          <Button type="submit" disabled={loading}>
            {loading ? <Loader2 size={16} className="animate-spin" /> : <LogIn size={16} />}
            Login
          </Button>
        </form>
      </motion.div>
    </div>
  );
}

function Sidebar({ page, collapsed, onToggle, onNavigate, onLogout }) {
  return (
    <aside className={cx("border-b border-slate-200 bg-white p-4 transition-all lg:sticky lg:top-0 lg:h-screen lg:border-b-0 lg:border-r", collapsed ? "lg:p-3" : "lg:p-5")}>
      <div className={cx("mb-6 flex items-center gap-3", collapsed && "lg:justify-center")}>
        <div className="grid h-10 w-10 place-items-center rounded-md bg-slate-950 text-sm font-bold text-white">SP</div>
        <div className={cx(collapsed && "lg:hidden")}>
          <p className="font-bold leading-tight text-slate-950">Segmentasi Pelanggan</p>
          <p className="text-xs text-slate-500">CRISP-DM + K-Means Plus</p>
        </div>
        <Button
          variant="primary"
          className={cx("ml-auto h-11 w-11 shrink-0 px-0 shadow-sm", collapsed && "lg:hidden")}
          onClick={onToggle}
          aria-label="Tutup sidebar"
          title="Tutup sidebar"
        >
          <PanelLeftClose size={24} strokeWidth={2.4} />
        </Button>
      </div>
      <nav className="grid gap-1">
        {nav.map(([key, label, Icon]) => (
          <button key={key} onClick={() => onNavigate(key)} className={cx("flex h-10 items-center gap-3 rounded-md px-3 text-left text-sm font-semibold transition", collapsed && "lg:justify-center lg:px-0", page === key ? "bg-slate-950 text-white" : "text-slate-600 hover:bg-slate-100 hover:text-slate-950")} title={collapsed ? label : undefined}>
            <Icon size={17} />
            <span className={cx(collapsed && "lg:hidden")}>{label}</span>
          </button>
        ))}
      </nav>
      {collapsed ? (
        <Button variant="secondary" className="mt-4 hidden h-10 w-full border-slate-300 px-0 shadow-sm lg:flex" onClick={onToggle} aria-label="Buka sidebar" title="Buka sidebar">
          <PanelLeftOpen size={18} />
        </Button>
      ) : null}
      {collapsed ? (
        <div className="mt-6 flex justify-center lg:absolute lg:bottom-5 lg:left-0 lg:right-0">
          <button
            className="grid h-11 w-11 place-items-center rounded-md bg-transparent text-red-600 transition hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-red-200"
            onClick={onLogout}
            aria-label="Logout"
          >
            <svg aria-hidden="true" viewBox="0 0 24 24" className="h-6 w-6" fill="none" stroke="#dc2626" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
              <path d="M16 17l5-5-5-5" />
              <path d="M21 12H9" />
            </svg>
          </button>
        </div>
      ) : (
        <div className="mt-6 rounded-lg border border-slate-200 bg-slate-50 p-3 lg:absolute lg:bottom-5 lg:left-5 lg:right-5">
          <div className="flex items-center justify-between gap-3">
            <div>
            <p className="text-sm font-bold text-slate-950">Data Analyst</p>
            <p className="text-xs text-slate-500">Session aktif</p>
            </div>
            <Button variant="danger" className="h-10 shrink-0 px-3" onClick={onLogout} title="Logout">
              <LogOut size={16} strokeWidth={2.4} />
              <span>Logout</span>
            </Button>
          </div>
        </div>
      )}
    </aside>
  );
}

function Header({ title, subtitle, action }) {
  return (
    <div className="mb-6 flex flex-wrap items-start justify-between gap-4">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-950">{title}</h1>
        <p className="mt-1 text-sm text-slate-500">{subtitle}</p>
      </div>
      {action}
    </div>
  );
}

function Alert({ children, tone = "slate" }) {
  const color = tone === "red" ? "border-red-200 bg-red-50 text-red-700" : "border-slate-200 bg-slate-50 text-slate-600";
  return <div className={cx("mb-4 rounded-md border px-3 py-2 text-sm font-medium", color)}>{children}</div>;
}

function LoadingCard() {
  return (
    <Card>
      <div className="flex items-center gap-2 text-sm text-slate-500">
        <Loader2 size={16} className="animate-spin" />
        Memuat data dari API...
      </div>
    </Card>
  );
}

function Metric({ label, value, note, compact }) {
  return (
    <Card className="p-4">
      <p className="text-xs font-semibold uppercase text-slate-500">{label}</p>
      <p className={cx("mt-2 font-bold tracking-tight text-slate-950", compact ? "text-2xl" : "text-3xl")}>{value}</p>
      <p className="mt-1 text-sm text-slate-500">{note}</p>
    </Card>
  );
}

function Dashboard({ setPage, refreshKey }) {
  const { loading, error, data } = useApi("/dashboard/", { summary: {}, evaluation: {} }, refreshKey);
  const summary = data.summary || {};
  return (
    <>
      <Header title="Dashboard" subtitle="Ringkasan data, model, dan hasil segmentasi terakhir." action={<Badge tone={summary.customers ? "green" : "amber"}>{summary.customers ? "Data MySQL tersedia" : "Menunggu data MySQL"}</Badge>} />
      {error ? <Alert tone="red">{error}</Alert> : null}
      {loading ? <LoadingCard /> : null}
      <div className="grid gap-4 md:grid-cols-3">
        <Metric label="Total Pelanggan" value={fmt(summary.customers || 0)} note="Dari tabel customers" />
        <Metric label="Total Mutasi" value={fmt(summary.transactions || 0)} note="Dari tabel transactions" />
        <Metric label="Algoritma" value={summary.algorithm || "K-Means Plus"} note={`Level segmen: ${(summary.segment_levels || ["Low", "Medium", "High"]).join(", ")}`} compact />
      </div>
      <div className="mt-4 grid gap-4 xl:grid-cols-[1fr_1.2fr]">
        <Card>
          <CardTitle title="Tahapan PRD" subtitle="Alur fitur utama sistem." />
          <div className="grid gap-3">
            {[
              ["Login", "Autentikasi Data Analyst", ShieldCheck, "dashboard"],
              ["Data Tertanam", "Preview sumber data dari MySQL", Database, "data"],
              ["Proses Segmentasi", "Pipeline CRISP-DM dan K-Means Plus", Workflow, "process"],
              ["Lihat Hasil", "Grafik, karakteristik cluster, dan tabel hasil", BarChart3, "result"],
            ].map(([title, text, Icon, target]) => (
              <button key={title} onClick={() => setPage(target)} className="flex items-center gap-3 rounded-md border border-slate-200 bg-white p-3 text-left transition hover:border-slate-300 hover:bg-slate-50">
                <div className="grid h-9 w-9 place-items-center rounded-md bg-slate-100 text-slate-700">
                  <Icon size={17} />
                </div>
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-bold text-slate-950">{title}</p>
                  <p className="text-xs text-slate-500">{text}</p>
                </div>
                <ChevronRight size={16} className="text-slate-400" />
              </button>
            ))}
          </div>
        </Card>
        <Card>
          <CardTitle title="Evaluasi Model Terakhir" subtitle="Data diambil dari tabel evaluation_metrics." />
          <EvaluationTable evaluation={data.evaluation} />
        </Card>
      </div>
    </>
  );
}

function DataEmbedded({ refreshKey }) {
  const { loading, error, data } = useApi("/data/embedded", { summary: {}, raw_files: [], database_ready: false }, refreshKey);
  const summary = data.summary || {};
  const understanding = data.data_understanding || {};
  const distributions = understanding.distributions || {};
  const preview = data.preview || { customers: [], transactions: [] };
  return (
    <>
      <Header title="Data Tertanam" subtitle="Sumber data pelanggan dan mutasi transaksi yang disiapkan di MySQL." action={<Badge tone={data.database_ready ? "green" : "red"}>{data.database_ready ? "MySQL tersambung" : "MySQL belum tersambung"}</Badge>} />
      {error ? <Alert tone="red">{error}</Alert> : null}
      {loading ? <LoadingCard /> : null}
      <div className="grid gap-4 md:grid-cols-3">
        <Metric label="Data Master" value={fmt(summary.customers || 0)} note="customers" />
        <Metric label="Data Mutasi" value={fmt(summary.transactions || 0)} note="transactions" />
        <Metric label="Loaded At" value={summary.loaded_at || "-"} note="datasets.loaded_at" compact />
      </div>
      <Card className="mt-4">
        <CardTitle title="Sumber File Awal" subtitle="File digunakan oleh loader untuk mengisi MySQL, bukan oleh Data Analyst dari UI." />
        <div className="grid gap-2">
          {(data.raw_files || []).map((file) => (
            <div key={file} className="rounded-md border border-slate-200 bg-slate-50 px-3 py-2 text-sm font-medium text-slate-700">{file}</div>
          ))}
        </div>
      </Card>
      <Card className="mt-4">
        <CardTitle title="Preview Data Sebelum Diolah" subtitle="Data mentah dari MySQL sebelum proses segmentasi." />
        <div className="grid gap-4 xl:grid-cols-2">
          <SimpleTable
            headers={["Customer ID", "Nama", "Tanggal Aktif", "Paket", "Biaya Bulanan"]}
            rows={(preview.customers || []).map((row) => [row.customer_id, row.name, row.active_date, row.category, fmt(row.monthly_fee)])}
          />
          <SimpleTable
            headers={["Customer ID", "Nama Mutasi", "Tanggal", "Jenis", "Metode", "Masuk", "Keluar"]}
            rows={(preview.transactions || []).map((row) => [row.customer_id, row.customer_name, row.transaction_date, row.transaction_type, row.payment_method, fmt(row.money_in), fmt(row.money_out)])}
          />
        </div>
      </Card>
      <Card className="mt-4">
        <CardTitle title="Ringkasan Struktur Data" subtitle="Struktur, missing value, duplikasi, dan transaksi relevan untuk LRFMC." />
        <div className="grid gap-4 xl:grid-cols-2">
          <SimpleTable
            headers={["Tabel", "Rows", "Missing ID", "Missing Nama/Tanggal", "Missing Kategori/Uang"]}
            rows={(understanding.structure || []).map((row) => [
              row.table_name,
              fmt(row.row_count),
              fmt(row.missing_customer_id),
              fmt(row.missing_name ?? row.missing_transaction_date),
              fmt(row.missing_category ?? row.missing_money_in),
            ])}
          />
          <div className="grid gap-3">
            <Metric label="Duplikasi NOPEL" value={fmt(understanding.duplicates?.customer_id || 0)} note="Cek duplikasi dasar" compact />
            <Metric label="Duplikasi Nama" value={fmt(understanding.duplicates?.name || 0)} note="Nama pelanggan yang berulang" compact />
            <Metric label="Transaksi Relevan" value={fmt(understanding.relevant_transactions || 0)} note="Filter transaksi ke LRFMC" compact />
          </div>
        </div>
      </Card>
      <div className="mt-4 grid gap-4 xl:grid-cols-3">
        <Card><CardTitle title="Distribusi Paket" /><MiniBarChart rows={distributions.category || []} /></Card>
        <Card><CardTitle title="Distribusi Transaksi" /><MiniBarChart rows={distributions.transaction_type || []} /></Card>
        <Card><CardTitle title="Distribusi Pembayaran" /><MiniBarChart rows={distributions.payment_method || []} /></Card>
      </div>
    </>
  );
}

function Process({ setPage, processState, setProcessState, onRefresh }) {
  const { running, done, result, error } = processState;
  const [period, setPeriod] = useState(processState.period || "all");

  async function start() {
    setProcessState({ running: true, done: 0, result: null, error: "", period });
    let index = 0;
    const startedAt = performance.now();
    const timer = setInterval(() => {
      index += 1;
      setProcessState((current) => ({ ...current, done: Math.min(index, pipelineSteps.length) }));
      if (index >= pipelineSteps.length) clearInterval(timer);
    }, 160);
    try {
      const response = await api("/segmentation/run", { method: "POST", body: JSON.stringify({ period }) });
      response.duration_seconds = (performance.now() - startedAt) / 1000;
      setProcessState({ running: false, done: pipelineSteps.length, result: response, error: "", period });
      onRefresh();
    } catch (err) {
      setProcessState((current) => ({ ...current, running: false, done: pipelineSteps.length, error: err.message }));
    } finally {
      clearInterval(timer);
    }
  }

  const completed = result?.status === "completed";
  return (
    <>
      <Header title="Proses Segmentasi" subtitle="Pipeline CRISP-DM, preprocessing, K-Means Plus, dan evaluasi model." action={<span data-testid="segmentation-status"><Badge tone={completed ? "green" : result ? "amber" : "slate"}>{completed ? "Segmentasi selesai" : result?.status || "Siap dijalankan"}</Badge></span>} />
      {error ? <Alert tone="red">{error}</Alert> : null}
      {result && !completed ? <Alert>Pipeline belum selesai. Pastikan MySQL aktif dan data sudah diload.</Alert> : null}
      <Card className="mb-4">
        <div className="grid items-end gap-4 md:grid-cols-[minmax(0,320px)_1fr]">
          <Field label="Periode transaksi">
            <Select
              data-testid="period-select"
              value={period}
              disabled={running}
              onChange={(event) => setPeriod(event.target.value)}
            >
              <option value="1_month">1 bulan</option>
              <option value="3_months">3 bulan</option>
              <option value="6_months">6 bulan</option>
              <option value="1_year">1 tahun</option>
              <option value="all">Semua data sampai hari ini</option>
            </Select>
          </Field>
          <p className="text-sm text-slate-500">Frequency, monetary, dan transaksi terakhir dihitung hanya dari periode yang dipilih.</p>
        </div>
      </Card>
      <div className="grid gap-4 xl:grid-cols-[1.1fr_0.9fr]">
        <Card>
          <CardTitle
            title="Progress Log"
            subtitle={`${done}/${pipelineSteps.length} tahapan`}
            action={
              <Button data-testid="start-segmentation" onClick={start} disabled={running}>
                {running ? <Loader2 size={16} className="animate-spin" /> : <Play size={16} />}
                Start Pipeline
              </Button>
            }
          />
          <div className="mb-4 h-2 overflow-hidden rounded-full bg-slate-100">
            <motion.div className="h-full rounded-full bg-slate-950" animate={{ width: `${(done / pipelineSteps.length) * 100}%` }} />
          </div>
          <div className="grid max-h-[520px] gap-2 overflow-auto rounded-md border border-slate-200 bg-slate-50 p-3">
            {pipelineSteps.map((step, index) => (
              <div key={step} className="flex items-center gap-2 rounded-md bg-white px-3 py-2 text-sm text-slate-700">
                {index < done ? <CheckCircle2 size={16} className="text-emerald-600" /> : <span className="h-4 w-4 rounded-full border border-slate-300" />}
                {step}
              </div>
            ))}
          </div>
        </Card>
        <Card>
          <CardTitle title="Evaluasi Model" subtitle={`Rows processed: ${fmt(result?.rows_processed || 0)}`} />
          {result?.period ? (
            <div data-testid="period-result" className="mb-4 grid gap-2 rounded-md border border-slate-200 bg-slate-50 p-3 text-sm sm:grid-cols-2">
              <span><strong>Periode:</strong> {result.period.label}</span>
              <span><strong>Rentang:</strong> {fmt(result.period.start_date)} - {fmt(result.period.end_date)}</span>
              <span><strong>Total transaksi:</strong> {fmt(result.period.transaction_count)}</span>
              <span><strong>Transaksi relevan:</strong> {fmt(result.period.relevant_transaction_count)}</span>
              <span><strong>Durasi UI:</strong> {decimal(result.duration_seconds)} detik</span>
            </div>
          ) : null}
          <EvaluationTable evaluation={result?.evaluation} />
          <div className="mt-5 flex flex-wrap gap-3">
            <Button onClick={() => setPage("result")} disabled={!completed}>
              <BarChart3 size={16} />
              Lihat Hasil
            </Button>
            <Button variant="secondary" onClick={() => setPage("data")}>
              <Database size={16} />
              Data Tertanam
            </Button>
          </div>
        </Card>
      </div>
      {result ? <ProcessInsight result={result} /> : null}
    </>
  );
}

function Result({ refreshKey }) {
  const [downloadOpen, setDownloadOpen] = useState(false);
  const [page, setPageNumber] = useState(1);
  const [keyword, setKeyword] = useState("");
  const [category, setCategory] = useState("name");
  const [segment, setSegment] = useState("all");
  const [paymentStatus, setPaymentStatus] = useState("all");
  const query = useMemo(() => {
    const params = new URLSearchParams({
      page: String(page),
      per_page: "10",
      keyword,
      category,
      segment,
      payment_status: paymentStatus,
    });
    return `/result/?${params.toString()}`;
  }, [page, keyword, category, segment, paymentStatus]);
  const { loading, error, data } = useApi(query, { summary: {}, evaluation: {}, clusters: [], customers: [], cluster_profile: [], pagination: {}, database_ready: false }, refreshKey);
  const clusters = data.clusters || [];
  const customers = data.customers || [];
  const pagination = data.pagination || { page: 1, total_pages: 1, total: 0 };
  useEffect(() => {
    setPageNumber(1);
  }, [keyword, category, segment, paymentStatus]);
  const segmentTotals = ["Low-Value", "Medium-Value", "High-Value"].map((label) => ({
    label,
    count: clusters.filter((item) => item.segment_label === label).reduce((sum, item) => sum + Number(item.customer_count || 0), 0),
  }));
  const max = Math.max(1, ...segmentTotals.map((row) => row.count));
  return (
    <>
      <Header title="Lihat Hasil" subtitle="Grafik jumlah pelanggan, karakteristik cluster, dan tabel hasil pelanggan." action={<Badge tone={data.database_ready ? "green" : "red"}>{data.database_ready ? "MySQL" : "MySQL belum tersambung"}</Badge>} />
      {error ? <Alert tone="red">{error}</Alert> : null}
      {loading ? <LoadingCard /> : null}
      {!loading && !customers.length ? <Alert>Belum ada hasil segmentasi. Jalankan proses segmentasi setelah MySQL dan data tersedia.</Alert> : null}
      <Card>
        <CardTitle title="Jumlah Pelanggan per Segmen" subtitle="Distribusi 3 tingkatan segmentasi: Low, Medium, High." />
        <div className="grid h-72 grid-cols-3 items-end gap-5 border-b border-slate-200 px-2">
          {segmentTotals.map((row) => {
            const count = row.count;
            return (
              <div key={row.label} className="grid h-full content-end gap-2 text-center">
                <p className="text-sm font-bold text-slate-950">{fmt(count)}</p>
                <motion.div initial={{ height: 0 }} animate={{ height: Math.max(0, (count / max) * 210) }} className="rounded-t-md bg-slate-950" />
                <p className="pb-2 text-xs font-semibold text-slate-500">{row.label}</p>
              </div>
            );
          })}
        </div>
      </Card>
      <Card className="mt-4">
        <CardTitle title="Karakteristik Cluster" />
        <ClusterTable rows={clusters} />
      </Card>
      <div className="mt-4 grid gap-4 xl:grid-cols-[0.9fr_1.1fr]">
        <Card>
          <CardTitle title="Radar Profil Cluster" subtitle="Rata-rata fitur LRFMC tiap cluster." />
          <RadarChart profiles={data.cluster_profile || []} />
        </Card>
        <Card>
          <CardTitle title="Saran Bisnis per Cluster" subtitle="Rekomendasi berdasarkan profil LRFMC." />
          <BusinessRecommendations profiles={data.cluster_profile || []} />
        </Card>
      </div>
      <Card className="mt-4">
        <CardTitle
          title={`Table Hasil Pelanggan (${fmt(pagination.total || 0)} data)`}
          action={
            <div className="flex flex-wrap gap-2">
              <Button variant="secondary" onClick={() => setDownloadOpen(true)}><Download size={16} />Download Result</Button>
            </div>
          }
        />
        <div className="mb-4 grid gap-3 rounded-md border border-slate-200 bg-slate-50 p-3 lg:grid-cols-[180px_minmax(220px,1fr)_180px_210px] lg:items-end">
          <Field label="Cari berdasarkan">
            <Select value={category} onChange={(event) => setCategory(event.target.value)}>
              <option value="name">Nama Pelanggan</option>
              <option value="customer_id">Customer ID</option>
            </Select>
          </Field>
          <Field label="Kata kunci">
            <Input value={keyword} onChange={(event) => setKeyword(event.target.value)} placeholder="Cari di hasil segmentasi" />
          </Field>
          <Field label="Filter segmen">
            <Select value={segment} onChange={(event) => setSegment(event.target.value)}>
              <option value="all">Semua Segmen</option>
              <option>Low-Value</option>
              <option>Medium-Value</option>
              <option>High-Value</option>
            </Select>
          </Field>
          <Field label="Status pembayaran">
            <Select value={paymentStatus} onChange={(event) => setPaymentStatus(event.target.value)}>
              <option value="all">Semua Status</option>
              <option value="on_time">Tepat waktu</option>
              <option value="late">Sering terlambat</option>
              <option value="unknown">Belum teridentifikasi</option>
            </Select>
          </Field>
        </div>
        <CustomerTable rows={customers} />
        <Pagination pagination={pagination} onChange={setPageNumber} />
      </Card>
      <DownloadOverlay open={downloadOpen} onClose={() => setDownloadOpen(false)} />
    </>
  );
}

function DownloadOverlay({ open, onClose }) {
  const [format, setFormat] = useState("csv");
  const [status, setStatus] = useState("Pilih format export.");
  const [loading, setLoading] = useState(false);

  async function download() {
    setLoading(true);
    setStatus("Menyiapkan file untuk browser...");
    try {
      const result = await downloadApi("/download/", {
        method: "POST",
        body: JSON.stringify({ format, include_metadata: true, include_evaluation: true }),
      });
      const url = URL.createObjectURL(result.blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = result.filename;
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(url);
      setStatus(`Download dimulai: ${result.filename}`);
    } catch (error) {
      setStatus(error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <AnimatePresence>
      {open ? (
        <motion.div className="fixed inset-0 z-50 grid place-items-center bg-slate-950/40 p-4" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
          <motion.div className="w-full max-w-xl rounded-lg border border-slate-200 bg-white p-5 shadow-soft" initial={{ scale: 0.96, y: 10 }} animate={{ scale: 1, y: 0 }} exit={{ scale: 0.96, y: 10 }}>
            <CardTitle title="Download Result" subtitle="Export hasil segmentasi tanpa berpindah halaman." action={<Button variant="ghost" className="h-9 w-9 px-0" onClick={onClose}><X size={16} /></Button>} />
            <div className="grid gap-4">
              {[
                ["csv", "CSV", FileSpreadsheet],
                ["excel", "Excel", FileSpreadsheet],
                ["json", "JSON", FileJson],
              ].map(([key, label, Icon]) => (
                <label key={key} className={cx("flex cursor-pointer items-center gap-3 rounded-md border p-3 transition", format === key ? "border-slate-950 bg-slate-50" : "border-slate-200 bg-white hover:bg-slate-50")}>
                  <input className="h-4 w-4 accent-slate-950" type="radio" checked={format === key} onChange={() => setFormat(key)} />
                  <Icon size={17} />
                  <span className="text-sm font-semibold">{label}</span>
                </label>
              ))}
              <div className="rounded-md border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-600">{status}</div>
              <div className="flex flex-wrap justify-end gap-3">
                <Button variant="secondary" onClick={onClose}>Cancel</Button>
                <Button onClick={download} disabled={loading}>{loading ? <Loader2 size={16} className="animate-spin" /> : <Download size={16} />}Download</Button>
              </div>
            </div>
          </motion.div>
        </motion.div>
      ) : null}
    </AnimatePresence>
  );
}

function EvaluationTable({ evaluation = {} }) {
  const rows = [
    ["DBI", evaluation?.dbi, "Semakin kecil semakin baik"],
    ["CHI", evaluation?.chi, "Separasi cluster"],
    ["Silhouette Score", evaluation?.silhouette_score, "Kualitas cluster"],
    ["Segment Level", evaluation?.segment_level_count ?? 3, "Low, Medium, High"],
  ];
  return (
    <div className="overflow-auto rounded-md border border-slate-200">
      <table className="w-full min-w-[560px] text-left text-sm">
        <thead className="bg-slate-50 text-xs uppercase text-slate-500">
          <tr><th className="px-3 py-3">Metric</th><th className="px-3 py-3">Value</th><th className="px-3 py-3">Note</th></tr>
        </thead>
        <tbody className="divide-y divide-slate-200">
          {rows.map((row) => (
            <tr key={row[0]} className="bg-white">
              <td className="px-3 py-3 font-semibold text-slate-950">{row[0]}</td>
              <td className="px-3 py-3 text-slate-700">{decimal(row[1])}</td>
              <td className="px-3 py-3 text-slate-500">{row[2]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function ProcessInsight({ result }) {
  return (
    <div className="mt-4 grid gap-4">
      <div className="grid gap-4 xl:grid-cols-[1.1fr_0.9fr]">
        <Card>
          <CardTitle title={`Evaluasi K dan Elbow Method${result.optimal_k ? ` - K optimal ${result.optimal_k}` : ""}`} subtitle="Setiap k dicek menggunakan inertia, silhouette, DBI, CHI, dan iterasi." />
          <KMetricTable rows={result.k_evaluation || []} optimalK={result.optimal_k} />
        </Card>
        <Card>
          <CardTitle title="Ringkasan Model Terpilih" subtitle="Konfigurasi final yang digunakan pada proses segmentasi." />
          <ModelConfigSummary config={result.model_config || {}} />
        </Card>
      </div>
      <MetricCharts rows={result.k_evaluation || []} selected={result.optimal_k} />
      <Card>
        <CardTitle title="Feature Overview LRFMC" subtitle="Garis putus-putus menunjukkan rata-rata seluruh data; bar menunjukkan rata-rata tiap segmen." />
        <FeatureOverview rows={result.feature_overview || []} />
      </Card>
      <div className="grid gap-4 xl:grid-cols-2">
        <Card><CardTitle title="Heatmap Profil Cluster" subtitle="Intensitas warna menunjukkan posisi relatif fitur LRFMC antar cluster." /><ClusterHeatmap profiles={result.cluster_profile || []} /></Card>
        <Card><CardTitle title="Peta Nilai Cluster" subtitle="Frequency dibanding Monetary; ukuran bubble mengikuti jumlah pelanggan." /><ClusterBubbleChart profiles={result.cluster_profile || []} /></Card>
      </div>
    </div>
  );
}

function ClusterTable({ rows }) {
  return (
    <div className="overflow-auto rounded-md border border-slate-200">
      <table className="w-full min-w-[1040px] text-left text-sm">
        <thead className="bg-slate-50 text-xs uppercase text-slate-500">
          <tr>{["Cluster", "Label Segmen", "Avg L", "Avg R", "Avg F", "Avg M", "Avg C", "Jumlah Pelanggan", "Interpretasi"].map((head) => <th key={head} className="px-3 py-3">{head}</th>)}</tr>
        </thead>
        <tbody className="divide-y divide-slate-200">
          {rows.map((row) => (
            <tr key={`${row.cluster}-${row.segment_label}`} className="bg-white">
              <td className="px-3 py-3 text-slate-700">{row.cluster}</td>
              <td className="px-3 py-3 text-slate-700"><SegmentBadge segment={row.segment_label} /></td>
              <td className="px-3 py-3 text-slate-700">{decimal(row.avg_loyalty)}</td>
              <td className="px-3 py-3 text-slate-700">{decimal(row.avg_recency)}</td>
              <td className="px-3 py-3 text-slate-700">{decimal(row.avg_frequency)}</td>
              <td className="px-3 py-3 text-slate-700">{decimal(row.avg_monetary)}</td>
              <td className="px-3 py-3 text-slate-700">{decimal(row.avg_category)}</td>
              <td className="px-3 py-3 text-slate-700">{fmt(row.customer_count)}</td>
              <td className="max-w-[260px] break-words px-3 py-3 text-slate-700">{row.interpretation}</td>
            </tr>
          ))}
          {!rows.length ? <EmptyRow colSpan={9} /> : null}
        </tbody>
      </table>
    </div>
  );
}

function SimpleTable({ headers, rows }) {
  return (
    <div className="overflow-auto rounded-md border border-slate-200">
      <table className="w-full min-w-[520px] text-left text-sm">
        <thead className="bg-slate-50 text-xs uppercase text-slate-500"><tr>{headers.map((head) => <th key={head} className="px-3 py-3">{head}</th>)}</tr></thead>
        <tbody className="divide-y divide-slate-200">
          {rows.map((row, index) => <tr key={index}>{row.map((cell, idx) => <td key={idx} className="max-w-[240px] break-words px-3 py-3 text-slate-700">{cell}</td>)}</tr>)}
          {!rows.length ? <EmptyRow colSpan={headers.length} /> : null}
        </tbody>
      </table>
    </div>
  );
}

function KMetricTable({ rows, optimalK }) {
  return (
    <SimpleTable
      headers={["K", "Inertia", "Silhouette", "DBI", "CHI", "Iterasi", "Status"]}
      rows={rows.map((row) => [
        row.k,
        decimal(row.inertia_sse),
        decimal(row.silhouette_score),
        decimal(row.davies_bouldin_index),
        decimal(row.calinski_harabasz_index),
        fmt(row.iteration),
        Number(row.k) === Number(optimalK) ? "K optimal" : "-",
      ])}
    />
  );
}

function ModelConfigSummary({ config }) {
  const rows = [
    ["Nama model", config.name || "-"],
    ["Transformasi", config.transform || "-"],
    ["Scaler", config.scaler || "-"],
    ["Winsor", config.winsor || "-"],
    ["K optimal", config.optimal_k ?? "-"],
    ["Skor seleksi", config.selection_score === undefined ? "-" : decimal(config.selection_score)],
  ];
  return (
    <div className="grid gap-2">
      {rows.map(([label, value]) => (
        <div key={label} className="flex items-center justify-between gap-3 rounded-md border border-slate-200 bg-slate-50 px-3 py-2 text-sm">
          <span className="text-slate-500">{label}</span>
          <strong className="break-all text-right text-slate-950">{value}</strong>
        </div>
      ))}
    </div>
  );
}

function ModelCandidateTable({ rows }) {
  return (
    <SimpleTable
      headers={["Konfigurasi", "Transform", "Scaler", "Winsor", "K", "Silhouette", "DBI", "CHI", "Skor", "Status"]}
      rows={rows.map((row) => [
        row.name,
        row.transform,
        row.scaler,
        row.winsor,
        row.optimal_k,
        decimal(row.silhouette_score),
        decimal(row.davies_bouldin_index),
        decimal(row.calinski_harabasz_index),
        decimal(row.selection_score),
        row.selected ? "Dipakai" : "-",
      ])}
    />
  );
}

function MiniBarChart({ rows }) {
  const max = Math.max(1, ...rows.map((row) => Number(row.value || 0)));
  return (
    <div className="grid gap-2">
      {rows.slice(0, 8).map((row) => (
        <div key={row.label} className="grid grid-cols-[minmax(0,1fr)_70px] items-center gap-3 text-sm">
          <div className="min-w-0">
            <div className="truncate text-slate-600">{row.label}</div>
            <div className="mt-1 h-2 overflow-hidden rounded-full bg-slate-100">
              <div className="h-full rounded-full bg-slate-950" style={{ width: `${(Number(row.value || 0) / max) * 100}%` }} />
            </div>
          </div>
          <strong className="text-right text-slate-950">{fmt(row.value)}</strong>
        </div>
      ))}
      {!rows.length ? <div className="text-sm text-slate-500">Data tidak tersedia.</div> : null}
    </div>
  );
}

function FlowDiagram({ steps }) {
  return (
    <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
      {steps.map((step, index) => {
        const title = typeof step === "string" ? step : step.title;
        return (
        <div key={title} className="relative rounded-md border border-slate-200 bg-slate-50 p-3 text-sm text-slate-700">
          <span className="mb-2 grid h-6 w-6 place-items-center rounded-full bg-slate-950 text-xs text-white">{index + 1}</span>
          <p className="font-semibold text-slate-950">{title}</p>
          {typeof step !== "string" ? <p className="mt-1 text-xs leading-5 text-slate-500">{step.description}</p> : null}
          {typeof step !== "string" && step.processes?.length ? (
            <ul className="mt-3 grid gap-1 text-xs text-slate-600">
              {step.processes.map((item) => <li key={item} className="break-words rounded border border-slate-200 bg-white px-2 py-1">{item}</li>)}
            </ul>
          ) : null}
          {typeof step !== "string" && step.output ? <p className="mt-3 rounded bg-white px-2 py-1 text-xs font-semibold text-slate-700">{step.output}</p> : null}
        </div>
        );
      })}
    </div>
  );
}

function PreparationVisual({ steps }) {
  const width = 860;
  const height = 190;
  const nodes = (steps || []).slice(0, 8).map((step, index) => ({
    label: typeof step === "string" ? step : step.title,
    x: 42 + index * 108,
    y: index % 2 === 0 ? 52 : 118,
  }));
  return (
    <div className="overflow-auto rounded-md border border-slate-200 bg-white">
      <svg viewBox={`0 0 ${width} ${height}`} className="min-h-[190px] w-full min-w-[760px]">
        {nodes.slice(0, -1).map((node, index) => {
          const next = nodes[index + 1];
          return (
            <g key={`${node.label}-${next.label}`}>
              <line x1={node.x + 70} y1={node.y} x2={next.x - 12} y2={next.y} stroke="#94a3b8" strokeWidth="1.5" />
              <polygon points={`${next.x - 12},${next.y} ${next.x - 21},${next.y - 5} ${next.x - 21},${next.y + 5}`} fill="#94a3b8" />
            </g>
          );
        })}
        {nodes.map((node, index) => (
          <g key={node.label}>
            <rect x={node.x - 34} y={node.y - 27} width="104" height="54" rx="6" fill={index === nodes.length - 1 ? "#ecfdf5" : "#f8fafc"} stroke={index === nodes.length - 1 ? "#10b981" : "#cbd5e1"} />
            <circle cx={node.x - 22} cy={node.y - 16} r="10" fill="#0f172a" />
            <text x={node.x - 22} y={node.y - 12} textAnchor="middle" fontSize="10" fill="#ffffff">{index + 1}</text>
            <foreignObject x={node.x - 18} y={node.y - 19} width="76" height="42">
              <div className="flex h-full items-center text-[10px] font-semibold leading-tight text-slate-700">{node.label}</div>
            </foreignObject>
          </g>
        ))}
      </svg>
    </div>
  );
}

function MetricCharts({ rows, selected }) {
  const charts = [
    ["Diagram Elbow", "Inertia/SSE per nilai k", "inertia_sse"],
    ["Diagram Silhouette", "Semakin tinggi semakin baik", "silhouette_score"],
    ["Diagram Davies-Bouldin", "Semakin rendah semakin baik", "davies_bouldin_index"],
    ["Diagram Calinski-Harabasz", "Semakin tinggi semakin baik", "calinski_harabasz_index"],
  ];
  return (
    <div className="grid gap-4 xl:grid-cols-2">
      {charts.map(([title, subtitle, key]) => (
        <Card key={key}>
          <CardTitle title={title} subtitle={subtitle} />
          <LineChart rows={rows} xKey="k" yKey={key} selected={selected} />
        </Card>
      ))}
    </div>
  );
}

function LineChart({ rows, xKey, yKey, selected }) {
  const width = 520;
  const height = 220;
  const pad = 34;
  if (!rows.length) {
    return <div className="text-sm text-slate-500">Evaluasi K belum tersedia.</div>;
  }
  const values = rows.map((row) => Number(row[yKey] || 0));
  const min = Math.min(...values);
  const max = Math.max(...values);
  const points = rows.map((row, index) => {
    const x = pad + (index / Math.max(rows.length - 1, 1)) * (width - pad * 2);
    const y = height - pad - ((Number(row[yKey] || 0) - min) / Math.max(max - min, 0.0001)) * (height - pad * 2);
    return { x, y, row };
  });
  return (
    <div className="overflow-auto">
      <svg viewBox={`0 0 ${width} ${height}`} className="min-h-[220px] w-full min-w-[480px] rounded-md bg-slate-50">
        {[0, 0.25, 0.5, 0.75, 1].map((level) => {
          const y = pad + level * (height - pad * 2);
          const value = max - level * (max - min);
          return (
            <g key={level}>
              <line x1={pad} y1={y} x2={width - pad} y2={y} stroke="#e2e8f0" />
              <text x={pad - 6} y={y + 4} textAnchor="end" fontSize="10" fill="#94a3b8">{decimal(value)}</text>
            </g>
          );
        })}
        <line x1={pad} y1={height - pad} x2={width - pad} y2={height - pad} stroke="#cbd5e1" />
        <line x1={pad} y1={pad} x2={pad} y2={height - pad} stroke="#cbd5e1" />
        <polyline fill="none" stroke="#0f172a" strokeWidth="2" points={points.map((point) => `${point.x},${point.y}`).join(" ")} />
        {points.map((point) => (
          <g key={point.row[xKey]}>
            <circle cx={point.x} cy={point.y} r={Number(point.row[xKey]) === Number(selected) ? 6 : 4} fill={Number(point.row[xKey]) === Number(selected) ? "#059669" : "#0f172a"} />
            <title>{`K ${point.row[xKey]}: ${decimal(point.row[yKey])}`}</title>
            <text x={point.x} y={height - 8} textAnchor="middle" fontSize="11" fill="#64748b">{point.row[xKey]}</text>
          </g>
        ))}
      </svg>
    </div>
  );
}

function RadarChart({ profiles }) {
  const [selectedCluster, setSelectedCluster] = useState("all");
  const labels = ["loyalty", "recency", "frequency", "monetary", "category"];
  const names = ["L", "R", "F", "M", "C"];
  const width = 320;
  const height = 280;
  const center = { x: width / 2, y: height / 2 };
  const radius = 96;
  const colors = ["#0f172a", "#d97706", "#059669", "#2563eb", "#dc2626", "#7c3aed"];
  const visibleProfiles = selectedCluster === "all" ? profiles : profiles.filter((profile) => String(profile.cluster) === selectedCluster);
  const maxByLabel = labels.reduce((acc, label) => {
    acc[label] = Math.max(1, ...profiles.map((profile) => Number(profile[label] || 0)));
    return acc;
  }, {});
  const normalizedValue = (profile, label) => {
    const raw = Number(profile[label] || 0);
    return Math.max(0, Math.min(1, raw / (maxByLabel[label] || 1)));
  };
  const angle = (index) => -Math.PI / 2 + (index / labels.length) * Math.PI * 2;
  const point = (value, index) => {
    const a = angle(index);
    return [center.x + Math.cos(a) * radius * Number(value || 0), center.y + Math.sin(a) * radius * Number(value || 0)];
  };
  return (
    <div className="grid min-w-0 gap-3">
      <div className="flex flex-wrap gap-2">
        <Button variant={selectedCluster === "all" ? "primary" : "secondary"} className="h-8 px-3 text-xs" onClick={() => setSelectedCluster("all")}>Semua</Button>
        {profiles.map((profile) => (
          <Button key={profile.cluster} variant={String(profile.cluster) === selectedCluster ? "primary" : "secondary"} className="h-8 px-3 text-xs" onClick={() => setSelectedCluster(String(profile.cluster))}>
            Cluster {profile.cluster}
          </Button>
        ))}
      </div>
      <div className="grid min-w-0 gap-3">
        <svg viewBox={`0 0 ${width} ${height}`} className="mx-auto w-full max-w-[360px]">
          {[0.25, 0.5, 0.75, 1].map((level) => (
            <polygon key={level} points={labels.map((_, idx) => point(level, idx).join(",")).join(" ")} fill="none" stroke="#e2e8f0" />
          ))}
          {labels.map((_, idx) => {
            const [x, y] = point(1, idx);
            return <line key={idx} x1={center.x} y1={center.y} x2={x} y2={y} stroke="#e2e8f0" />;
          })}
          {visibleProfiles.map((profile) => {
            const colorIndex = Math.max(profiles.findIndex((item) => item.cluster === profile.cluster), 0);
            return (
              <polygon
                key={profile.cluster}
                points={labels.map((label, idx) => point(normalizedValue(profile, label), idx).join(",")).join(" ")}
                fill={colors[colorIndex % colors.length]}
                fillOpacity="0.12"
                stroke={colors[colorIndex % colors.length]}
                strokeWidth="2"
              />
            );
          })}
          {names.map((label, idx) => {
            const [x, y] = point(1.16, idx);
            return <text key={label} x={x} y={y} textAnchor="middle" fontSize="12" fill="#475569">{label}</text>;
          })}
        </svg>
        <div className="grid min-w-0 content-start gap-2">
          {visibleProfiles.map((profile) => {
            const colorIndex = Math.max(profiles.findIndex((item) => item.cluster === profile.cluster), 0);
            return (
            <div key={profile.cluster} className="min-w-0 rounded-md border border-slate-200 bg-slate-50 p-3 text-sm">
              <div className="mb-2 flex flex-wrap items-center gap-2">
                <span className="h-3 w-3 rounded-full" style={{ background: colors[colorIndex % colors.length] }} />
                <span className="font-semibold">Cluster {profile.cluster}</span>
                <SegmentBadge segment={profile.segment_label} />
              </div>
              <div className="grid gap-2 text-xs text-slate-600 sm:grid-cols-5">
                {labels.map((label, idx) => (
                  <div key={label} className="rounded border border-slate-200 bg-white px-2 py-1">
                    <span className="block font-semibold text-slate-950">{names[idx]}</span>
                    <span className="break-words">{decimal(profile[label])}</span>
                  </div>
                ))}
              </div>
            </div>
            );
          })}
          {!profiles.length ? <div className="text-sm text-slate-500">Profil cluster belum tersedia.</div> : null}
        </div>
      </div>
    </div>
  );
}

function FeatureOverview({ rows }) {
  return (
    <div className="grid gap-3">
      {rows.map((row) => (
        <FeatureOverviewItem key={row.feature} row={row} />
      ))}
      {!rows.length ? <div className="text-sm text-slate-500">Feature overview belum tersedia.</div> : null}
      <div className="rounded-md border border-slate-200 bg-white p-3 text-xs leading-5 text-slate-600">
        <strong className="block text-sm text-slate-950">Keterangan Arah Panah</strong>
        <span className="block">L, R, F, M, C naik berarti lebih baik; R naik berarti transaksi lebih baru.</span>
        <span className="block">Bar lebih panjang berarti rata-rata fitur segmen lebih tinggi.</span>
      </div>
    </div>
  );
}

function FeatureOverviewItem({ row }) {
  const segmentOrder = { "High-Value": 0, "Medium-Value": 1, "Low-Value": 2 };
  const segments = [...(row.segments || [])].sort(
    (a, b) => (segmentOrder[a.segment] ?? 99) - (segmentOrder[b.segment] ?? 99)
  );
  const values = [Number(row.mean || 0), ...segments.map((item) => Number(item.value || 0))];
  const max = Math.max(1, ...values);
  const averagePosition = Math.min(100, Math.max(0, (Number(row.mean || 0) / max) * 100));
  const colorFor = (segment) => (segment?.includes("High") ? "bg-emerald-600" : segment?.includes("Medium") ? "bg-amber-600" : "bg-red-600");
  return (
    <div className="rounded-md border border-slate-200 bg-slate-50 p-3">
      <div className="mb-3 flex flex-wrap items-start justify-between gap-3">
        <div>
          <strong className="text-sm text-slate-950">{row.feature}</strong>
          <p className="mt-1 text-xs text-slate-500">{row.direction}</p>
        </div>
        <span className="rounded border border-slate-200 bg-white px-2 py-1 text-xs font-semibold text-slate-600">Avg {decimal(row.mean)}</span>
      </div>
      <div className="grid gap-2">
        {segments.map((segment) => (
          <div key={segment.segment} className="grid grid-cols-[112px_minmax(0,1fr)_92px] items-center gap-2 text-xs">
            <span className="truncate font-semibold text-slate-700">{segment.segment}</span>
            <div className="relative h-7 overflow-hidden rounded border border-slate-200 bg-white">
              <span className="absolute inset-y-0 border-l border-dashed border-slate-400" style={{ left: `${averagePosition}%` }} />
              <span className={cx("block h-full rounded-r", colorFor(segment.segment))} style={{ width: `${Math.max(3, (Number(segment.value || 0) / max) * 100)}%`, opacity: 0.82 }} />
            </div>
            <span className="text-right font-semibold text-slate-700">{decimal(segment.value)} {segment.arrow}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function ClusterHeatmap({ profiles }) {
  const features = [
    ["loyalty", "L"],
    ["recency", "R"],
    ["frequency", "F"],
    ["monetary", "M"],
    ["category", "C"],
  ];
  const maxByFeature = features.reduce((acc, [key]) => {
    acc[key] = Math.max(1, ...profiles.map((profile) => Number(profile[key] || 0)));
    return acc;
  }, {});
  const intensity = (profile, key) => {
    const value = Number(profile[key] || 0);
    const normalized = value / maxByFeature[key];
    return Math.max(0.08, Math.min(1, normalized));
  };
  return (
    <div className="overflow-auto rounded-md border border-slate-200">
      <table className="w-full min-w-[620px] text-left text-sm">
        <thead className="bg-slate-50 text-xs uppercase text-slate-500">
          <tr>
            <th className="px-3 py-3">Cluster</th>
            <th className="px-3 py-3">Segmen</th>
            {features.map(([, label]) => <th key={label} className="px-3 py-3 text-center">{label}</th>)}
            <th className="px-3 py-3 text-right">Pelanggan</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-200">
          {profiles.map((profile) => (
            <tr key={profile.cluster} className="bg-white">
              <td className="px-3 py-3 font-semibold text-slate-950">Cluster {profile.cluster}</td>
              <td className="px-3 py-3"><SegmentBadge segment={profile.segment_label} /></td>
              {features.map(([key, label]) => {
                const alpha = intensity(profile, key);
                const bg = key === "recency" ? `rgba(5, 150, 105, ${alpha})` : `rgba(15, 23, 42, ${alpha})`;
                return (
                  <td key={key} className="px-3 py-3 text-center">
                    <span className="inline-flex min-w-20 justify-center rounded px-2 py-1 font-semibold text-white" style={{ backgroundColor: bg }} title={`${label}: ${decimal(profile[key])}`}>
                      {decimal(profile[key])}
                    </span>
                  </td>
                );
              })}
              <td className="px-3 py-3 text-right font-semibold text-slate-700">{fmt(profile.customer_count)}</td>
            </tr>
          ))}
          {!profiles.length ? <EmptyRow colSpan={8} /> : null}
        </tbody>
      </table>
      <div className="border-t border-slate-200 bg-slate-50 px-3 py-2 text-xs text-slate-500">
        Untuk Recency, nilai dan warna lebih kuat berarti lebih baik karena transaksi lebih baru.
      </div>
    </div>
  );
}

function ClusterBubbleChart({ profiles }) {
  const width = 520;
  const height = 320;
  const pad = 48;
  const maxFrequency = Math.max(1, ...profiles.map((profile) => Number(profile.frequency || 0)));
  const maxMonetary = Math.max(1, ...profiles.map((profile) => Number(profile.monetary || 0)));
  const maxCount = Math.max(1, ...profiles.map((profile) => Number(profile.customer_count || 0)));
  const colorFor = (segment) => (segment?.includes("High") ? "#059669" : segment?.includes("Medium") ? "#d97706" : "#dc2626");
  const xScale = (value) => pad + (Number(value || 0) / maxFrequency) * (width - pad * 2);
  const yScale = (value) => height - pad - (Number(value || 0) / maxMonetary) * (height - pad * 2);
  return (
    <div className="overflow-auto">
      <svg viewBox={`0 0 ${width} ${height}`} className="min-h-[320px] w-full min-w-[480px] rounded-md bg-slate-50">
        {[0, 0.25, 0.5, 0.75, 1].map((level) => {
          const x = pad + level * (width - pad * 2);
          const y = pad + level * (height - pad * 2);
          return (
            <g key={level}>
              <line x1={x} y1={pad} x2={x} y2={height - pad} stroke="#e2e8f0" />
              <line x1={pad} y1={y} x2={width - pad} y2={y} stroke="#e2e8f0" />
            </g>
          );
        })}
        <line x1={pad} y1={height - pad} x2={width - pad} y2={height - pad} stroke="#cbd5e1" />
        <line x1={pad} y1={pad} x2={pad} y2={height - pad} stroke="#cbd5e1" />
        <text x={width - pad} y={height - 14} textAnchor="end" fontSize="11" fill="#64748b">Frequency</text>
        <text x={12} y={pad + 4} fontSize="11" fill="#64748b">Monetary</text>
        {profiles.map((profile) => {
          const radius = 9 + (Number(profile.customer_count || 0) / maxCount) * 24;
          const x = xScale(profile.frequency);
          const y = yScale(profile.monetary);
          return (
            <g key={profile.cluster}>
              <circle cx={x} cy={y} r={radius} fill={colorFor(profile.segment_label)} opacity="0.72" stroke="#ffffff" strokeWidth="1.5">
                <title>{`Cluster ${profile.cluster}\n${profile.segment_label}\nFrequency: ${decimal(profile.frequency)}\nMonetary: ${decimal(profile.monetary)}\nPelanggan: ${fmt(profile.customer_count)}`}</title>
              </circle>
              <text x={x} y={y + 4} textAnchor="middle" fontSize="12" fontWeight="700" fill="#ffffff">{profile.cluster}</text>
            </g>
          );
        })}
      </svg>
      <ClusterLegend />
      {!profiles.length ? <div className="text-sm text-slate-500">Peta cluster belum tersedia.</div> : null}
    </div>
  );
}

function Scatter2D({ points }) {
  const width = 520;
  const height = 300;
  const pad = 42;
  const xs = points.map((p) => Number(p.x));
  const ys = points.map((p) => Number(p.y));
  const minX = Math.min(...xs, -1);
  const maxX = Math.max(...xs, 1);
  const minY = Math.min(...ys, -1);
  const maxY = Math.max(...ys, 1);
  const colorFor = (segment) => (segment?.includes("High") ? "#059669" : segment?.includes("Medium") ? "#d97706" : "#dc2626");
  const xScale = (value) => pad + ((Number(value) - minX) / Math.max(maxX - minX, 1)) * (width - pad * 2);
  const yScale = (value) => height - pad - ((Number(value) - minY) / Math.max(maxY - minY, 1)) * (height - pad * 2);
  return (
    <div className="overflow-auto">
      <svg viewBox={`0 0 ${width} ${height}`} className="min-h-[300px] w-full min-w-[480px] rounded-md bg-slate-50">
        {[0, 0.25, 0.5, 0.75, 1].map((level) => {
          const x = pad + level * (width - pad * 2);
          const y = pad + level * (height - pad * 2);
          return (
            <g key={level}>
              <line x1={x} y1={pad} x2={x} y2={height - pad} stroke="#e2e8f0" />
              <line x1={pad} y1={y} x2={width - pad} y2={y} stroke="#e2e8f0" />
            </g>
          );
        })}
        <line x1={pad} y1={height - pad} x2={width - pad} y2={height - pad} stroke="#cbd5e1" />
        <line x1={pad} y1={pad} x2={pad} y2={height - pad} stroke="#cbd5e1" />
        <text x={width - pad} y={height - 12} textAnchor="end" fontSize="11" fill="#64748b">PCA 1</text>
        <text x={12} y={pad + 4} fontSize="11" fill="#64748b">PCA 2</text>
        <text x={pad} y={height - 12} fontSize="10" fill="#94a3b8">{decimal(minX)}</text>
        <text x={width - pad} y={height - 28} textAnchor="end" fontSize="10" fill="#94a3b8">{decimal(maxX)}</text>
        <text x={pad + 4} y={height - pad - 4} fontSize="10" fill="#94a3b8">{decimal(minY)}</text>
        <text x={pad + 4} y={pad + 12} fontSize="10" fill="#94a3b8">{decimal(maxY)}</text>
        {points.map((p, index) => {
          const x = xScale(p.x);
          const y = yScale(p.y);
          return (
            <circle key={`${p.customer_id}-${index}`} cx={x} cy={y} r={4.2} fill={colorFor(p.segment_label)} opacity={0.7} stroke="#ffffff" strokeWidth="0.6">
              <title>{`${p.customer_id} - ${p.name || "-"}\n${p.segment_label} / Cluster ${p.cluster}\nPCA 1: ${decimal(p.x)} | PCA 2: ${decimal(p.y)}`}</title>
            </circle>
          );
        })}
      </svg>
      <ClusterLegend />
      {!points.length ? <div className="text-sm text-slate-500">Visualisasi belum tersedia.</div> : null}
    </div>
  );
}

function Scatter3D({ points }) {
  const width = 520;
  const height = 340;
  const xs = points.map((p) => Number(p.x));
  const ys = points.map((p) => Number(p.y));
  const zs = points.map((p) => Number(p.z || 0));
  const minX = Math.min(...xs, -1);
  const maxX = Math.max(...xs, 1);
  const minY = Math.min(...ys, -1);
  const maxY = Math.max(...ys, 1);
  const minZ = Math.min(...zs, -1);
  const maxZ = Math.max(...zs, 1);
  const colorFor = (segment) => (segment?.includes("High") ? "#059669" : segment?.includes("Medium") ? "#d97706" : "#dc2626");
  const norm = (value, min, max) => ((Number(value) - min) / Math.max(max - min, 1)) * 2 - 1;
  const project = (point) => {
    const nx = norm(point.x, minX, maxX);
    const ny = norm(point.y, minY, maxY);
    const nz = norm(point.z || 0, minZ, maxZ);
    return {
      x: width / 2 + nx * 150 + nz * 62,
      y: height / 2 - ny * 92 - nz * 52,
      z: nz,
    };
  };
  const projected = points
    .map((point, index) => ({ ...point, index, pc1: point.x, pc2: point.y, pc3: point.z, ...project(point) }))
    .sort((a, b) => a.z - b.z);
  const axis = {
    origin: { x: width / 2, y: height / 2 + 16 },
    pc1: { x: width / 2 + 178, y: height / 2 + 16 },
    pc2: { x: width / 2, y: height / 2 - 98 },
    pc3: { x: width / 2 + 86, y: height / 2 - 52 },
  };
  return (
    <div className="overflow-auto">
      <svg viewBox={`0 0 ${width} ${height}`} className="min-h-[340px] w-full min-w-[480px] rounded-md bg-slate-50">
        {[0.25, 0.5, 0.75, 1].map((level) => (
          <polygon
            key={level}
            points={[
              `${axis.origin.x - 150 * level},${axis.origin.y + 86 * level}`,
              `${axis.origin.x + 150 * level},${axis.origin.y + 86 * level}`,
              `${axis.origin.x + 212 * level},${axis.origin.y + 38 * level}`,
              `${axis.origin.x - 88 * level},${axis.origin.y + 38 * level}`,
            ].join(" ")}
            fill="none"
            stroke="#e2e8f0"
          />
        ))}
        <line x1={axis.origin.x} y1={axis.origin.y} x2={axis.pc1.x} y2={axis.pc1.y} stroke="#94a3b8" />
        <line x1={axis.origin.x} y1={axis.origin.y} x2={axis.pc2.x} y2={axis.pc2.y} stroke="#94a3b8" />
        <line x1={axis.origin.x} y1={axis.origin.y} x2={axis.pc3.x} y2={axis.pc3.y} stroke="#94a3b8" />
        <text x={axis.pc1.x + 4} y={axis.pc1.y + 4} fontSize="11" fill="#64748b">PCA3D 1</text>
        <text x={axis.pc2.x - 8} y={axis.pc2.y - 8} fontSize="11" fill="#64748b">PCA3D 2</text>
        <text x={axis.pc3.x + 4} y={axis.pc3.y - 4} fontSize="11" fill="#64748b">PCA3D 3</text>
        {projected.map((p) => (
          <circle
            key={`${p.customer_id}-${p.index}`}
            cx={p.x}
            cy={p.y}
            r={3.2 + (p.z + 1) * 1.2}
            fill={colorFor(p.segment_label)}
            opacity={0.45 + (p.z + 1) * 0.22}
            stroke="#ffffff"
            strokeWidth="0.6"
          >
            <title>{`${p.customer_id} - ${p.name || "-"}\n${p.segment_label} / Cluster ${p.cluster}\nPCA3D 1: ${decimal(p.pc1)} | PCA3D 2: ${decimal(p.pc2)} | PCA3D 3: ${decimal(p.pc3)}`}</title>
          </circle>
        ))}
      </svg>
      <ClusterLegend />
      {!points.length ? <div className="text-sm text-slate-500">Visualisasi belum tersedia.</div> : null}
    </div>
  );
}

function ClusterLegend() {
  return (
    <div className="mt-3 flex flex-wrap gap-3 text-xs text-slate-600">
      <span className="inline-flex items-center gap-1"><span className="h-2.5 w-2.5 rounded-full bg-red-600" />Low</span>
      <span className="inline-flex items-center gap-1"><span className="h-2.5 w-2.5 rounded-full bg-amber-600" />Medium</span>
      <span className="inline-flex items-center gap-1"><span className="h-2.5 w-2.5 rounded-full bg-emerald-600" />High</span>
    </div>
  );
}

function BusinessRecommendations({ profiles }) {
  return (
    <div className="grid gap-3">
      {profiles.map((profile) => {
        const detail = profile.recommendation_detail || {};
        const actions = detail.actions || [profile.business_recommendation].filter(Boolean);
        return (
          <div key={profile.cluster} className="rounded-md border border-slate-200 bg-white p-3">
            <div className="mb-2 flex flex-wrap items-center gap-2">
              <strong className="text-sm text-slate-950">Cluster {profile.cluster}</strong>
              <SegmentBadge segment={profile.segment_label} />
              <span className="text-xs text-slate-500">{fmt(profile.customer_count)} pelanggan</span>
            </div>
            <p className="text-sm font-semibold text-slate-800">{detail.headline || profile.business_recommendation}</p>
            <ul className="mt-3 grid gap-2 text-sm text-slate-600">
              {actions.slice(0, 6).map((action) => (
                <li key={action} className="rounded border border-slate-200 bg-slate-50 px-3 py-2">{action}</li>
              ))}
            </ul>
            {profile.arrow_summary ? <ArrowSummary summary={profile.arrow_summary} /> : null}
            {detail.risk ? (
              <div className="mt-3 rounded-md border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-800">
                <span className="font-semibold">Risiko: </span>{detail.risk}
              </div>
            ) : null}
          </div>
        );
      })}
      {!profiles.length ? <div className="text-sm text-slate-500">Saran cluster belum tersedia.</div> : null}
    </div>
  );
}

function ArrowSummary({ summary }) {
  return (
    <div className="mt-3 grid gap-2 sm:grid-cols-5">
      {["L", "R", "F", "M", "C"].map((code) => {
        const item = summary[code] || {};
        const good = item.status === "baik";
        return (
          <div key={code} className={cx("rounded border px-2 py-2 text-xs", good ? "border-emerald-200 bg-emerald-50 text-emerald-800" : "border-slate-200 bg-slate-50 text-slate-600")}>
            <span className="block font-bold">{code} {item.arrow || "-"}</span>
            <span>{decimal(item.value)} - {item.status || "-"}</span>
          </div>
        );
      })}
    </div>
  );
}

function CustomerTable({ rows, onSelect, selected }) {
  return (
    <div className="overflow-auto rounded-md border border-slate-200">
      <table className="w-full min-w-[1380px] text-left text-sm">
        <thead className="bg-slate-50 text-xs uppercase text-slate-500">
          <tr>
            {onSelect ? <th className="px-3 py-3">Pilih</th> : null}
            {["Customer ID", "Nama", "L", "R", "F", "M", "C", "Kombinasi LRFMC", "Cluster", "Segment Label", "Status Pembayaran", "Tepat/Terlambat", "Rekomendasi"].map((head) => <th key={head} className="px-3 py-3">{head}</th>)}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-200">
          {rows.map((row) => (
            <tr key={row.customer_id} className={cx("bg-white", selected === row.customer_id && "bg-slate-50")}>
              {onSelect ? (
                <td className="px-3 py-3"><Button variant="secondary" className="h-8 px-3" onClick={() => onSelect(row)}>Pilih</Button></td>
              ) : null}
              <td className="px-3 py-3 text-slate-700">{row.customer_id}</td>
              <td className="max-w-[220px] break-words px-3 py-3 text-slate-700">{row.name}</td>
              <td className="px-3 py-3 text-slate-700">{decimal(row.loyalty)}</td>
              <td className="px-3 py-3 text-slate-700">{decimal(row.recency)}</td>
              <td className="px-3 py-3 text-slate-700">{fmt(row.frequency)}</td>
              <td className="px-3 py-3 text-slate-700">{decimal(row.monetary)}</td>
              <td className="px-3 py-3 text-slate-700">{decimal(row.category_score)}</td>
              <td className="px-3 py-3 text-slate-700">{row.lrfmc_combination || "-"}</td>
              <td className="px-3 py-3 text-slate-700">{row.cluster ?? "-"}</td>
              <td className="px-3 py-3 text-slate-700"><SegmentBadge segment={row.segment_label || "Low-Value"} /></td>
              <td className="px-3 py-3 text-slate-700"><PaymentBadge status={row.payment_status} /></td>
              <td className="px-3 py-3 text-slate-700">{fmt(row.on_time_payments || 0)} / {fmt(row.late_payments || 0)}</td>
              <td className="max-w-[260px] break-words px-3 py-3 text-slate-700">{row.recommendation || "-"}</td>
            </tr>
          ))}
          {!rows.length ? <EmptyRow colSpan={onSelect ? 14 : 13} /> : null}
        </tbody>
      </table>
    </div>
  );
}

function Pagination({ pagination, onChange }) {
  const totalPages = Math.max(Number(pagination.total_pages || 1), 1);
  const page = Math.min(Number(pagination.page || 1), totalPages);
  const pages = Array.from(new Set([1, 2, 3, page - 1, page, page + 1, totalPages].filter((item) => item >= 1 && item <= totalPages))).sort((a, b) => a - b);
  return (
    <div className="mt-4 flex flex-wrap items-center justify-between gap-3">
      <p className="text-sm text-slate-500">Halaman {page} dari {totalPages}</p>
      <div className="flex flex-wrap gap-2">
        <Button variant="secondary" className="h-9 px-3" disabled={page <= 1} onClick={() => onChange(page - 1)}>Prev</Button>
        {pages.map((item, idx) => (
          <React.Fragment key={item}>
            {idx > 0 && item - pages[idx - 1] > 1 ? <span className="grid h-9 place-items-center px-1 text-slate-400">...</span> : null}
            <Button variant={item === page ? "primary" : "secondary"} className="h-9 px-3" onClick={() => onChange(item)}>{item}</Button>
          </React.Fragment>
        ))}
        <Button variant="secondary" className="h-9 px-3" disabled={page >= totalPages} onClick={() => onChange(page + 1)}>Next</Button>
      </div>
    </div>
  );
}

function EmptyRow({ colSpan }) {
  return (
    <tr>
      <td className="px-3 py-6 text-center text-slate-500" colSpan={colSpan}>Data tidak ditemukan.</td>
    </tr>
  );
}

function SegmentBadge({ segment }) {
  const tone = segment.includes("High") ? "green" : segment.includes("Medium") ? "amber" : "red";
  return <Badge tone={tone}>{segment}</Badge>;
}

function PaymentBadge({ status }) {
  const label = status || "Belum teridentifikasi";
  const tone = label.includes("Tepat") ? "green" : label.includes("terlambat") ? "red" : "amber";
  return <Badge tone={tone}>{label}</Badge>;
}

function CustomerDetail({ row }) {
  const interpretation = row.cluster_interpretation || (
    row.segment_label?.includes("High")
      ? "Prioritas loyalitas dan layanan premium."
      : row.segment_label?.includes("Medium")
      ? "Potensi dikembangkan melalui retensi."
      : "Jarang transaksi dan nilai transaksi rendah."
  );
  const recommendation = row.business_recommendation || row.recommendation || "-";
  const items = [
    ["Customer ID", row.customer_id],
    ["Nama Pelanggan", row.name],
    ["Nilai LRFMC", `L ${decimal(row.loyalty)} / R ${decimal(row.recency)} / F ${fmt(row.frequency)} / M ${decimal(row.monetary)} / C ${decimal(row.category_score)}`],
    ["Paket", row.category],
    ["Biaya Bulanan", fmt(row.monthly_fee)],
    ["Kombinasi LRFMC", row.lrfmc_combination],
    ["Label Segmen", row.segment_label],
    ["Cluster", row.cluster],
    ["Status Pembayaran", row.payment_status],
    ["Tepat / Terlambat", `${fmt(row.on_time_payments || 0)} / ${fmt(row.late_payments || 0)}`],
    ["Status Hasil", "Pelanggan dipilih dari tabel hasil"],
  ];
  return (
    <div className="grid min-w-0 gap-3 overflow-hidden">
      {items.map(([label, value]) => (
        <div key={label} className="grid min-w-0 gap-1 border-b border-slate-200 pb-3 sm:grid-cols-[130px_minmax(0,1fr)]">
          <span className="text-sm text-slate-500">{label}</span>
          <strong className="min-w-0 break-words text-sm text-slate-950 sm:text-right">{value ?? "-"}</strong>
        </div>
      ))}
      <div className="grid gap-3">
        <div className="break-words rounded-md border border-slate-200 bg-slate-50 p-3 text-sm text-slate-600">
          <span className="mb-1 block text-xs font-semibold uppercase text-slate-500">Interpretasi</span>
          {interpretation}
        </div>
        <div className="break-words rounded-md border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-800">
          <span className="mb-1 block text-xs font-semibold uppercase text-emerald-700">Saran Bisnis</span>
          {recommendation}
        </div>
      </div>
    </div>
  );
}

createRoot(document.getElementById("root")).render(<App />);
