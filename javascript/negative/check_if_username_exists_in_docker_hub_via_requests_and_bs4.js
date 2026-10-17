/**
 * Direct 1:1 behavioral match of the corrected Python function.
 * Evaluates SPA hydration contexts natively without third party parsing tools.
 */
async function check_if_username_exists_in_docker_hub_via_requests_and_bs4(
    username = '',
    retries = 3,
    delay = 2,
    url = "https://docker.com",
    cookies = {},
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    },
    allow_redirects = false
) {
    if (!username || typeof username !== 'string' || !username.trim()) {
        return { 'error': 'invalid <username> value', "status": null, "username": username, "content": null, "title": null, "available": false, "exists": false };
    }

    let requestHeaders = { ...headers };
    if (Object.keys(cookies).length > 0) {
        requestHeaders['Cookie'] = Object.entries(cookies)
            .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
            .join('; ');
    }

    const cleanUrl = String(url).trim().replace(/\/+$/, '');
    const cleanUsername = String(username).trim().replace(/^\/+|\/+$/g, '');
    let targetUrl = `${cleanUrl}/${cleanUsername}/`;

    const sleep = (s) => new Promise(resolve => setTimeout(resolve, s * 1000));
    let last_error = null;

    for (let attempt = 0; attempt < retries; attempt++) {
        try {
            let response = await fetch(targetUrl, {
                method: 'GET',
                headers: requestHeaders,
                redirect: 'manual'
            });

            if ([301, 302, 307, 308].includes(response.status)) {
                if (allow_redirects) {
                    const location = response.headers.get('location');
                    if (location) {
                        targetUrl = location;
                        response = await fetch(targetUrl, { method: 'GET', headers: requestHeaders, redirect: 'manual' });
                    }
                }
            }

            const htmlText = await response.text();

            // Extract initial header meta tags matching titles
            const titleMatch = htmlText.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
            let title = titleMatch ? titleMatch[1].trim() : (response.status === 200 ? username : "Page Not Found");

            if (response.status === 200) {
                let contentText = "";
                
                // Parse out hydration script tags since content blocks render fully blank on raw text reads
                const stateMatch = htmlText.match(/const\s+state\s*=\s*(\{[\s\S]*?\});/);
                if (stateMatch) {
                    try {
                        const cleanJson = stateMatch[1];
                        const stateData = JSON.parse(cleanJson);
                        const profile = stateData.profile || {};
                        const fullName = (profile.full_name || "").trim();
                        const company = (profile.company || "").trim();
                        const locationStr = (profile.location || "").trim();
                        
                        const parts = [username, fullName, company, locationStr];
                        contentText = parts.filter(p => p).join(" ");
                    } catch (e) {
                        // fallback execution
                    }
                }

                if (!contentText) {
                    contentText = `${username} Community User`;
                }

                return {
                    'error': false,
                    "status": 200,
                    "username": username,
                    "content": contentText.trim(),
                    "title": title,
                    "available": false,
                    "exists": true
                };
            }

            if (response.status === 404) {
                return {
                    'error': false,
                    "status": 404,
                    "username": username,
                    "content": '',
                    "title": 'Page Not Found',
                    "available": true,
                    "exists": false
                };
            }

            last_error = `unexpected status_code ${response.status}`;
            await sleep(delay);
            continue;

        } catch (e) {
            last_error = e.message;
            await sleep(delay);
        }
    }

    return { 'error': last_error, "status": null, "username": username, "content": null, "title": null, "available": null, "exists": null };
}

// --- Verification Pipeline ---
//(async () => { console.log(await check_if_username_exists_in_docker_hub_via_requests_and_bs4('alitakos90')); console.log(await check_if_username_exists_in_docker_hub_via_requests_and_bs4('anon')); })();