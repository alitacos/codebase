function checkIfUsernameExistsInBehanceViaRequestsAndBs4(
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
    // 1. Initial validation
    if (!username || typeof username !== 'string' || !username.trim()) {
        return Promise.resolve({
            error: 'invalid <username> value',
            status: null,
            username: username,
            content: null,
            title: null,
            available: false,
            exists: false
        });
    }

    // Prepare headers and inject cookies if present
    const requestHeaders = { ...headers };
    if (Object.keys(cookies).length > 0) {
        requestHeaders['Cookie'] = Object.entries(cookies)
            .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
            .join('; ');
    }

    const redirectMode = allow_redirects ? 'follow' : 'manual';
    const cleanUrl = url.trim().replace(/\/+$/, '');
    const cleanUsername = username.trim();
    const targetUrl = `${cleanUrl}/${cleanUsername}`;

    // Sleep helper matching Python's time.sleep
    const sleep = (s) => new Promise(resolve => setTimeout(resolve, s * 1000));

    // Text parsing helper matching Python's content cleanup loop
    const cleanElementText = (element) => {
        if (!element) return null;
        return element.textContent
            .replace(/\t/g, '\n')
            .trim()
            .split('\n')
            .map(line => line.trim())
            .filter(line => line.length > 0)
            .join('\n');
    };

    // Async execution loop handling retries internally
    async function execute() {
        let last_error = null;

        for (let i = 0; i < retries; i++) {
            try {
                const response = await fetch(targetUrl, {
                    method: 'GET',
                    headers: requestHeaders,
                    redirect: redirectMode
                });

                const htmlText = await response.text();
                
                // Native DOMParser replaces BeautifulSoup
                const parser = new DOMParser();
                const soup = parser.parseFromString(htmlText, 'text/html');
                
                const title = soup.title ? soup.title.textContent.trim() : null;
                const content = soup.querySelector('div[id="site-content"]');

                if (response.status === 200) {
                    return {
                        error: false,
                        status: 200,
                        username: username,
                        content: cleanElementText(content),
                        title: title,
                        available: false,
                        exists: true
                    };
                }

                if (response.status === 404) {
                    const errorHeader = content ? content.querySelector('div[class="errors-header"]') : null;
                    return {
                        error: false,
                        status: 404,
                        username: username,
                        content: cleanElementText(errorHeader),
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

    return execute();
}

// --- Direct Output Invocation ---
// Resolving the promises with .then() logs the literal output object directly
//checkIfUsernameExistsInBehanceViaRequestsAndBs4('anonymous').then(console.log);
//checkIfUsernameExistsInBehanceViaRequestsAndBs4('alitakos90').then(console.log);
