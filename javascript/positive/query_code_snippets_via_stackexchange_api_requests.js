/**
 * Query code snippets via StackExchange API.
 * 
 * @param {string} query - The search query string.
 * @param {string} tag - Tag to filter the search (default: 'python').
 * @param {number} max_results - Max number of results to fetch (default: 5).
 * @param {string} apiKey - Optional StackExchange API Key.
 * @returns {Promise<object>}
 */
async function query_code_snippets_via_stackexchange_api_requests(query = '', tag = 'python', max_results = 5, apiKey = '') {
    if (!query) {
        return {
            "query": query ? query : "",
            "tag": tag ? tag : "",
            "items": 0,
            "records": [],
            "error": "ValueError - missing query argument"
        };
    }

    // Die identische Basis-URL aus dem Python-Skript
    const url = "https://api.stackexchange.com/2.3/search/advanced";

    // Aufbau der exakt gleichen Parameter-Struktur
    const params = new URLSearchParams({
        "order": "desc",
        "sort": "relevance",
        "q": query ? query : "",
        "tagged": tag ? tag : "",
        "site": "stackoverflow",
        "filter": "!9_bDE(fI5",  // Beinhaltet den Body-Content laut deiner Definition
        "pagesize": max_results.toString()
    });

    // WIE MAN DEN API-KEY NUTZT:
    // Der Key wird laut StackExchange-Dokumentation einfach als Query-Parameter 'key' angehängt.
    if (apiKey && apiKey.trim()) {
        params.append("key", apiKey.trim());
    }

    const targetUrl = `${url}?${params.toString()}`;

    try {
        const response = await fetch(targetUrl);
        const data = await response.json();
        
        // Exakte Umsetzung deines Python-Ablaufs: 
        // Gibt die rohen JSON-Daten der API direkt hier zurück.
        return data;

        // Der nachfolgende Code ist aufgrund des obigen 'return' unerreichbar (wie in der Vorlage):
        const results = [];
        const items = data.items || [];
        for (const item of items) {
            const question_title = item.title;
            const question_link = item.link;
            const question_body = item.body || "";

            // Simuliert BeautifulSoup für <code> Blöcke und bereinigt Whitespaces flach
            const code_blocks = [];
            const codeRegex = /<code[^>]*>([\s\S]*?)<\/code>/gi;
            let match;
            while ((match = codeRegex.exec(question_body)) !== null) {
                let codeText = match[1].replace(/<[^>]+>/g, ' ');
                codeText = codeText.replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>');
                const cleanCode = codeText.replace(/[\t\r\n]+/g, ' ').split(' ').map(w => w.trim()).filter(w => w.length > 0).join(' ');
                if (cleanCode) code_blocks.push(cleanCode);
            }

            results.push({
                "title": question_title,
                "link": question_link,
                "code_snippets": code_blocks.length > 0 ? code_blocks : ["No code snippet found"]
            });
        }
        return { "query": query, "tag": tag, 'items': results.length, "records": results, "error": null };

    } catch (e) {
        return {
            "query": query ? query : "",
            "tag": tag ? tag : "",
            "items": 0,
            "records": [],
            "error": e.message
        };
    }
}

// Example usage:
// (async () => { const result = await query_code_snippets_via_stackexchange_api_requests('import pymupdf', 'python', 5); console.dir(result, { depth: null, colors: true }); })();
