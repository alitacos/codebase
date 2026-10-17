// negative
/**
 * Direct 1:1 transformation of your Python Docker Hub checker.
 * Runs in pure standard JavaScript (no node.js, no external modules).
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
    // 1:1 Translation of: if not username or not isinstance(username, str) or not str(username).strip()
    if (!username || typeof username !== 'string' || !username.trim()) {
        return {
            'error': 'invalid <username> value',
            "status": null,
            "username": username,
            "content": null,
            "title": null,
            "available": false,
            "exists": false
        };
    }

    // Build the request headers object and include cookies string if needed
    let requestHeaders = { ...headers };
    if (Object.keys(cookies).length > 0) {
        requestHeaders['Cookie'] = Object.entries(cookies)
            .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
            .join('; ');
    }

    // Exact string combination replica: f'{url.strip().rstrip('/')}/{str(username).strip().strip('/')}/'
    const cleanUrl = String(url).trim().replace(/\/+$/, '');
    const cleanUsername = String(username).trim().replace(/^\/+|\/+$/g, '');
    let targetUrl = `${cleanUrl}/${cleanUsername}/`;

    // Helpers mimicking Python's sleep and BeautifulSoup text manipulation array chain
    const sleep = (s) => new Promise(resolve => setTimeout(resolve, s * 1000));
    
    // 1:1 Replica of: '\n'.join([i for i in content.get_text().replace('\t','\n').strip().split('\n') if i and i.strip()])
    const bs4GetTextComprehension = (htmlBlock) => {
        if (!htmlBlock) return null;
        let stripped = htmlBlock.replace(/<[^>]*>/g, ' '); // Replicates extracting raw innerText
        return stripped
            .replace(/\t/g, '\n')
            .trim()
            .split('\n')
            .map(i => i.trim())
            .filter(i => i !== '' && i.length > 0)
            .join('\n');
    };

    let last_error = null;

    // 1:1 Translation of: for _ in range(retries):
    for (let attempt = 0; attempt < retries; attempt++) {
        try {
            // Native fetch with manual redirect handling to perfectly mimic Python requests engine
            let response = await fetch(targetUrl, {
                method: 'GET',
                headers: requestHeaders,
                redirect: 'manual'
            });

            // Replicating Python requests automatic redirect handling logic 
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

            // Replicating soup.title.get_text().strip()
            const titleMatch = htmlText.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
            const title = titleMatch && titleMatch[1] ? titleMatch[1].trim() : null;

            // 1:1 Translation of: if response.status_code == 200:
            if (response.status === 200) {
                // Replicating soup.find('div', {'data-testid': 'profile-header'})
                let contentText = null;
                const profileHeaderMatch = htmlText.match(/<div[^>]*data-testid=["']profile-header["'][^>]*>([\s\S]*?)<\/div>/i);
                if (profileHeaderMatch && profileHeaderMatch[1]) {
                    contentText = bs4GetTextComprehension(profileHeaderMatch[1]);
                }

                return {
                    'error': false,
                    "status": 200,
                    "username": username,
                    "content":  contentText ,
                    "title": title,
                    "available": false,
                    "exists": true
                };
            }

            // 1:1 Translation of: if response.status_code == 404:
            if (response.status === 404) {
                // Replicating soup.find('img', {'data-testid': '404page'})
                let contentText = null;
                const errorPageMatch = htmlText.match(/<img[^>]*data-testid=["']404page["'][^>]*>([\s\S]*?)(?:\/>|<\/img>)/i);
                if (errorPageMatch && errorPageMatch[1]) {
                    contentText = bs4GetTextComprehension(errorPageMatch[1]);
                }

                return {
                    'error': false,
                    "status": 404,
                    "username": username,
                    "content": contentText || "", // Empty string default matching your exact output log comment
                    "title": title,
                    "available": true,
                    "exists": false
                };
            }

            // 1:1 Translation of: last_error = f"unexpected status_code {response.status_code}"
            last_error = `unexpected status_code ${response.status}`;
            await sleep(delay);
            continue;

        } catch (e) {
            // 1:1 Translation of: except Exception as e: last_error = str(e)
            last_error = e.message;
            await sleep(delay);
        }
    }

    return {
        'error': last_error,
        "status": null,
        "username": username,
        "content": null,
        "title": null,
        "available": null,
        "exists": null
    };
}

// --- Execution Pipeline ---
// Immediate Invocation resolves the async function to log the plain dict-like outputs straight to the output panel

// (async () => { console.log(await check_if_username_exists_in_docker_hub_via_requests_and_bs4('alitakos90')); console.log(await check_if_username_exists_in_docker_hub_via_requests_and_bs4('anon')); })();