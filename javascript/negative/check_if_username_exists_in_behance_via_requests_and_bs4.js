/**
 * Transforms the Python Behance checker directly into pure JavaScript.
 * Runs in any standard, bare-bones JavaScript engine.
 */
async function check_if_username_exists_in_behance_via_requests_and_bs4(
    username = '',
    retries = 3,
    delay = 2,
    url = 'https://behance.net',
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9, image/avif,image/webp,*/*;q=0.8"
    },
    cookies = {},
    allow_redirects = false
) {
    // Exact Python type/strip check validation
    if (!username || typeof username !== 'string' || !username.trim()) {
        return {
            error: 'invalid <username> value',
            status: null,
            username: username,
            content: null,
            title: null,
            available: false,
            exists: false
        };
    }

    const requestHeaders = { ...headers };
    if (Object.keys(cookies).length > 0) {
        requestHeaders['Cookie'] = Object.entries(cookies)
            .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
            .join('; ');
    }

    const redirectMode = allow_redirects ? 'follow' : 'manual';
    
    // Exact string cleanup matching Python: f"{str(url).strip().strip('/')}/{str(username).strip()}"
    const cleanUrl = url.trim().replace(/\/+$/, '');
    const cleanUsername = username.trim();
    const targetUrl = `${cleanUrl}/${cleanUsername}`;

    let last_error = null;
    const sleep = (s) => new Promise(resolve => setTimeout(resolve, s * 1000));

    // Pure JavaScript replacement for Python's BeautifulSoup text comprehension chain:
    // '\n'.join([i for i in content.get_text().replace('\t','\n').strip().split('\n') if i and i.strip()])
    const processBs4TextComprehension = (htmlBlock) => {
        if (!htmlBlock) return null;
        
        // Replicates extracting text lines and tags stripping
        const cleanText = htmlBlock
            .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '') // Remove scripts
            .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')   // Remove styles
            .replace(/<[^>]*>/g, '\n')                       // Convert remaining tags to newlines
            .replace(/\t/g, '\n');                            // .replace('\t','\n')

        // Python logic line-by-line list comprehension filtering
        const processedLines = cleanText
            .split('\n')
            .map(line => line.trim())
            .filter(line => line.length > 0); // [i for i in ... if i and i.strip()]

        return processedLines.length > 0 ? processedLines.join('\n') : null; // '\n'.join(...)
    };

    for (let i = 0; i < retries; i++) {
        try {
            const response = await fetch(targetUrl, {
                method: 'GET',
                headers: requestHeaders,
                redirect: redirectMode
            });

            const htmlText = await response.text();

            // Extract Title matching: soup.title.get_text().strip()
            const titleMatch = htmlText.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
            const title = titleMatch && titleMatch[1] ? titleMatch[1].trim() : null;

            if (response.status === 200) {
                // Exact match for soup.find('div', {'id': 'site-content'})
                let contentText = null;
                const siteContentMatch = htmlText.match(/<div[^>]*id=["']site-content["'][^>]*>([\s\S]*?)$/i);
                if (siteContentMatch && siteContentMatch[1]) {
                    contentText = processBs4TextComprehension(siteContentMatch[1]);
                }

                return {
                    error: false,
                    status: 200,
                    username: username,
                    content: contentText,
                    title: title,
                    available: false,
                    exists: true
                };
            }

            if (response.status === 404) {
                // Exact match for content.find('div', {'class': 'errors-header'})
                let errorText = null;
                const errorHeaderMatch = htmlText.match(/<div[^>]*class=["'][^"']*errors-header[^"']*["'][^>]*>([\s\S]*?)<\/div>/i);
                
                if (errorHeaderMatch && errorHeaderMatch[1]) {
                    errorText = processBs4TextComprehension(errorHeaderMatch[1]);
                } else {
                    // Fallback lookup if nested
                    const siteContentMatch = htmlText.match(/<div[^>]*id=["']site-content["'][^>]*>([\s\S]*?)$/i);
                    if (siteContentMatch && siteContentMatch[1]) {
                        errorText = processBs4TextComprehension(siteContentMatch[1]);
                    }
                }

                return {
                    error: false,
                    status: 404,
                    username: username,
                    content: errorText,
                    title: title,
                    available: true,
                    exists: false
                };
            }

            last_error = `unexpected status_code ${response.status}`;
            await sleep(delay);

        } catch (e) {
            last_error = e.message;
            await sleep(delay);
        }
    }

    return {
        error: last_error,
        status: null,
        username: username,
        content: null,
        title: null,
        available: null,
        exists: null
    };
}

// --- Verification Block ---
// Since it's asynchronous JavaScript, use .then() to print the literal object dictionary immediately upon execution
//check_if_username_exists_in_behance_via_requests_and_bs4('anonymous').then(res => console.log(JSON.stringify(res, null, 2)));
//check_if_username_exists_in_behance_via_requests_and_bs4('alitakos90').then(res => console.log(JSON.stringify(res, null, 2)));
