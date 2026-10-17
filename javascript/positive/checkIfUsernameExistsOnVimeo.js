async function checkIfUsernameExistsOnVimeo(options = {}) {
    const {
        username = '',
        retries = 3,
        url = 'https://vimeo.com/',
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
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

    // Hilfsfunktion zum Extrahieren und Bereinigen des gesamten HTML-Textes via RegEx
    const extractCleanText = (htmlContent) => {
        let cleanHtml = htmlContent;
        
        // 1. Entferne Scripte, Styles, Noscripts und SVGs samt Inhalt
        cleanHtml = cleanHtml.replace(/<(script|style|noscript|svg)[^>]*>[\s\S]*?<\/\1>/gi, '');
        // 2. Entferne alle HTML-Tags
        cleanHtml = cleanHtml.replace(/<[^>]+>/g, ' ');
        // 3. HTML-Entities dekodieren
        cleanHtml = cleanHtml.replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>');
        // 4. Whitespaces und Zeilenumbrüche in ein einziges Leerzeichen umwandeln
        let textResult = cleanHtml.replace(/[\t\r\n]+/g, ' ').split(' ').map(w => w.trim()).filter(w => w.length > 0).join(' ');
        
        // Entspricht dem .replace('Vimeo\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '') aus dem Python-Code.
        // Da wir Zeilenumbrüche oben entfernt haben, filtern wir hier das übrig gebliebene "Vimeo " am Anfang heraus, falls vorhanden.
        if (textResult.startsWith('Vimeo ')) {
            textResult = textResult.replace(/^Vimeo\s+/, '');
        }
        
        return textResult || null;
    };

    for (let i = 0; i < retries; i++) {
        try {
            const response = await fetch(targetUrl, { method: 'GET', headers, redirect });
            const html = await response.text();

            // Titel extrahieren (soup.title.get_text())
            const titleMatch = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
            const titleText = titleMatch ? titleMatch[1].trim() : null;

            if (response.status === 200) {
                const textContent = extractCleanText(html);
                return { error: false, status: 200, username, content: textContent, title: titleText, available: false, exists: true };
            }

            if (response.status === 404) {
                const textContent = extractCleanText(html);
                return { error: false, status: 404, username, content: textContent, title: titleText, available: true, exists: false };
            }

            lastError = `unexpected status_code ${response.status}`;
        } catch (error) {
            lastError = error.message;
        }
    }
    return { error: lastError, status: null, username, content: null, title: null, available: null, exists: null };
}

// Beispiel-Aufrufe
// (async () => { const result1 = await checkIfUsernameExistsOnVimeo({ username: 'anna' }); console.log(result1); const result2 = await checkIfUsernameExistsOnVimeo({ username: 'alexpapatolios90' }); console.log(result2); })();