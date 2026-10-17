/**
 * Extrahiert das Inhaltsverzeichnis (ToC) einer Google DevSite als hierarchische Baumstruktur.
 * Nutzt den '?partial=1' JSON-Endpunkt, um auch dynamisch nachgeladene Seiteninhalte stabil zu erfassen.
 * 
 * @param {string} url - Die originale URL des Google-Artikels.
 * @returns {Promise<Array<object>>} Die hierarchische Struktur des Inhaltsverzeichnisses.
 */
async function get_hierarchical_devsite_toc_via_partial_json(url = '') {
    if (!url || typeof url !== 'string' || !url.trim()) {
        return [];
    }

    const headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "Accept": "application/json"
    };

    try {
        // 1. '?partial=1' Parameter erzwingen, um das rohe JSON mit dem Artikel-HTML abzufragen
        const parsedUrl = new URL(url.trim());
        parsedUrl.searchParams.set('partial', '1');
        
        const response = await fetch(parsedUrl.href, { method: 'GET', headers });
        if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);
        
        const jsonData = await response.json();
        
        // Google speichert das gerenderte HTML im 'content' oder 'body' Feld des JSON-Objekts
        const bodyHtml = jsonData.content || jsonData.body || '';
        if (!bodyHtml) return [];

        const tocTree = [];
        let lastH2 = null;

        // 2. Googles exakte Filter-Logik aus 'tDa' anwenden:
        // Matcht H2- und H3-Tags, die eine ID und ein data-text/text Attribut besitzen.
        // Schließt Tags mit der Klasse 'hide-from-toc' sowie die IDs 'contents' / 'table-of-contents' aus.
        const headingRegex = /<(h2|h3)(?![^>]*class="[^"]*hide-from-toc[^"]*")(?![^>]*id="(contents|table-of-contents)")[^>]*?id="([^"]+)"[^>]*?(data-text|text)="([^"]+)"[^>]*>/gi;
        let match;

        while ((match = headingRegex.exec(bodyHtml)) !== null) {
            const level = match[1].toLowerCase();
            const id = match[3];
            let text = match[5];

            // HTML-Entities (z.B. &amp; oder &lt;) auflösen
            text = text.replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>');
            text = text.replace(/[\t\r\n]+/g, ' ').trim();

            const node = {
                id: id,
                level: level,
                text: text,
                children: []
            };

            // 3. Baumstruktur aufbauen: H3-Elemente wandern als Kinder in das vorherige H2
            if (level === 'h2') {
                tocTree.push(node);
                lastH2 = node; 
            } else if (level === 'h3' && lastH2) {
                lastH2.children.push(node);
            } else {
                tocTree.push(node);
            }
        }

        return tocTree;

    } catch (e) {
        console.error(`Fehler beim dynamischen ToC-Parsing: ${e.message}`);
        return [];
    }
}

// === Testlauf ===
//(async () => { const targetUrl = 'https://developer.chrome.com/docs/ai/built-in-apis'; const toc = await get_hierarchical_devsite_toc_via_partial_json(targetUrl); console.dir(toc, { depth: null, colors: true }); })();
//negative