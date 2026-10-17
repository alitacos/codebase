async function checkIfUsernameExistsInYcombinator(options = {}) {
    const {
        username = '',
        retries = 3,
        url = 'https://news.ycombinator.com/user',
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
        },
        redirect = 'manual' // Entspricht allow_redirects=False
    } = options;

    if (!username || typeof username !== 'string' || !username.trim()) {
        return { error: 'invalid <username> value', status: null, username, content: null, title: null, available: false, exists: false };
    }

    // Parameter an die URL anhängen (?id=username)
    const targetUrl = `${url.trim()}?id=${encodeURIComponent(username.trim())}`;
    let lastError = null;

    // Hilfsfunktion zur Textextraktion ohne HTML-Tags und mit flacher Textstruktur
    const extractCleanText = (htmlContent) => {
        let cleanHtml = htmlContent;
        // Entferne Scripte, Styles, Noscripts und SVGs samt Inhalt
        cleanHtml = cleanHtml.replace(/<(script|style|noscript|svg)[^>]*>[\s\S]*?<\/\1>/gi, '');
        // Entferne alle HTML-Tags
        cleanHtml = cleanHtml.replace(/<[^>]+>/g, ' ');
        // HTML-Entities dekodieren
        cleanHtml = cleanHtml.replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>');
        // Whitespaces zu einem flachen Fließtext bereinigen
        return cleanHtml.replace(/[\t\r\n]+/g, ' ').split(' ').map(w => w.trim()).filter(w => w.length > 0).join(' ');
    };

    for (let i = 0; i < retries; i++) {
        try {
            const response = await fetch(targetUrl, { method: 'GET', headers, redirect });
            const html = await response.text();

            // Titel extrahieren
            const titleMatch = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
            const titleText = titleMatch ? titleMatch[1].trim() : null;

            if (response.status === 200) {
                const contentText = extractCleanText(html);

                // Exakter Abgleich mit der YCombinator "Nicht gefunden"-Meldung
                if (contentText === "No such user.") {
                    return { error: false, status: 200, username, content: contentText, title: titleText, available: true, exists: false };
                }

                return { error: false, status: 200, username, content: contentText, title: titleText, available: false, exists: true };
            }

            lastError = `unexpected status_code ${response.status}`;
        } catch (error) {
            lastError = error.message;
        }
    }
    return { error: lastError, status: null, username, content: null, title: null, available: null, exists: null };
}

// Beispiel-Aufrufe
// (async () => { const result1 = await checkIfUsernameExistsInYcombinator({ username: 'alexpapatolios90' }); console.log(result1); const result2 = await checkIfUsernameExistsInYcombinator({ username: 'anonymous' }); console.log(result2); })();