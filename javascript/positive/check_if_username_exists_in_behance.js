async function check_if_username_exists_in_behance(
    username = '',
    retries = 3,
    delay = 2,
    url = 'https://www.behance.net/',
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9, image/avif,image/webp,*/*;q=0.8"
    },
    cookies = {},
    allow_redirects = false
) {
    // 1:1 Translation of: if not username or not isinstance(username, str) or not str(username).strip()
    if (!username || typeof username !== 'string' || !username.trim()) {
        return { 'error': 'invalid <username> value', "status": null, "username": username, "content": null, "title": null, "available": false, "exists": false };
    }

    // Convert cookies object to a string header format if provided
    let requestHeaders = { ...headers };
    if (Object.keys(cookies).length > 0) {
        requestHeaders['Cookie'] = Object.entries(cookies)
            .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
            .join('; ');
    }

    // Exact string combination: f"{str(url).strip().strip('/')}/{str(username).strip()}"
    let targetUrl = `${String(url).trim().replace(/\/+$/, '')}/${String(username).trim()}`;

    // Helper functions for time.sleep and BeautifulSoup list comprehension formatting
    const sleep = (s) => new Promise(resolve => setTimeout(resolve, s * 1000));
    
    // 1:1 Replica of: '\n'.join([i for i in content.get_text().replace('\t','\n').strip().split('\n') if i and i.strip()])
    const bs4GetTextComprehension = (htmlBlock) => {
        if (!htmlBlock) return null;
        let stripped = htmlBlock.replace(/<[^>]*>/g, ' '); // Basic innerText extraction
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
            // JavaScript fetch requires 'manual' to handle redirects explicitly like Python requests
            let response = await fetch(targetUrl, {
                method: 'GET',
                headers: requestHeaders,
                redirect: 'manual' 
            });

            // Replicating Python requests redirect behavior
            if ([301, 302, 303, 307, 308].includes(response.status)) {
                if (allow_redirects) {
                    const location = response.headers.get('location');
                    if (location) {
                        targetUrl = location; // Follow redirect target address
                        response = await fetch(targetUrl, { method: 'GET', headers: requestHeaders, redirect: 'manual' });
                    }
                }
            }

            const htmlText = await response.text();

            // Replicating soup.title.get_text().strip()
            const titleMatch = htmlText.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
            const title = titleMatch && titleMatch[1] ? titleMatch[1].trim() : null;

            // Replicating soup.find('div', {'id': 'site-content'})
            const siteContentMatch = htmlText.match(/<div[^>]*id=["']site-content["'][^>]*>([\s\S]*?)<\/div>/i);
            const contentBlock = siteContentMatch && siteContentMatch[1] ? siteContentMatch[1] : null;

            // 1:1 Translation of: if response.status_code == 200:
            if (response.status === 200) {
                return { 
                    'error': false, 
                    "status": 200, 
                    "username": username, 
                    "content": contentBlock ? bs4GetTextComprehension(contentBlock) : null, 
                    "title": title, 
                    "available": false, 
                    "exists": true 
                };
            }

            // 1:1 Translation of: if response.status_code == 404:
            if (response.status === 404) {
                let errorText = null;
                if (contentBlock) {
                    // Replicating content.find('div', {'class': 'errors-header'})
                    const errorsHeaderMatch = contentBlock.match(/<div[^>]*class=["'][^"']*errors-header[^"']*["'][^>]*>([\s\S]*?)<\/div>/i);
                    if (errorsHeaderMatch && errorsHeaderMatch[1]) {
                        errorText = bs4GetTextComprehension(errorsHeaderMatch[1]);
                    }
                }

                return { 
                    'error': false, 
                    "status": 404, 
                    "username": username, 
                    "content": errorText, 
                    "title": title, 
                    "available": true, 
                    "exists": false 
                };
            }

            // 1:1 Translation of: last_error = f'unexpected status_code {response.status_code}'
            last_error = `unexpected status_code ${response.status}`;
            await sleep(delay);
            continue;

        } catch (e) {
            // 1:1 Translation of: except Exception as e: last_error = str(e)
            last_error = e.message;
            await sleep(delay);
        }
    }

    return { 'error': last_error, "status": null, "username": username, "content": null, "title": null, "available": null, "exists": null };
}

// --- Execution Pipeline ---
// (async () => { console.log(await check_if_username_exists_in_behance('anonymous')); console.log(await check_if_username_exists_in_behance_via_requests_and_bs4('alitakos90')); })();