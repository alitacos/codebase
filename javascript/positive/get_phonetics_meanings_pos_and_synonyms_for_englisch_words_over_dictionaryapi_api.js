/**
 * Fetch phonetics, meanings, parts of speech, and synonyms for an English word using the free DictionaryAPI service.
 * 
 * @param {string} word - English word to look up in the dictionary API.
 * @param {object} kwargs - Optional arguments passed directly to fetch (e.g. headers, method).
 * @returns {Promise<any>} JSON response from DictionaryAPI containing word definitions, phonetics, meanings, and synonyms.
 */
async function get_phonetics_meanings_pos_and_synonyms_for_englisch_words_over_dictionaryapi_api(word = '', kwargs = {}) {
    if (!word || typeof word !== 'string' || !word.trim()) {
        return { error: 'invalid <word> value' };
    }

    const url = `https://api.dictionaryapi.dev/api/v2/entries/en/${encodeURIComponent(word.trim())}`;
    
    // Standard-Header vorbereiten, damit die API die Verbindung nicht blockiert
    const defaultHeaders = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "Accept": "application/json"
    };

    try {
        const response = await fetch(url, {
            method: 'GET',
            ...kwargs,
            headers: {
                ...defaultHeaders,
                ...(kwargs.headers || {}) // Erlaubt das Überschreiben über kwargs
            }
        });

        // WICHTIG: Wenn die API 404 liefert (Wort nicht gefunden), fangen wir das hier ab
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            return {
                error: `API error! status: ${response.status}`,
                status: response.status,
                details: errorData
            };
        }

        return await response.json();
    } catch (e) {
        return { error: e.message };
    }
}

// Beispiel-Aufruf
// (async () => { const result = await get_phonetics_meanings_pos_and_synonyms_for_englisch_words_over_dictionaryapi_api('hello'); console.dir(result, { depth: null, colors: true }); })();