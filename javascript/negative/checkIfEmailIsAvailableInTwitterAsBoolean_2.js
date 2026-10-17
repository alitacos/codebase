// WICHTIG: Erlaubt Node.js, die SSL-Zertifikate von Cloudflare One zu akzeptieren
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

const HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
    'Referer': 'https://x.com',
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
 */
async function checkIfEmailIsAvailableInTwitterAsBoolean(email = '') {
    if (!email) email = '';
    const url = `https://api.x.com/i/users/email_available.json?email={encodeURIComponent(email)}`;
    let response;
    let data = {};

    try {
        response = await fetch(url, { 
            method: 'GET', 
            headers: HEADERS
        });
        
        // Prüfen, ob die Antwort HTML statt JSON ist (z.B. Cloudflare Block)
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            const textPreview = await response.text();
            throw new Error(`Kein JSON empfangen. Status: ${response.status}. Vorschau: ${textPreview.slice(0, 150)}`);
        }

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

    console.log("Daten:", data);

    if (data.taken === true) return false;
    if (data.taken === false) return true;
    return false;
}

