async function showBrowserInCell(page) {
  const screenshot = await page.screenshot({
    type: "png"
  });

  const base64 = screenshot.toString("base64");

  console.log(
    `<img src="data:image/png;base64,${base64}" width="1280"/>`
  );
}
await showBrowserInCell(activePage);