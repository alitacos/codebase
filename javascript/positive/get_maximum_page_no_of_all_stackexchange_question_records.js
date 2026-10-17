/**
 * Retrieves the maximum page number from a StackExchange question listing page.
 * 
 * @param {string} netloc - The StackExchange domain (e.g., 'math.stackexchange.com').
 * @param {string} tab - The sorting/filter tab to use in the query (default: 'votes').
 * @param {number} pagesize - Number of items per page (default: 50).
 * @returns {Promise<number>} The maximum page number found, or 0.
 */
async function get_maximum_page_no_of_all_stackexchange_question_records(netloc = '', tab = 'votes', pagesize = 50) {
    let cleanNetloc = netloc.trim();
    
    // Protokolle abschneiden, genau wie im Python-Skript
    if (cleanNetloc.startsWith('https://')) {
        cleanNetloc = cleanNetloc.substring(8);
    } else if (cleanNetloc.startsWith('http://')) {
        cleanNetloc = cleanNetloc.substring(7);
    }
    
    // URL für die Anfrage zusammenbauen
    const url = `https://${cleanNetloc}/questions?tab=${tab}&pagesize=${pagesize}`;

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const html = await response.text();

        const pages_nums = [];

        // Exakte Nachbildung des BeautifulSoup-Verhaltens via RegEx:
        // Sucht nach <a> Tags, die sowohl ein 'href' als auch ein 'title' Attribut besitzen
        const aTagRegex = /<a\s+[^>]*href="([^"]+)"[^>]*title="[^"]*"[^>]*>([\s\S]*?)<\/a>/gi;
        let match;

        while ((match = aTagRegex.exec(html)) !== null) {
            const href = match[1];
            let text = match[2];

            // Filter-Kriterium aus deinem Python-Skript:
            // Es wird strikt geprüft, ob '/questions?tab=votes' UND '&page=' in der URL enthalten sind
            if (href.includes('/questions?tab=votes') && href.includes('&page=')) {
                
                // HTML-Tags im inneren Text entfernen und Whitespaces trimmen
                text = text.replace(/<[^>]+>/g, '').trim();

                // Prüfen, ob der verbleibende Text eine reine Zahl ist
                if (/^\d+$/.test(text)) {
                    pages_nums.push(parseInt(text, 10));
                }
            }
        }

        // Maximalen Wert ermitteln oder 0 zurückgeben
        return pages_nums.length > 0 ? Math.max(...pages_nums) : 0;

    } catch (e) {
        // Fehler abfangen (gibt 0 zurück, analog zum leeren Array-Verhalten in Python)
        return 0;
    }
}

// example usage:
// (async () => { const result = await get_maximum_page_no_of_all_stackexchange_question_records('https://math.stackexchange.com/'); console.log(result); })();
// [out]: 34021