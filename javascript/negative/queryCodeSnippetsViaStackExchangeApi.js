/**
 * Query code snippets via StackExchange API.
 * 
 * @param {object} options 
 * @param {string} options.query - The search query string.
 * @param {string} options.tag - Tag to filter the search (default: 'python').
 * @param {number} options.maxResults - Max number of results to fetch (default: 5).
 * @param {string} options.apiKey - Optional StackExchange API Key to prevent rate-limiting.
 * @returns {Promise<object>}
 */
async function queryCodeSnippetsViaStackExchangeApi(options = {}) {
    const {
        query = '',
        tag = 'python',
        maxResults = 5,
        apiKey = '' // Hier kannst du deinen API-Key übergeben
    } = options;

    if (!query || typeof query !== 'string' || !query.trim()) {
        return {
            query: query || "",
            tag: tag || "",
            items: 0,
            records: [],
            error: "ValueError - missing query argument"
        };
    }

    // API-Query-Parameter aufbauen
    const params = new URLSearchParams({
        order: "desc",
        sort: "relevance",
        q: query.trim(),
        site: "stackoverflow",
        filter: "!9_bDE(fI5", // Filter beinhaltet das 'body'-Feld
        pagesize: maxResults.toString()
    });

    if (tag && tag.trim()) {
        params.append("tagged", tag.trim());
    }

    // SO WIRD DER API-KEY BENUTZT:
    // Wenn ein Key existiert, wird er einfach als Parameter 'key' angehängt.
    if (apiKey && apiKey.trim()) {
        params.append("key", apiKey.trim());
    }
 
    const apiUrl = `https://api.stackexchange.com/2.3/search/advanced{params.toString()}`;

    try {
        const response = await fetch(apiUrl);
        
        // StackExchange komprimiert Antworten oft mit GZIP. 
        // Die native Node.js fetch-API entpackt dies automatisch im Hintergrund.
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        const results = [];

        const items = data.items || [];
        for (const item of items) {
            const questionTitle = item.title || "";
            const questionLink = item.link || "";
            const questionBody = item.body || "";

            // Ersatz für BeautifulSoup: Alle <code>...</code> Blöcke via RegEx matchen
            const codeBlocks = [];
            const codeRegex = /<code[^>]*>([\s\S]*?)<\/code>/gi;
            let match;

            while ((match = codeRegex.exec(questionBody)) !== null) {
                let codeContent = match[1];
                
                // 1. Alle verbleibenden inneren HTML-Tags entfernen
                codeContent = codeContent.replace(/<[^>]+>/g, ' ');
                // 2. HTML Entities wie &lt;, &gt;, &amp; dekodieren
                codeContent = codeContent.replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>');
                // 3. Zeilenumbrüche flachlegen, damit die Konsole den String nicht zerhackt
                const cleanCode = codeContent.replace(/[\t\r\n]+/g, ' ').split(' ').map(w => w.trim()).filter(w => w.length > 0).join(' ');
                
                if (cleanCode) {
                    codeBlocks.push(cleanCode);
                }
            }

            results.push({
                title: questionTitle,
                link: questionLink,
                code_snippets: codeBlocks.length > 0 ? codeBlocks : ["No code snippet found"]
            });
        }

        return {
            query: query,
            tag: tag,
            items: results.length,
            records: results,
            error: null
        };

    } catch (e) {
        return {
            query: query,
            tag: tag,
            items: 0,
            records: [],
            error: e.message
        };
    }
}

// Beispiel-Aufruf
// (async () => { const result = await queryCodeSnippetsViaStackExchangeApi({ query: 'import pymupdf', tag: 'python' }); console.log(result); })();