import { chromium } from "playwright";
import { spawn, execSync } from "child_process";
import fs from "fs";

let xvfbProcess;
let browser;
let context;
let page;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function startXvfb() {
  console.log("Starting Xvfb...");

  try {
    execSync("rm -f /tmp/.X99-lock");
  } catch {}

  xvfbProcess = spawn(
    "Xvfb",
    [
      ":99",
      "-screen",
      "0",
      "1280x720x24",
      "-ac",
      "-nolisten",
      "tcp"
    ],
    {
      stdio: "ignore"
    }
  );

  xvfbProcess.on("error", err => {
    console.error("Xvfb error:", err);
  });

  process.env.DISPLAY = ":99";

  // wait until X server is ready
  await sleep(1000);

  console.log("Xvfb ready on DISPLAY=:99");
}


async function startBrowser() {

  await startXvfb();

  console.log("Launching Chromium...");

  browser = await chromium.launch({
    headless: false,
    args: [
      "--no-sandbox",
      "--disable-setuid-sandbox",
      "--disable-dev-shm-usage",
      "--window-size=1280,720"
    ]
  });


  context = await browser.newContext({
    viewport: {
      width:1280,
      height:720
    }
  });


  page = await context.newPage();

  await page.goto("https://example.com");

  console.log("Browser started");

  // save screenshot
  const img = await page.screenshot({
    type:"png"
  });

  fs.writeFileSync(
    "browser.png",
    img
  );

  console.log("Screenshot saved: browser.png");
}


startBrowser();