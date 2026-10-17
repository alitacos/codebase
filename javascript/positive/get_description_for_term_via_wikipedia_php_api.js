/**
 * Wikipedia PHP API Search + Page Property Extractor
 * 
 * Uses the Wikipedia Action API (w/api.php) to first search for the most relevant article title for a given term, 
 * and then fetches page-level metadata (such as extracts, categories, info, or description) from that article.
 * 
 * @param {string} term - Search term used to find a matching Wikipedia article.
 * @param {string} lang - Wikipedia language code used for the API endpoint (e.g. 'en', 'de').
 * @param {string} prop - Page property type to retrieve ('extracts', 'categories', 'info', 'description').
 * @returns {Promise<object|string>} Raw page data object for the resolved article, an error string, or an empty string on failure.
 */
async function get_description_for_term_via_wikipedia_php_api(term = '', lang = 'de', prop = 'extracts') {
    if (!term || typeof term !== 'string' || !term.trim()) {
        return "";
    }

    // Validierung des Eigenschaftstyps (Fallback auf 'extracts')
    let validProp = prop;
    if (!['extracts', 'categories', 'info', 'description'].includes(validProp)) {
        validProp = 'extracts';
    }

    const url = `https://${lang}.wikipedia.org/w/api.php`;

    const headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    };

    try {
        // --- STEP 1: Suchanfrage für den am besten passenden Artikeltitel ---
        const searchParams = new URLSearchParams({
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": term.trim(),
            "srlimit": "1"
        });

        // 5-Sekunden Timeout für Schritt 1 einrichten
        const controller1 = new AbortController();
        const timeout1 = setTimeout(() => controller1.abort(), 5000);

        const searchResponse = await fetch(`${url}?${searchParams.toString()}`, {
            method: 'GET',
            headers: headers,
            signal: controller1.signal
        });
        clearTimeout(timeout1);

        if (!searchResponse.ok) throw new Error(`Search HTTP error: ${searchResponse.status}`);
        
        const searchData = await searchResponse.json();
        const searchResults = searchData?.query?.search || [];

        if (searchResults.length === 0) {
            return `Fehler: '${term}' nicht gefunden.`;
        }

        const exactTitle = searchResults[0].title;

        // --- STEP 2: Seiten-Eigenschaften für den gefundenen Titel abrufen ---
        const pageParams = new URLSearchParams({
            "action": "query",
            "format": "json",
            "titles": exactTitle,
            "prop": validProp,
            "exintro": "true",
            "explaintext": "false"
        });

        // 5-Sekunden Timeout für Schritt 2 einrichten
        const controller2 = new AbortController();
        const timeout2 = setTimeout(() => controller2.abort(), 5000);

        const pageResponse = await fetch(`${url}?${pageParams.toString()}`, {
            method: 'GET',
            headers: headers,
            signal: controller2.signal
        });
        clearTimeout(timeout2);

        if (!pageResponse.ok) throw new Error(`Page data HTTP error: ${pageResponse.status}`);

        const pageData = await pageResponse.json();
        const pages = pageData?.query?.pages || {};

        // Iteriere über die zurückgegebenen Page-IDs und gib das erste Ergebnis-Objekt zurück
        for (const pageId in pages) {
            if (Object.prototype.hasOwnProperty.call(pages, pageId)) {
                return pages[pageId];
            }
        }

    } catch (e) {
        // Sicherer Fallback bei jeglichen Request- oder Parsing-Fehlern (analog zu Python)
        return '';
    }

    return "";
}

// Beispiel-Aufruf (Entspricht deinem Python-Test)
// (async () => { const result = await get_description_for_term_via_wikipedia_php_api('url', 'en'); console.dir(result, { depth: null, colors: true }); })();
