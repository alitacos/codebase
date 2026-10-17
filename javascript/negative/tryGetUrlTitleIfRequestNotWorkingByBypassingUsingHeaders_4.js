async function tryGetUrlTitleIfRequestNotWorkingByBypassingUsingHeaders(url = '', headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}, cookies = {}, allowRedirects = true, timeout = 5000) {
    try {
        const finalHeaders = headers || {};

        if (Object.keys(cookies).length) {
            finalHeaders["Cookie"] = Object.entries(cookies)
                .map(([key,value]) => `${key}=${value}`)
                .join("; ");
        }

        const response = await fetch(url, {
            headers: finalHeaders,
            redirect: allowRedirects ? "follow" : "manual",
            signal: AbortSignal.timeout(timeout)
        });

        const html = await response.text();

        const title = html.match(/<title[^>]*>(.*?)<\/title>/i);

        return title ? title[1].trim() : "";

    } catch (e) {
        return "";
    }
}


// example usage:
//(async()=>{ const url = "https://www.quora.com"; console.log(await tryGetUrlTitleIfRequestNotWorkingByBypassingUsingHeaders(url, null)); console.log(await tryGetUrlTitleIfRequestNotWorkingByBypassingUsingHeaders(url)); })();