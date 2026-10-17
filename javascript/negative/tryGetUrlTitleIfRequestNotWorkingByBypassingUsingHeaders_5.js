async function tryGetUrlTitleIfRequestNotWorkingByBypassingUsingHeaders(url = '', headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}, cookies = {}, allowRedirects = true, timeout = 5) {
    try {
        const https = require("https");

        const defaultHeaders = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br"
        };

        const finalHeaders = headers === null ? {} : headers;

        const cookieHeader = Object.keys(cookies).length
            ? Object.entries(cookies).map(([k,v]) => `${k}=${v}`).join("; ")
            : null;

        if (cookieHeader) {
            finalHeaders["Cookie"] = cookieHeader;
        }

        const response = await fetch(url, {
            method: "GET",
            headers: finalHeaders,
            redirect: allowRedirects ? "follow" : "manual",
            signal: AbortSignal.timeout(timeout * 1000)
        });

        const html = await response.text();

        const match = html.match(/<title[^>]*>(.*?)<\/title>/is);

        return {
            status: response.status,
            title: match ? match[1].trim() : '',
            headers: finalHeaders
        };

    } catch (e) {
        return {
            status: null,
            title: '',
            error: String(e)
        };
    }
}
//(async()=>{ const url = "https://www.quora.com"; console.log(await tryGetUrlTitleIfRequestNotWorkingByBypassingUsingHeaders(url, null)); console.log(await tryGetUrlTitleIfRequestNotWorkingByBypassingUsingHeaders(url)); console.log(await tryGetUrlTitleIfRequestNotWorkingByBypassingUsingHeaders(url, { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.9" })); })();