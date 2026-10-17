// Gemeinsame Header für beide Funktionen, um Browser-Verhalten zu simulieren
const HEADERS = {
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

/**
 * 1. PRÜFT OB DIE E-MAIL VERFÜGBAR (FREI) IST
 * Gibt true zurück, wenn frei. Gibt false zurück, wenn bereits vergeben.
 */
async function checkIfEmailIsAvailableInTwitterAsBoolean(email = '') {
    if (!email) {
        email = '';
    }
    const url = `https://api.x.com/i/users/email_available.json?email={encodeURIComponent(email)}`;
    let response;
    let data = {};

    try {
        response = await fetch(url, { method: 'GET', headers: HEADERS });
        const dict_response = await response.json();
        
        data = { 
            "error": null, 
            "status_code": response.status, 
            "valid": dict_response.valid, 
            "msg": dict_response.msg, 
            "taken": dict_response.taken 
        };
    } catch (e) {
        data = { 
            "error": e.message, 
            "status_code": response ? response.status : 500, 
            "valid": false, 
            "msg": null, 
            "taken": null 
        };
    }

    console.log(data);

    if (!data) {
        return false;
    }
    
    if (data) {
        if (data.taken === true) {
            return false;
        }
        if (data.taken === false) {
            return true;
        }
    }
}

/**
 * 2. PRÜFT OB DIE E-MAIL EXISTIERT (BEREITS VERGEBEN IST)
 * Gibt true zurück, wenn vergeben. Gibt false zurück, wenn frei.
 */
async function checkIfEmailExistsInTwitterAsBoolean(email = '') {
    if (!email) {
        email = '';
    }
    const url = `https://x.com{encodeURIComponent(email)}`;
    let response;
    let data;

    try {
        response = await fetch(url, { method: 'GET', headers: HEADERS });
        const dict_response = await response.json();
        
        // Logik aus Ihrem Code (isvalid wird berechnet, aber im data-Objekt nicht überschrieben)
        const isvalid = ['Diese E-Mail-Adresse wird bereits verwendet', 'Verfügbar!'].includes(dict_response.msg) ? true : false;
        
        data = { 
            "error": null, 
            "status_code": response.status, 
            "valid": dict_response.valid, 
            "msg": dict_response.msg, 
            "taken": dict_response.taken 
        };
    } catch (e) {
        data = { 
            "error": e.message, 
            "status_code": response ? response.status : 500, 
            "valid": false, 
            "msg": null, 
            "taken": null 
        };
    }

    if (!data) {
        return false;
    }
    
    console.log(data);
    
    if (data) {
        return data.taken ?? '';
    }
}

// === Beispiel-Aufrufe (Ausführung in einer async-IIFE) ===
//(async () => { console.log("--- Test: Ist E-Mail VERFÜGBAR? ---"); await checkIfEmailIsAvailableInTwitterAsBoolean('f'); await checkIfEmailIsAvailableInTwitterAsBoolean('anon@grr.la'); await checkIfEmailIsAvailableInTwitterAsBoolean('alitakos9s0@gmail.com'); console.log("\n--- Test: EXISTIERT die E-Mail bereits? ---"); await checkIfEmailExistsInTwitterAsBoolean('f'); await checkIfEmailExistsInTwitterAsBoolean('anon@grr.la'); await checkIfEmailExistsInTwitterAsBoolean('alitakos9s0@gmail.com'); })();