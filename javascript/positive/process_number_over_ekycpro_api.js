/**
 * Verarbeitet eine Telefonnummer über die eKYC Pro API.
 * 
 * @param {string} service - Der gewünschte Dienst (z. B. 'whatsapp', 'telegram').
 * @param {string} phone - Die Telefonnummer im internationalen Format.
 * @param {string} mode - Der Abfragemodus (Standard: 'phone').
 * @param {string|null} token - Der API-Schlüssel für die Authentifizierung.
 * @returns {Promise<object>} Das JSON-Ergebnis der API oder ein leeres Objekt im Fehlerfall.
 */
async function process_number_over_ekycpro_api(service = '', phone = '', mode = 'phone', token = null) {
    if (!token) {
        console.log('missing token. error processing number');
        return {};
    }

    // Normalisierung des Service-Namens (identisch zur Python-Logik)
    let cleanService = service;
    if (['whatsapp', 'ws'].includes(cleanService)) {
        cleanService = 'ws';
    }
    if (['whatsapp-avatar', 'whatsapp-pic', 'ws_avatar'].includes(cleanService)) {
        cleanService = 'ws_avatar';
    }
    if (['ws_business', 'whatsapp_business'].includes(cleanService)) {
        cleanService = 'ws_business';
    }
    if (['tg', 'telegram'].includes(cleanService)) {
        cleanService = 'tg';
    }

    const url = "https://api.ekycpro.com/v1/check";

    const headers = {
        "X-API-Key": token,
        "Content-Type": "application/json"
    };

    const payload = {
        "service_type": cleanService,
        "identifier": phone
    };

    const max_retries = 3;

    for (let attempt = 0; attempt < max_retries; attempt++) {
        // 30-Sekunden Timeout für fetch einrichten (timeout=30)
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 30500);

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: headers,
                body: JSON.stringify(payload),
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            // Entspricht response.raise_for_status()
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // Prüfen, ob die Antwort ein gültiges, nicht-leeres Objekt ist
            if (data && typeof data === 'object' && !Array.isArray(data) && Object.keys(data).length > 0) {
                return data;
            }

            console.log(`Attempt ${attempt + 1}: Empty or invalid response.`);

        } catch (e) {
            clearTimeout(timeoutId);
            if (e.name === 'AbortError') {
                console.log(`Attempt ${attempt + 1} failed: Request timeout after 30 seconds`);
            } else {
                console.log(`Attempt ${attempt + 1} failed: ${e.message}`);
            }
        }
        
        // Kein sleep() – Schleife springt bei Fehlern sofort in den nächsten Versuch
    }

    // Alle Versuche fehlgeschlagen
    return {};
}

// === Beispiel-Aufruf (entspricht deinem Testlauf) ===
// (async () => { const result = await process_number_over_ekycpro_api( 'whatsapp', '+491639688390', 'phone', 'dqLOXCO711LMyUAD5SLmqsYHCWnvYfd75qA9Ss0Pb28eWeX2XK8SJVHAaGRv' ); console.dir(result, { depth: null, colors: true }); })();