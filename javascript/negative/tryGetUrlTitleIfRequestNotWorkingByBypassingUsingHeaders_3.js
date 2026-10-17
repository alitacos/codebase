async function tryGetUrlTitleIfRequestNotWorkingByBypassingUsingHeaders(url = '', headers = null, cookies = {}, allowRedirects = true, timeout = 5000) {
    try {
        const defaultHeaders = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language":"en-US,en;q=0.9",
            "Cache-Control":"no-cache",
            "Pragma":"no-cache",
            "Upgrade-Insecure-Requests":"1"
        };

        const finalHeaders = {
            ...defaultHeaders,
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

        const title = html.match(/<title[^>]*>(.*?)<\/title>/is);

        return title ? title[1].trim() : '';

    } catch (e) {
        return '';
    }
}
 


//(async()=>{ const url = "https://www.quora.com/topics"; console.log(await tryGetUrlTitleIfRequestNotWorkingByBypassingUsingHeaders(url, null)); console.log(await tryGetUrlTitleIfRequestNotWorkingByBypassingUsingHeaders(url)); })();
