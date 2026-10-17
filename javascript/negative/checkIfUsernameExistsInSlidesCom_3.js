async function checkIfUsernameExistsInSlidesCom(options = {}) {
    const {
        username = '',
        retries = 3,
        url = 'https://slides.com',
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9, image/avif,image/webp,*/*;q=0.8"
        },
        redirect = 'manual'
    } = options;

    if (!username || typeof username !== 'string' || !username.trim()) {
        return { error: 'invalid <username> value', status: null, username, content: null, title: null, available: false, exists: false };
    }

    const cleanUrl = url.trim().replace(/\/+$/, '');
    const cleanUsername = username.trim().replace(/^\/+|\/+$/g, '');
    const targetUrl = `${cleanUrl}/${cleanUsername}`;
    let lastError = null;

    // Hilfsfunktion zum radikalen Säubern von HTML-Inhalten via RegEx
    const extractCleanText = (htmlContent, contentSelector = 'body') => {
        let targetHtml = htmlContent;

        if (contentSelector === 'body') {
            const bodyMatch = htmlContent.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
            targetHtml = bodyMatch ? bodyMatch[1] : htmlContent;
        } else if (contentSelector === 'errors-header') {
            const errorMatch = htmlContent.match(/<[^>]*class="[^"]*errors-header[^"]*"[^>]*>([\s\S]*?)<\/[^>]+>/i);
            targetHtml = errorMatch ? errorMatch[1] : '';
        }

        // 1. Entferne Scripte, Styles, Noschripts und SVGs samt Inhalt
        targetHtml = targetHtml.replace(/<(script|style|noscript|svg)[^>]*>[\s\S]*?<\/\1>/gi, '');
        // 2. Entferne alle verbleibenden HTML-Tags
        targetHtml = targetHtml.replace(/<[^>]+>/g, ' ');
        // 3. Ersetze HTML-Entities wie &nbsp; oder &amp; durch Leerzeichen/Zeichen
        targetHtml = targetHtml.replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>');
        // 4. Bereinige Whitespaces und Zeilenumbrüche in eine flache Zeile
        return targetHtml.replace(/[\t\r\n]+/g, ' ').split(' ').map(w => w.trim()).filter(w => w.length > 0).join(' ');
    };

    for (let i = 0; i < retries; i++) {
        try {
            const response = await fetch(targetUrl, { method: 'GET', headers, redirect });
            const html = await response.text();

            // Titel extrahieren
            const titleMatch = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
            const titleText = titleMatch ? titleMatch[1].trim() : null;

            if (response.status === 200) {
                let bodyText = extractCleanText(html, 'body');

                let finalContent = bodyText;
                if (titleText && !bodyText.startsWith(titleText)) {
                    finalContent = `${titleText} ${bodyText}`;
                }

                return { error: false, status: 200, username, content: finalContent || null, title: titleText, available: false, exists: true };
            }

            if (response.status === 404) {
                const errorContent = extractCleanText(html, 'errors-header');
                return { error: false, status: 404, username, content: errorContent || null, title: titleText, available: true, exists: false };
            }

            lastError = `unexpected status_code ${response.status}`;
            // Kein sleep() mehr – Schleife springt sofort in den nächsten Versuch
        } catch (error) {
            lastError = error.message;
        }
    }
    return { error: lastError, status: null, username, content: null, title: null, available: null, exists: null };
}