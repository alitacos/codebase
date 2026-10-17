/**
 * Prüft, ob eine E-Mail-Adresse bei X (Twitter) bereits registriert ist.
 * @param {string} email - Die zu prüfende E-Mail-Adresse.
 * @returns {Promise<boolean>} - Gibt true zurück, wenn die E-Mail vergeben ist, andernfalls false.
 */
async function checkIfEmailExistsInTwitterAsBoolean(email = '') {
    if (!email) {
        email = '';
    }
    
    const url = `https://api.x.com/i/users/email_available.json?email={encodeURIComponent(email)}`;
    
    // Notwendige Browser-Header, um eine Blockade durch X zu verhindern
    const headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://x.com/',
        'Origin': 'https://x.com',
        'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site'
    };

    let data;
    let statusCode = 500;

    try {
        const response = await fetch(url, { method: 'GET', headers: headers });
        statusCode = response.status;

        // Versuche die JSON-Antwort zu parsen
        const dictResponse = await response.json();
        
        data = {
            "error": null,
            "status_code": statusCode,
            "valid": dictResponse.valid ?? false,
            "msg": dictResponse.msg ?? null,
            "taken": dictResponse.taken ?? false
        };
    } catch (e) {
        // Fängt JSON-Fehler (HTML/Cloudflare-Blockaden) und Netzwerkfehler ab
        data = {
            "error": e.message,
            "status_code": statusCode,
            "valid": false,
            "msg": null,
            "taken": false
        };
    }

    if (!data) {
        return false;
    }

    console.log(data);
    
    // Gibt das Feld 'taken' als Boolean zurück (entspricht data.get('taken', ''))
    return Boolean(data.taken);
}

// === Beispiel-Aufrufe (Ausführung in einer async-Umgebung) ===
//(async () => { console.log("Ergebnis 1:", await checkIfEmailExistsInTwitterAsBoolean('f')); console.log("Ergebnis 2:", await checkIfEmailExistsInTwitterAsBoolean('anon@grr.la')); })();