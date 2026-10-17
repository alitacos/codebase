const { spawn } = require("child_process");

const chrome = spawn("google-chrome", [
  "--no-sandbox",
  "--remote-debugging-port=9222"
], {
  detached: true,
  stdio: "ignore"
});

console.log("Chrome started");