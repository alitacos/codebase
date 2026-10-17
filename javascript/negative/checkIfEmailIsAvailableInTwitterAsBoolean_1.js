async function checkIfEmailIsAvailableInTwitterAsBoolean(email = '') {
    if (!email) return false;
    
    const url = `https://api.x.com/i/users/email_available.json?email={encodeURIComponent(email)}`;
    
    const headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://x.com/',
        'Origin': 'https://x.com',
        // WICHTIG: Falls X strikt blockiert, müssen hier die "auth_token" oder "guest_token" Cookies Ihres Browsers rein:
        // 'Cookie': 'auth_token=IHR_TOKEN; ct0=IHR_X_CSRF_TOKEN',
        // 'X-Csrf-Token': 'IHR_X_CSRF_TOKEN'
    };

    let response;
    let data = {};

    try {
        response = await fetch(url, { 
            method: 'GET', 
            headers: headers,
            credentials: 'include' // ZWINGT Node.js/Browser Cookies und Anmeldedaten zu verarbeiten
        });

        // Prüfen ob die API blockiert oder HTML liefert
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            const rawText = await response.text();
            throw new Error(`X verlangt Authentifizierung (HTML empfangen). Status: ${response.status}`);
        }

        const dict_response = await response.json();
        
        data = { 
            "error": null, 
            "status_code": response.status, 
            "valid": dict_response.valid ?? false, 
            "msg": dict_response.msg ?? null, 
            "taken": dict_response.taken ?? false 
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

    // Ihre exakte Python-Logik übersetzt:
    if (!data) return false;
    if (data.taken === true) return false;
    if (data.taken === false) return true;
    return false;
}
