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

    // Erstellt den URL-konformen 'ml'-Parameter (Wörter mit '+' verbinden)
    const mlParam = word.split(' ').map(a => a.trim().toLowerCase()).filter(a => a.length > 0).join('+');
    const url = `https://datamuse.com{mlParam}`;

    // Aufbau der Query-Parameter (?sp=word&md=d&max=1)
    const params = new URLSearchParams({
        "sp": word.toLowerCase(),
        "md": "d",
        "max": "1"
    });

    const targetUrl = `${url}&${params.toString()}`;

    // 5-Sekunden-Timeout via AbortController einrichten
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000);

    try {
        const response = await fetch(targetUrl, { signal: controller.signal });
        clearTimeout(timeoutId); // Timeout löschen, da der Request rechtzeitig ankam

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Falls du die vollständige Antwort brauchst, aktiviere diese Zeile:
        // return data;

        if (!data || data.length === 0) {
            console.log("Wort nicht gefunden.");
            return;
        }

        console.log(`=== DATAMUSE ERGEBNIS FÜR: ${word.toUpperCase()} ===`);
        const word_info = data[0];

        const defs = word_info.defs || [];
        for (const def_entry of defs) {
            // Datamuse liefert das Format: "n\tdefinition..."
            // Wir splitten am Tabulator (\t) auf
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

            // Ausgabe bereinigen und flachhalten, um verschachtelte Token-Fehler in Node zu vermeiden
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
