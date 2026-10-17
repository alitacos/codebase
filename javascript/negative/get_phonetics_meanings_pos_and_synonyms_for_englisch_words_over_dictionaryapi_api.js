/**
 * Fetch phonetics, meanings, parts of speech, and synonyms for an English word using the free DictionaryAPI service.
 * 
 * @param {string} word - English word to look up in the dictionary API.
 * @param {object} kwargs - Optional arguments passed directly to fetch (e.g. headers, signal, method).
 * @returns {Promise<any>} JSON response from DictionaryAPI containing word definitions, phonetics, meanings, and synonyms.
 */
async function get_phonetics_meanings_pos_and_synonyms_for_englisch_words_over_dictionaryapi_api(word = '', kwargs = {}) {
    // API-Endpunkt für die Wortsuche zusammenbauen
    const url = `https://dictionaryapi.dev{encodeURIComponent(word.trim())}`;
    
    try {
        // HTTP GET Request ausführen und die kwargs direkt als Fetch-Optionen übergeben
        const response = await fetch(url, {
            method: 'GET',
            ...kwargs
        });

        // Parsen und Zurückgeben der JSON-Antwort
        return await response.json();
    } catch (e) {
        // Fehlerbehandlung analog zu JS-Standards
        return { error: e.message };
    }
}

// Beispiel-Aufruf
(async () => {
    // Einfacher Aufruf
    const result = await get_phonetics_meanings_pos_and_synonyms_for_englisch_words_over_dictionaryapi_api('hello');
    
    // Node.js-Konsole zwingen, das komplette verschachtelte JSON-Objekt flach und vollständig anzuzeigen
    console.dir(result, { depth: null, colors: true });

    // Beispiel mit kwargs (z.B. mit einem Custom-Header oder Timeout-Signal):
    // const controller = new AbortController();
    // setTimeout(() => controller.abort(), 5000);
    // const resultWithKwargs = await get_phonetics_meanings_pos_and_synonyms_for_englisch_words_over_dictionaryapi_api('world', { 
    //     headers: { "Accept": "application/json" },
    //     signal: controller.signal 
    // });
})();
//negative