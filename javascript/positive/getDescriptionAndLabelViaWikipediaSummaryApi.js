async function getDescriptionAndLabelViaWikipediaSummaryApi(
    term = '', 
    lang = 'de', 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }
) {
    const trimmedTerm = term ? term.trim() : '';
    
    // Initialisiere die Standard-Rückgabestruktur
    const result = { 
        term: trimmedTerm, 
        label: "Unbekannt", 
        description: "" 
    };

    // Validierung des Suchbegriffs (behebt den Bug aus dem Python-Template)
    if (!trimmedTerm) {
        return result;
    }

    // URL-Encoding für den Endpunkt (ersetzt Leerzeichen durch Unterstriche und maskiert Sonderzeichen)
    const termEncoded = encodeURIComponent(trimmedTerm.replace(/ /g, '_'));
    const restUrl = `https://${lang}.wikipedia.org/api/rest_v1/page/summary/${termEncoded}`;

    try {
        // AbortController für den 5-Sekunden-Timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000);

        const response = await fetch(restUrl, {
            method: 'GET',
            headers: headers,
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        // HTTP-Fehlerbehandlung
        if (response.status === 403) {
            result.description = "Fehler: Ihre IP-Adresse wird von Wikipedia blockiert (HTTP 403 Forbidden).";
            return result;
        } else if (response.status === 404) {
            result.description = `Fehler: Begriff '${trimmedTerm}' wurde nicht gefunden.`;
            return result;
        }

        // Falls ein anderer HTTP-Fehler auftritt (äquivalent zu raise_for_status)
        if (!response.ok) {
            return result;
        }

        const data = await response.json();

        result.term = data.title || trimmedTerm;
        result.description = data.extract ? data.extract.trim() : "";

        // Optionales Beschreibungsfeld auslesen
        if (data.description) {
            result.label = data.description;
        }

    } catch (error) {
        // Fängt Netzwerkfehler, JSON-Fehler oder Timeouts (AbortError) ab
        return result;
    }

    return result;
}

// --- Testaufrufe (Asynchroner Kontext erforderlich) ---
// (async () => { console.log("Test 1:", await getDescriptionAndLabelViaWikipediaSummaryApi("Albert Einstein", "en")); console.log("\nTest 2:", await getDescriptionAndLabelViaWikipediaSummaryApi("URL", "gr")); })();