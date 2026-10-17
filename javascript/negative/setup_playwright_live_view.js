import express from "express";

const app = express();

let latestScreenshot = "";

app.get("/browser", (req, res) => {
  res.send(`
    <html>
    <body style="margin:0">
      <img id="screen" width="1280">

      <script>
        setInterval(() => {
          document.getElementById("screen").src =
            "/screenshot?t=" + Date.now();
        }, 500);
      </script>
    </body>
    </html>
  `);
});


app.get("/screenshot", (req,res)=>{
  res.setHeader("Content-Type","image/jpeg");
  res.send(Buffer.from(latestScreenshot,"base64"));
});


setInterval(async()=>{
  if(activePage){
    const buf = await activePage.screenshot({
      type:"jpeg",
      quality:70
    });

    latestScreenshot = buf.toString("base64");
  }
},500);


app.listen(3000);