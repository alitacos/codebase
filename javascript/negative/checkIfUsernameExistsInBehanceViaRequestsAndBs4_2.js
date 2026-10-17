/**
 * Überprüft, ob ein Benutzername auf Behance existiert (Node.js, OHNE externe Module).
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
    
    // WICHTIG: Behance erzwingt ein Slash '/' am Ende des Usernamens, sonst gibt es einen 301 Redirect.
    const cleanUrl = url.trim().replace(/\/+$/, '');
    const cleanUsername = username.trim().replace(/\/+$/, '');
    const targetUrl = `${cleanUrl}/${cleanUsername}/`; 

    let last_error = null;
    const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

    // Nachbildung der Text-Extraktion von BeautifulSoup ohne externe Module
    const extractTextFromHtml = (html, startTagRegex) => {
        if (!html) return null;
        const match = html.match(startTagRegex);
        if (!match) return null;
        
        // Schneidet das HTML ab dem gefundenen Container ab
        let subHtml = html.substring(match.index);
        
        // Entfernt alle Skripte, Styles und HTML-Tags
        subHtml = subHtml.replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '');
        subHtml = subHtml.replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '');
        
        // Extrahiert reinen Text (Filtert leere Zeilen wie Pythons split/strip)
        const lines = subHtml
            .replace(/<[^>]*>/g, '\n')
            .replace(/\t/g, '\n')
            .split('\n')
            .map(line => line.trim())
            .filter(line => line.length > 0);

        // Begrenzung für den Profil-Inhalt (stoppt beim Footer, um Müll zu vermeiden)
        const stopIndex = lines.findIndex(l => l.includes("Adobe") || l.includes("Company"));
        const cleanLines = stopIndex !== -1 ? lines.slice(0, stopIndex) : lines;

        return cleanLines.join(' ');
    };

    for (let i = 0; i < retries; i++) {
        try {
            const response = await fetch(targetUrl, {
                method: 'GET',
                headers: requestHeaders,
                redirect: redirectMode
            });

            // Wenn der Server trotz des Slashes mit 301/302 antwortet und allow_redirects false ist
            if ((response.status === 301 || response.status === 302) && !allow_redirects) {
                last_error = `unexpected status_code ${response.status}`;
                await sleep(delay * 1000);
                continue;
            }

            const htmlText = await response.text();

            // Titel extrahieren
            const titleMatch = htmlText.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
            const title = titleMatch && titleMatch[1] ? titleMatch[1].trim() : null;

            if (response.status === 200) {
                const content = extractTextFromHtml(htmlText, /<div[^>]*id=["']site-content["']/i);
                
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
                const content = extractTextFromHtml(htmlText, /<div[^>]*class=["'][^"']*errors-header[^"']*["']/i);

                return {
                    error: false,
                    status: 404,
                    username: username,
                    content: content || "Oops! We can’t find that page.",
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

// --- Richtiger Aufruf in Node.js ---
// (async () => { console.log(await checkIfUsernameExistsInBehanceViaRequestsAndBs4('anonymous')); console.log(await checkIfUsernameExistsInBehanceViaRequestsAndBs4('alitakos90')); })();