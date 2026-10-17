async function tryGetUrlTitleIfRequestNotWorkingByBypassingUsingHeadersViaCheerio(url = '', headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}, cookies = {}, allowRedirects = true, timeout = 10000) {
    try {
        const cheerio = require("cheerio");

        const finalHeaders = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            ...(headers || {})
        };

        if (Object.keys(cookies).length) {
            finalHeaders["Cookie"] = Object.entries(cookies)
                .map(([key,value]) => `${key}=${value}`)
                .join("; ");
        }

        const response = await fetch(url, {
            method:"GET",
            headers:finalHeaders,
            redirect:allowRedirects ? "follow" : "manual",
            signal:AbortSignal.timeout(timeout)
        });

        const html = await response.text();

        const $ = cheerio.load(html);

        return $("title").first().text().trim();

    } catch (e) {
        console.log(String(e));
        return "";
    }
}


//(async()=>{
//    const url = "https://www.quora.com";

//    console.log(await tryGetUrlTitleIfRequestNotWorkingByBypassingUsingHeadersViaCheerio(url));
//})();