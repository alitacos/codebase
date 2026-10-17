/**
 * Überprüft, ob ein Benutzername auf Behance existiert (Reines Browser-JavaScript).
 */
async function checkIfUsernameExistsInBehanceViaFetchAndDOMParser({
    username = '',
    retries = 3,
    delay = 2,
    url = 'https://www.behance.net/',
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    },
    cookies = {},
    allowRedirects = false
} = {}) {
    
    // Validierung des Usernamens
    if (!username || typeof username !== 'string' || !username.trim()) {
        return { error: 'invalid <username> value', status: null, username: username, content: null, title: null, available: false, exists: false };
    }

    // Header vorbereiten (Browser steuern User-Agent und Cookies meist selbst)
    const requestHeaders = { ...headers };
    if (Object.keys(cookies).length > 0) {
        requestHeaders['Cookie'] = Object.entries(cookies)
            .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
            .join('; ');
    }

    const redirectMode = allowRedirects ? 'follow' : 'manual';
    const cleanUrl = url.trim().replace(/\/+$/, '');
    const cleanUsername = username.trim();
    const targetUrl = `${cleanUrl}/${cleanUsername}`;

    let lastError = null;

    // Helper für das Delay (Ersatz für time.sleep)
    const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

    // Hilfsfunktion zur Textbereinigung (Ersatz für Pythons Listen-Verständnis & strip/split)
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
            
            // Nativer DOMParser des Browsers (Ersatz für BeautifulSoup)
            const parser = new DOMParser();
            const doc = parser.parseFromString(htmlText, 'text/html');

            const siteContent = doc.getElementById('site-content');
            const title = doc.title ? doc.title.trim() : null;

            if (response.status === 200) {
                return {
                    error: false,
                    status: 200,
                    username: username,
                    content: cleanText(siteContent),
                    title: title,
                    available: false,
                    exists: true
                };
            }

            if (response.status === 404) {
                const errorsHeader = siteContent ? siteContent.querySelector('.errors-header') : null;
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

            lastError = `unexpected status_code ${response.status}`;
            await sleep(delay * 1000);

        } catch (e) {
            lastError = e.message;
            await sleep(delay * 1000);
        }
    }

    return { error: lastError, status: null, username: username, content: null, title: null, available: null, exists: null };
}

// --- Beispiel für die Verwendung im Browser ---
// Wichtig: Argumente werden hier als ein Konfigurationsobjekt übergeben {}

// (async () => { console.log("Prüfe 'anonymous'..."); const res1 = await checkIfUsernameExistsInBehanceViaFetchAndDOMParser({ username: 'anonymous' }); console.log(res1); console.log("\nPrüfe 'alitakos90'..."); const res2 = await checkIfUsernameExistsInBehanceViaFetchAndDOMParser({ username: 'alitakos90' }); console.log(res2); })();