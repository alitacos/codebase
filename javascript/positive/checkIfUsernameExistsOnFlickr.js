async function checkIfUsernameExistsOnFlickr(options = {}) {
    const {
        username = '',
        retries = 3,
        url = "https://www.flickr.com/people/",
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9, image/avif,image/webp,*/*;q=0.8"
        },
        redirect = 'manual' // Entspricht allow_redirects=False
    } = options;

    if (!username || typeof username !== 'string' || !username.trim()) {
        return { error: 'invalid <username> value', status: null, username, content: null, title: null, available: false, exists: false };
    }

    const cleanUrl = url.trim().replace(/\/+$/, '');
    const cleanUsername = username.trim().replace(/^\/+|\/+$/g, '');
    const targetUrl = `${cleanUrl}/${cleanUsername}`;
    let lastError = null;

    // Hilfsfunktion zum Extrahieren und Bereinigen von HTML-Blöcken via RegEx
    const extractCleanText = (htmlContent, mode) => {
        let blockHtml = '';

        if (mode === '200') {
            // Entspricht: soup.find('div', {'id': 'content'}).find('div', {'class': 'info-container'})
            const contentMatch = htmlContent.match(/<div[^>]*id="content"[^>]*>([\s\S]*?)<\/div>/i);
            if (!contentMatch) return null;

            const infoMatch = contentMatch[1].match(/<div[^>]*class="[^"]*info-container[^"]*"[^>]*>([\s\S]*?)<\/div>/i);
            if (!infoMatch) return null;
            blockHtml = infoMatch[1];
        } else if (mode === '404') {
            // Entspricht: soup.find('section', {'class': 'is-http-404'})
            const errorMatch = htmlContent.match(/<section[^>]*class="[^"]*is-http-404[^"]*"[^>]*>([\s\S]*?)<\/section>/i);
            if (!errorMatch) return null;
            blockHtml = errorMatch[1];
        }

        // 1. Entferne Scripte, Styles, Noscripts und SVGs samt Inhalt
        blockHtml = blockHtml.replace(/<(script|style|noscript|svg)[^>]*>[\s\S]*?<\/\1>/gi, '');
        // 2. Entferne alle HTML-Tags
        blockHtml = blockHtml.replace(/<[^>]+>/g, ' ');
        // 3. HTML-Entities dekodieren
        blockHtml = blockHtml.replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>');
        // 4. Whitespaces zu einem flachen Fließtext bereinigen (verhindert tokenisierte '+'-Anzeigen in der Konsole)
        return blockHtml.replace(/[\t\r\n]+/g, ' ').split(' ').map(w => w.trim()).filter(w => w.length > 0).join(' ') || null;
    };

    for (let i = 0; i < retries; i++) {
        try {
            const response = await fetch(targetUrl, { method: 'GET', headers, redirect });
            const html = await response.text();

            // Titel extrahieren (soup.title.get_text())
            const titleMatch = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
            const titleText = titleMatch ? titleMatch[1].trim() : null;

            if (response.status === 200) {
                const textContent = extractCleanText(html, '200');
                return { error: false, status: 200, username, content: textContent, title: titleText, available: false, exists: true };
            }

            if (response.status === 404) {
                const errorContent = extractCleanText(html, '404');
                return { error: false, status: 404, username, content: errorContent, title: titleText, available: true, exists: false };
            }

            lastError = `unexpected status_code ${response.status}`;
        } catch (error) {
            lastError = error.message;
        }
    }
    return { error: lastError, status: null, username, content: null, title: null, available: null, exists: null };
}

// Beispiel-Aufrufe
// (async () => { const result1 = await checkIfUsernameExistsOnFlickr({ username: 'alexpapatolios90' }); console.log(result1); const result2 = await checkIfUsernameExistsOnFlickr({ username: 'anonymous' }); console.log(result2); })();