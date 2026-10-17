async function tryGetLinksOfUrlIfRequestNotWorkingBypassingUsingHeaders(url = '', headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}, cookies = {}, allowRedirects = true, timeout = 5000) {
    try {
        const fetchHeaders = headers || {};

        if (Object.keys(cookies).length) {
            fetchHeaders["Cookie"] = Object.entries(cookies)
                .map(([key, value]) => `${key}=${value}`)
                .join("; ");
        }

        const response = await fetch(url, {
            method:"GET",
            headers:fetchHeaders,
            redirect:allowRedirects ? "follow" : "manual",
            signal:AbortSignal.timeout(timeout)
        });

        const html = await response.text();

        const links = [...html.matchAll(/<a[^>]*href=["']([^"']+)["'][^>]*>/gi)]
            .map(i => i[1])
            .filter(i => i);

        return [...new Set(links)].sort();

    } catch (e) {
        return [];
    }
}


// example usage:
//(async()=>{ const url = "https://www.quora.com/topics"; console.log(await tryGetLinksOfUrlIfRequestNotWorkingBypassingUsingHeaders(url, null)); console.log(await tryGetLinksOfUrlIfRequestNotWorkingBypassingUsingHeaders(url)); })();
