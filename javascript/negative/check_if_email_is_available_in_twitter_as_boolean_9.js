// Verhindert einen Verbindungsabbruch durch Node.js bei lokalen SSL-/Proxy-Einschränkungen
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

async function check_if_email_is_available_in_twitter_as_boolean(email = '') {
    if (!email) {
        email = '';
    }
    // String-Interpolation via Backticks und ${email}
    const url = `https://api.x.com/i/users/email_available.json?email={email}`;
    let response;
    let data = {};
    try {
        response = await fetch(url);
        
        // Falls X mit einem HTTP-Fehlercode antwortet (z.B. 403, 429), werfen wir manuell einen Fehler
        if (!response.ok) {
            throw new Error(`X API Error (HTTP ${response.status})`);
        }
        
        const dict_response = await response.json();
        data = { 
            "error": null, 
            "status_code": response.status, 
            "valid": dict_response['valid'], 
            "msg": dict_response['msg'], 
            "taken": dict_response['taken']
        };
    } catch (e) {
        // Berechnet den Status-Code bei Blockaden (403/429) oder standardmäßig 500
        const statusCode = response ? response.status : 500;
        data = { 
            "error": e.message, 
            "status_code": statusCode, 
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
        if (data['taken'] === true) {
            return false;
        }
        if (data['taken'] === false) {
            return true;
        }
    }
}