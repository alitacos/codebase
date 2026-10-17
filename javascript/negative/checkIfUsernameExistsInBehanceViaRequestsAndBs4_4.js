/**
 * Überprüft, ob ein Benutzername auf Behance existiert.
 */
async function checkIfUsernameExistsInBehanceViaRequestsAndBs4(
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
    // Validierung des Usernamens
    if (!username || typeof username !== 'string' || !username.trim()) {
        return { error: 'invalid <username> value', status: null, username: username, content: null, title: null, available: false, exists: false };
    }

    // Cookies in den Header-String formatieren
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

    let last_error = null;
    const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

    // Hilfsfunktion zur Textbereinigung (Ersatz für Pythons Listen-Verständnis)
    const cleanText = (element) => {
        if (!element) return null;
        return element.textContent
            .replace(/\t/g, '\n')
            .split('\n')
            .map(line => line.trim())
            .filter(line => line.length > 0)
            .join('\n');
    };

    for (let i = 0; i < retries; i++) {
        try {
            const response = await fetch(targetUrl, {
                method: 'GET',
                headers: requestHeaders,
                redirect: redirectMode
            });

            const htmlText = await response.text();
            
            // Nativer Browser-Parser (Ersatz für BeautifulSoup)
            const parser = new DOMParser();
            const soup = parser.parseFromString(htmlText, 'text/html');

            const content = soup.getElementById('site-content');
            const title = soup.title ? soup.title.trim() : null;

            if (response.status === 200) {
                return {
                    error: false,
                    status: 200,
                    username: username,
                    content: cleanText(content),
                    title: title,
                    available: false,
                    exists: true
                };
            }

            if (response.status === 404) {
                const errorsHeader = content ? content.querySelector('.errors-header') : null;
                return {
                    error: false,
                    status: 404,
                    username: username,
                    content: cleanText(errorsHeader),
                    title: title,
                    available: true,
                    exists: false
                };
            }

            last_error = `unexpected status_code ${response.status}`;
            await sleep(delay * 1000);

        } catch (e) {
            last_error = e.message;
            await sleep(delay * 1000);
        }
    }

    return { error: last_error, status: null, username: username, content: null, title: null, available: null, exists: null };
}

// --- Beispiel für die Verwendung (Exakt wie im Python-Skript) ---
// (async () => { console.log(await checkIfUsernameExistsInBehanceViaRequestsAndBs4('anonymous')); console.log(await checkIfUsernameExistsInBehanceViaRequestsAndBs4('alitakos90')); })();