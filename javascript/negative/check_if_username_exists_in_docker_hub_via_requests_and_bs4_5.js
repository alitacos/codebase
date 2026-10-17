/**
 * Exact matching transformation of the corrected Python Docker Hub checker.
 * Built for direct engine run pipelines without node.js or third-party wrappers.
 */
async function check_if_username_exists_in_docker_hub_via_requests_and_bs4(
    username = '',
    retries = 3,
    delay = 2,
    url = "https://hub.docker.com/u/",
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
    
    const bs4GetTextComprehension = (htmlBlock) => {
        if (!htmlBlock) return "";
        let stripped = htmlBlock.replace(/<[^>]*>/g, ' '); 
        return stripped
            .replace(/\t/g, '\n')
            .trim()
            .split('\n')
            .map(i => i.trim())
            .filter(i => i !== '' && i.length > 0)
            .join('\n');
    };

    let last_error = null;

    for (let attempt = 0; attempt < retries; attempt++) {
        try {
            let response = await fetch(targetUrl, {
                method: 'GET',
                headers: requestHeaders,
                redirect: 'manual'
            });

            // FIXED: Added the redirection status codes array to fix the Unexpected token '.' error
            if ([301, 302, 303, 307, 308].includes(response.status)) {
                if (allow_redirects) {
                    const location = response.headers.get('location');
                    if (location) {
                        targetUrl = location;
                        response = await fetch(targetUrl, { method: 'GET', headers: requestHeaders, redirect: 'manual' });
                    }
                }
            }

            const htmlText = await response.text();

            // FIXED: Extract only the inner matched group capture index [1] to avoid saving raw HTML <title> tags
            const titleMatch = htmlText.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
            const title = titleMatch && titleMatch[1] ? titleMatch[1].trim() : (response.status === 200 ? username : "Page Not Found");

            if (response.status === 200) {
                let contentText = "";
                const profileHeaderMatch = htmlText.match(/<div[^>]*data-testid=["']profile-header["'][^>]*>([\s\S]*?)<\/div>/i);
                
                if (profileHeaderMatch && profileHeaderMatch[1]) {
                    contentText = bs4GetTextComprehension(profileHeaderMatch[1]);
                }
                
                // Fallback check matching Python text rendering
                if (!contentText || contentText.trim() === "") {
                    contentText = `${username} Community User`;
                }

                return {
                    'error': false,
                    "status": 200,
                    "username": username,
                    "content": contentText,
                    "title": title,
                    "available": false,
                    "exists": true
                };
            }

            if (response.status === 404) {
                // Returns an empty string for content, matching the Python script exactly
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

// --- Direct Console Execution Output Pipeline ---
//(async () => { console.log(await check_if_username_exists_in_docker_hub_via_requests_and_bs4('alitakos90')); console.log(await check_if_username_exists_in_docker_hub_via_requests_and_bs4('anon')); })();