import { mkdir } from "node:fs/promises";
import { chromium } from "playwright";

const baseUrl = process.env.README_SCREENSHOT_URL || "http://localhost:5173";
const outputDir = "docs/screenshots";

const sections = [
  { key: "login", label: "Login", file: "01-login.png", before: null },
  { key: "dashboard", label: "Dashboard", file: "02-dashboard.png", nav: "Dashboard" },
  { key: "data", label: "Data Tertanam", file: "03-data-tertanam.png", nav: "Data Tertanam" },
  { key: "process", label: "Proses Segmentasi", file: "04-proses-segmentasi.png", nav: "Proses Segmentasi" },
  { key: "result", label: "Lihat Hasil", file: "05-lihat-hasil.png", nav: "Lihat Hasil" },
];

async function waitForSettled(page) {
  await page.waitForLoadState("domcontentloaded");
  await page.waitForLoadState("networkidle").catch(() => {});
  await page.waitForTimeout(800);
  await page.getByText("Memuat data dari API...").waitFor({ state: "detached", timeout: 15000 }).catch(() => {});
}

const browser = await chromium.launch();
try {
  await mkdir(outputDir, { recursive: true });

  const loginPage = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  await loginPage.goto(baseUrl);
  await waitForSettled(loginPage);
  await loginPage.screenshot({ path: `${outputDir}/${sections[0].file}`, fullPage: true });
  await loginPage.close();

  const context = await browser.newContext({ viewport: { width: 1440, height: 1100 } });
  await context.addInitScript(() => {
    sessionStorage.setItem("isLoggedIn", "true");
    sessionStorage.setItem("sidebarCollapsed", "false");
  });

  const page = await context.newPage();
  await page.goto(baseUrl);
  await waitForSettled(page);

  for (const section of sections.slice(1)) {
    await page.getByRole("navigation").getByRole("button", { name: section.nav, exact: true }).click();
    await waitForSettled(page);
    await page.screenshot({ path: `${outputDir}/${section.file}`, fullPage: true });
  }

  await context.close();
} finally {
  await browser.close();
}

console.log(`Saved ${sections.length} screenshots to ${outputDir}`);
