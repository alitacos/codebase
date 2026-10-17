async function checkIfUsernameExistsInSnapchat(options = {}) {
    const {
        username = '',
        retries = 3,
        url = 'https://www.behance.net/',
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

    // Hilfsfunktion zum Extrahieren und Bereinigen von Text aus bestimmten HTML-Blöcken
    const extractCleanText = (htmlContent, contentSelector = 'site-content') => {
        let blockHtml = '';

        if (contentSelector === 'site-content') {
            // Entspricht soup.find('div', {'id': 'site-content'})
            const siteContentMatch = htmlContent.match(/<div[^>]*id="site-content"[^>]*>([\s\S]*?)<\/div>/i);
            if (!siteContentMatch) return null;
            blockHtml = siteContentMatch[1];
        } else if (contentSelector === 'errors-header') {
            // Sucht zuerst das site-content-div
            const siteContentMatch = htmlContent.match(/<div[^>]*id="site-content"[^>]*>([\s\S]*?)<\/div>/i);
            if (!siteContentMatch) return null;
            
            // Sucht das .errors-header darin (entspricht content.find('div', {'class': 'errors-header'}))
            const errorMatch = siteContentMatch[1].match(/<div[^>]*class="[^"]*errors-header[^"]*"[^>]*>([\s\S]*?)<\/div>/i);
            if (!errorMatch) return null;
            blockHtml = errorMatch[1];
        }

        // Entferne Scripte, Styles, Noscripts und SVGs samt Inhalt aus dem Block
        blockHtml = blockHtml.replace(/<(script|style|noscript|svg)[^>]*>[\s\S]*?<\/\1>/gi, '');
        // Entferne alle HTML-Tags
        blockHtml = blockHtml.replace(/<[^>]+>/g, ' ');
        // HTML-Entities dekodieren
        blockHtml = blockHtml.replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>');
        // Whitespaces zu einem flachen Fließtext bereinigen (keine störenden Token-Zeilenumbrüche)
        const textResult = blockHtml.replace(/[\t\r\n]+/g, ' ').split(' ').map(w => w.trim()).filter(w => w.length > 0).join(' ');
        
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
                const bodyContent = extractCleanText(html, 'site-content');
                return { error: false, status: 200, username, content: bodyContent, title: titleText, available: false, exists: true };
            }

            if (response.status === 404) {
                const errorContent = extractCleanText(html, 'errors-header');
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
// (async () => { const result1 = await checkIfUsernameExistsInSnapchat({ username: 'anonymous' }); console.log(result1); const result2 = await checkIfUsernameExistsInSnapchat({ username: 'alexpapatolios90' }); console.log(result2); })();
