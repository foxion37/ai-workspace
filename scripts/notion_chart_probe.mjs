#!/usr/bin/env node

import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const ROOT = "/Users/barq";
const TARGETS_PATH = path.join(
  ROOT,
  "developer/projects/ai-workspace/config/notion_work_note_targets.json",
);
const ARTIFACT_ROOT = path.join(
  ROOT,
  ".orchestra/artifacts/notion-chart-probe",
);

function parseArgs(argv) {
  const out = {
    browserPath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    headless: false,
    profileDir: path.join(ROOT, ".orchestra/browser-profiles/notion-chart"),
    screenshot: true,
    url: null,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (token === "--headless") out.headless = true;
    else if (token === "--no-screenshot") out.screenshot = false;
    else if (token === "--browser-path") out.browserPath = argv[index + 1];
    else if (token === "--url") out.url = argv[index + 1];
    else if (token === "--profile-dir") out.profileDir = argv[index + 1];
    if (
      token === "--url" ||
      token === "--profile-dir" ||
      token === "--browser-path"
    ) index += 1;
  }

  return out;
}

function loadDefaultUrl() {
  const targets = JSON.parse(fs.readFileSync(TARGETS_PATH, "utf8"));
  return `https://www.notion.so/${targets.session_reports.database_id.replaceAll("-", "")}`;
}

async function loadPlaywright() {
  try {
    return await import("playwright");
  } catch (error) {
    const lines = [
      "Playwright is not installed for this repo.",
      "Install it in /Users/barq/developer/projects/ai-workspace before running this probe.",
      "Suggested commands:",
      "  npm init -y",
      "  npm install --save-dev playwright",
      "",
      "This probe is designed for an authenticated browser profile and keeps chart creation as a dry-run check.",
    ];
    console.error(lines.join("\n"));
    process.exitCode = 2;
    return null;
  }
}

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function ensureBrowser(browserPath) {
  if (!fs.existsSync(browserPath)) {
    console.error(`Chrome executable not found: ${browserPath}`);
    console.error("Pass --browser-path with a valid Chrome-family executable.");
    process.exit(2);
  }
}

function timestamp() {
  return new Date().toISOString().replaceAll(":", "-");
}

function summarizeVisibleText(text) {
  return text.replace(/\s+/g, " ").trim().slice(0, 500);
}

function loginGateDetected(text) {
  const loginMarkers = [
    "Log in",
    "log in to your notion account",
    "sign in to see this page",
    "continue with google",
    "continue with apple",
    "continue with microsoft",
    "passkey",
    "sso",
    "이메일",
    "로그인",
  ];
  const lowered = text.toLowerCase();
  return loginMarkers.some((marker) => lowered.includes(marker));
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const targetUrl = args.url || loadDefaultUrl();
  const stamp = timestamp();
  const artifactDir = path.join(ARTIFACT_ROOT, stamp);
  ensureDir(artifactDir);
  ensureDir(args.profileDir);
  ensureBrowser(args.browserPath);

  const playwright = await loadPlaywright();
  if (!playwright) return;

  const { chromium } = playwright;
  const context = await chromium.launchPersistentContext(args.profileDir, {
    executablePath: args.browserPath,
    headless: args.headless,
    viewport: { width: 1600, height: 1100 },
  });

  try {
    const page = context.pages()[0] || (await context.newPage());
    await page.goto(targetUrl, { waitUntil: "domcontentloaded", timeout: 60000 });
    await page.waitForTimeout(4000);

    const bodyText = await page.locator("body").innerText();
    const gateDetected = loginGateDetected(bodyText);
    const authenticated = !gateDetected;
    const addViewCandidates = await page
      .locator("button, [role='button']")
      .evaluateAll((nodes) =>
        nodes
          .map((node) => node.textContent?.replace(/\s+/g, " ").trim() || "")
          .filter(Boolean)
          .filter((value) =>
            ["View", "Add a view", "New view", "차트", "보기", "새 보기"].some((token) =>
              value.includes(token),
            ),
          )
          .slice(0, 20),
      );

    const report = {
      targetUrl,
      profileDir: args.profileDir,
      loginGateDetected: gateDetected,
      authenticated,
      title: await page.title(),
      bodyPreview: summarizeVisibleText(bodyText),
      candidateButtons: addViewCandidates,
      nextAction: authenticated
        ? "Selectors are visible enough to attempt a chart-view creation flow next."
        : "Sign into Notion in this profile once, then rerun the probe.",
    };

    fs.writeFileSync(
      path.join(artifactDir, "report.json"),
      `${JSON.stringify(report, null, 2)}\n`,
      "utf8",
    );

    if (args.screenshot) {
      await page.screenshot({
        path: path.join(artifactDir, "page.png"),
        fullPage: true,
      });
    }

    console.log(JSON.stringify(report, null, 2));
  } finally {
    await context.close();
  }
}

main().catch((error) => {
  console.error(error instanceof Error ? error.stack : String(error));
  process.exitCode = 1;
});
