async function tryGetUrlTitle(url = '', headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}, cookies = {}, allowRedirects = true, timeout = 5) {
    try {
        const { request } = require("undici");

        let finalHeaders = {};

        if (headers !== null) {
            finalHeaders = headers;
        }

        if (cookies && Object.keys(cookies).length) {
            finalHeaders.Cookie = Object.entries(cookies)
                .map(([k,v]) => `${k}=${v}`)
                .join("; ");
        }

        const response = await request(url, {
            headers: finalHeaders,
            maxRedirections: allowRedirects ? 5 : 0,
            headersTimeout: timeout * 1000,
            bodyTimeout: timeout * 1000
        });

        const html = await response.body.text();

        const titleMatch = html.match(/<title[^>]*>(.*?)<\/title>/i);

        return {
            status: response.statusCode,
            title: titleMatch ? titleMatch[1].trim() : ""
        };

    } catch (e) {
        return {
            status: null,
            title: "",
            error: String(e)
        };
    }
}


//(async () => { console.log( await tryGetUrlTitle( "https://www.quora.com" ) ); console.log( await tryGetUrlTitle( "https://www.quora.com", null ) ); })();