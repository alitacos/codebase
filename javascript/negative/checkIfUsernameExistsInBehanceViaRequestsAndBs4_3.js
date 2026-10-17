/**
 * Überprüft, ob ein Benutzername auf Behance existiert (Node.js ohne externe Module).
 */
async function checkIfUsernameExistsInBehanceViaRequestsAndBs4(
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
    if (!username || typeof username !== 'string' || !username.trim()) {
        return { error: 'invalid <username> value', status: null, username: username, content: null, title: null, available: false, exists: false };
    }

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

    // Hilfsfunktion: Entfernt alle HTML-Tags und bereinigt den Text
    const stripHtmlAndClean = (htmlString) => {
        if (!htmlString) return null;
        return htmlString
            .replace(/<[^>]*>/g, ' ') // Alle HTML-Tags durch Leerzeichen ersetzen
            .replace(/\t/g, '\n')     // Tabs durch Umbrüche ersetzen
            .split('\n')
            .map(line => line.trim())
            .filter(line => line.length > 0)
            .join(' ');              // Zusammenfügen zu einem Fließtext wie im Wunsch-Output
    };

    for (let i = 0; i < retries; i++) {
        try {
            const response = await fetch(targetUrl, {
                method: 'GET',
                headers: requestHeaders,
                redirect: redirectMode
            });

            const htmlText = await response.text();

            // 1. Titel extrahieren mittels Regex
            const titleMatch = htmlText.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
            const title = titleMatch ? titleMatch[1].trim() : null;

            // 2. Element-Inhalte extrahieren
            let content = null;

            if (response.status === 200) {
                // Sucht das <div id="site-content">...</div>
                const contentMatch = htmlText.match(/<div[^>]*id=["']site-content["'][^>]*>([\s\S]*?)<\/div>/i);
                if (contentMatch) {
                    content = stripHtmlAndClean(contentMatch[1]);
                }

                return {
                    error: false,
                    status: 200,
                    username: username,
                    content: content,
                    title: title,
                    available: false,
                    exists: true
                };
            }

            if (response.status === 404) {
                // Sucht die Fehlerklasse innerhalb des HTMLs
                const errorMatch = htmlText.match(/<div[^>]*class=["'][^"']*errors-header[^"']*["'][^>]*>([\s\S]*?)<\/div>/i);
                if (errorMatch) {
                    content = stripHtmlAndClean(errorMatch[1]);
                } else {
                    // Fallback auf site-content falls errors-header tiefer verschachtelt ist
                    const contentMatch = htmlText.match(/<div[^>]*id=["']site-content["'][^>]*>([\s\S]*?)<\/div>/i);
                    if (contentMatch) content = stripHtmlAndClean(contentMatch[1]);
                }

                return {
                    error: false,
                    status: 404,
                    username: username,
                    content: content,
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

// --- WICHTIG: Richtiger asynchroner Aufruf in Node.js ---

// async function run() { const res1 = await checkIfUsernameExistsInBehanceViaRequestsAndBs4('anonymous'); console.log(res1); const res2 = await checkIfUsernameExistsInBehanceViaRequestsAndBs4('alitakos90'); console.log(res2); } run();