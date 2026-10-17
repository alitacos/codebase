async function tryGetUrlTitleIfRequestNotWorkingByBypassingUsingHeaders(url = '', headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}, cookies = {}, allowRedirects = true, timeout = 5) {
    try {
        const controller = new AbortController();
        const timer = setTimeout(() => controller.abort(), timeout * 1000);

        let options = {
            method: "GET",
            signal: controller.signal,
            redirect: allowRedirects ? "follow" : "manual"
        };

        if (headers !== null) {
            options.headers = headers;
        }

        if (cookies && Object.keys(cookies).length) {
            options.headers = options.headers || {};
            options.headers["Cookie"] = Object.entries(cookies)
                .map(([k, v]) => `${k}=${v}`)
                .join("; ");
        }

        const response = await fetch(url, options);

        clearTimeout(timer);

        const html = await response.text();

        const match = html.match(/<title[^>]*>(.*?)<\/title>/i);

        return {
            status: response.status,
            title: match ? match[1].trim() : ""
        };

    } catch (e) {
        return {
            status: null,
            title: "",
            error: String(e)
        };
    }
}

//(async () => { const url = "https://www.quora.com"; console.log(await tryGetUrlTitleIfRequestNotWorkingByBypassingUsingHeaders(url, null)); console.log(await tryGetUrlTitleIfRequestNotWorkingByBypassingUsingHeaders(url)); console.log(await tryGetUrlTitleIfRequestNotWorkingByBypassingUsingHeaders( url, { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.9" } )); })();