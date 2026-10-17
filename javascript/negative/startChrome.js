delete global.startChrome;

const { spawn } = require("child_process");
const http = require("http");

global.startChrome = async function ({
  display = ":99",
  width = 1920,
  height = 1080,
  cdpPort = 9222,
  userDataDir = "/tmp/chrome-profile",
  chromeBinary = "chromium"
} = {}) {

  function waitForCDP(timeout = 15000) {
    return new Promise((resolve, reject) => {
      const start = Date.now();

      const check = () => {
        http.get(`http://127.0.0.1:${cdpPort}/json`, res => {
          let data = "";

          res.on("data", d => data += d);

          res.on("end", () => {
            try {
              const json = JSON.parse(data);
              if (json[0]?.webSocketDebuggerUrl) {
                resolve(json[0].webSocketDebuggerUrl);
                return;
              }
            } catch {}

            retry();
          });

        }).on("error", retry);
      };

      function retry() {
        if (Date.now() - start > timeout) {
          reject(new Error("Chrome CDP timeout"));
          return;
        }
        setTimeout(check, 300);
      }

      check();
    });
  }


  const xvfb = spawn("Xvfb", [
    display,
    "-screen",
    "0",
    `${width}x${height}x24`
  ], {
    detached: true,
    stdio: "inherit"
  });


  const chrome = spawn(chromeBinary, [
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--remote-debugging-address=0.0.0.0",
    `--remote-debugging-port=${cdpPort}`,
    `--user-data-dir=${userDataDir}`,
    "--start-maximized"
  ], {
    env: {
      ...process.env,
      DISPLAY: display
    },
    detached: true,
    stdio: "inherit"
  });


  const wsUrl = await waitForCDP();

  return {
    xvfb,
    chrome,
    wsUrl,
    cdpHttp: `http://127.0.0.1:${cdpPort}`
  };
};

 