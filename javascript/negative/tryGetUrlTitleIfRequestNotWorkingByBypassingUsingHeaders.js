async function tryGetUrlTitleIfRequestNotWorkingByBypassingUsingHeaders(url = '', headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}, cookies = {}, allowRedirects = true, timeout = 5000) {
    try {
        const finalHeaders = headers ? {...headers} : {};

        if (Object.keys(cookies).length) {
            finalHeaders["Cookie"] = Object.entries(cookies)
                .map(([key,value]) => `${key}=${value}`)
                .join("; ");
        }

        const response = await fetch(url, {
            headers:finalHeaders,
            redirect:allowRedirects ? "follow" : "manual",
            signal:AbortSignal.timeout(timeout)
        });

        const html = await response.text();

        const parser = new DOMParser();
        const document = parser.parseFromString(html, "text/html");

        return document.querySelector("title")?.textContent.trim() || "";

    } catch (e) {
        return e;
    }
}