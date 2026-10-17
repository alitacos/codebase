async function tryGetUrlTitleIfRequestNotWorkingByBypassingUsingHeaders(url = '', headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}, cookies = {}, allowRedirects = true, timeout = 5) {
    try {
        const axios = require("axios");
        const cheerio = require("cheerio");

        const config = {
            timeout: timeout * 1000,
            maxRedirects: allowRedirects ? 5 : 0,
            validateStatus: () => true
        };

        if (headers !== null) {
            config.headers = headers;
        }

        if (Object.keys(cookies).length) {
            config.headers = config.headers || {};
            config.headers["Cookie"] = Object.entries(cookies)
                .map(([k,v]) => `${k}=${v}`)
                .join("; ");
        }

        const r = await axios.get(url, config);

        const $ = cheerio.load(r.data);

        return {
            status: r.status,
            title: $("title").first().text().trim()
        };

    } catch (e) {
        return {
            status: null,
            title: ''
        };
    }
}

//(async()=>{ const url = "https://www.quora.com"; console.log(await tryGetUrlTitleIfRequestNotWorkingByBypassingUsingHeaders(url, null)); console.log(await tryGetUrlTitleIfRequestNotWorkingByBypassingUsingHeaders(url)); })();
 