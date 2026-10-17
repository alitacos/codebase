/**
 * Fetch and print dictionary description info from the Datamuse API.
 * 
 * @param {string} word - The word to look up.
 * @returns {Promise<void>}
 */
async function query_datamuse_dictionary_description_info_api_and_print_response_desc(word = '') {
    if (!word || typeof word !== 'string' || !word.trim()) {
        console.log("Wort nicht gefunden.");
        return;
    }

    // Exakte Nachbildung des Python-Strings: Die geschweiften Klammern und der Inhalt 
    // müssen wortwörtlich als Text in den ml-Parameter übergeben werden!
    const mlValue = `{'+'.join([a.strip().lower() for a in word.split() if a and a.strip() ])}`;

    const baseUrl = "https://api.datamuse.com/words";
    const params = new URLSearchParams({
        "ml": mlValue,
        "sp": word.toLowerCase(),
        "md": "d",
        "max": "1"
    });

    const targetUrl = `${baseUrl}?${params.toString()}`;

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000);

    try {
        const response = await fetch(targetUrl, { signal: controller.signal });
        clearTimeout(timeoutId);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (!data || data.length === 0) {
            console.log("Wort nicht gefunden.");
            return;
        }

        console.log(`=== DATAMUSE ERGEBNIS FÜR: ${word.toUpperCase()} ===`);
        
        // Holt das erste gefundene Wort-Objekt (entspricht data[0] in Python)
        const word_info = data[0];

        const defs = word_info.defs || [];
        for (const def_entry of defs) {
            const splitIndex = def_entry.indexOf('\t');
            if (splitIndex === -1) continue;

            const pos = def_entry.substring(0, splitIndex);
            const definition = def_entry.substring(splitIndex + 1);

            const pos_mapping = {
                "n": "NOUN (Substantiv)",
                "v": "VERB (Zeitwort)",
                "adj": "ADJECTIVE",
                "adv": "ADVERB"
            };

            const wordType = pos_mapping[pos] || pos.toUpperCase();

            console.log(`Wortart: ${wordType}`);
            console.log(`Bedeutung: ${definition}\n`);
        }

    } catch (e) {
        if (e.name === 'AbortError') {
            console.log("Fehler: Request timeout after 5 seconds");
        } else {
            console.log(`Fehler: ${e.message}`);
        }
    }
}

// Testlauf
// (async () => { await query_datamuse_dictionary_description_info_api_and_print_response_desc("works"); })();
