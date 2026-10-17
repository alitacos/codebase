const axios = require("axios");
async function trackPackageByTrackingCodeViaPostdirektViaAxios(
    trackingCode = "",
    retries = 3,
    headers = null,
    cookies = null
) {
    if (!trackingCode) {
        return {
            error: "Failed to retrieve data.",
            status: "missing tracking_code"
        };
    }

    const url =
        `https://www.deutschepost.de/int-verfolgen/data/search?piececode=${encodeURIComponent(trackingCode)}&inputSearch=true&language=de`;

    if (!headers) {
        headers = { accept: "application/json", "accept-encoding": "gzip, deflate, br, zstd", "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7", "content-type": "application/json", referer: "https://www.deutschepost.de/de/s/sendungsverfolgung.html", "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"', "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": '"Windows"', "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/134.0.0.0 Safari/537.36", "verfolgen-csrf-token": "undefined", "verfolgen-wg": "null" };
    }

    try {
        for (let attempt = 0; attempt < retries; attempt++) {
            try {
                const response = await axios.get(url, {
                    headers,
                    ...(cookies
                        ? {
                              headers: {
                                  ...headers,
                                  Cookie: Object.entries(cookies)
                                      .map(([key, value]) => `${key}=${value}`)
                                      .join("; ")
                              }
                          }
                        : {}),
                    validateStatus: () => true
                });

                if (response.status === 200) {
                    return response.data;
                }

                if (response.status === 429) {
                    console.log(
                        `Rate limited. Retrying in 5 seconds... (Attempt ${attempt + 1})`
                    );

                    await new Promise(resolve => setTimeout(resolve, 5000));
                    continue;
                }

                if (response.status !== 200 && response.status !== 429) {
                    return {
                        error: "Failed to retrieve data.",
                        status_code: response.status
                    };
                }

            } catch (e) {
                if (attempt === retries - 1) {
                    throw e;
                }
            }
        }

    } catch (e) {
        return {
            error: "Failed to retrieve data.",
            status: String(e)
        };
    }
}


// Example usage
//(async () => { const trackingInfo = await trackPackageByTrackingCodeViaPostdirektViaAxios( "6666666666666" ); console.log(trackingInfo); })();