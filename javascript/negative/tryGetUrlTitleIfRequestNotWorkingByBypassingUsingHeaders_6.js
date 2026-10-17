async function tryGetUrlTitleIfRequestNotWorkingByBypassingUsingHeaders(url = '', headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}, cookies = {}, allowRedirects = true, timeout = 5) {
    try {
        const axios = require("axios");
        const cheerio = require("cheerio");

        let config = {
            timeout: timeout * 1000,
            maxRedirects: allowRedirects ? 5 : 0,
            validateStatus: () => true
        };

        if (headers !== null) {
            config.headers = headers;
        }

        if (cookies && Object.keys(cookies).length > 0) {
            config.headers = config.headers || {};
            config.headers["Cookie"] = Object.entries(cookies)
                .map(([k, v]) => `${k}=${v}`)
                .join("; ");
        }

        const r = await axios.get(url, config);

        const $ = cheerio.load(r.data);

        return {
            status: r.status,
            title: $("title").text().trim(),
            headers: config.headers || {}
        };

    } catch (e) {
        return {
            status: null,
            title: "",
            error: String(e)
        };
    }
}

//(async () => { const url = "https://www.quora.com"; console.log( await tryGetUrlTitleIfRequestNotWorkingByBypassingUsingHeaders( url, null ) ); console.log( await tryGetUrlTitleIfRequestNotWorkingByBypassingUsingHeaders( url ) ); console.log( await tryGetUrlTitleIfRequestNotWorkingByBypassingUsingHeaders( url, { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.9", "Cache-Control": "no-cache", "Pragma": "no-cache" } ) ); })();
