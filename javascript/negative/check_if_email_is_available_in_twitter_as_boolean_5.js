async function check_if_email_is_available_in_twitter_as_boolean(email = '') {
    if (!email) {
        email = '';
    }
    
    // 1. KORREKTUR: ${email} statt {email} verwenden
    // 2. KORREKTUR: Funktion direkt mit dem übergebenen 'email'-Argument aufrufen
    const generateUrl = (emailArg) => `https://x.com{encodeURIComponent(emailArg)}`;
    const url = generateUrl(email);

    let response;
    let data = {};
    try {
        // Jetzt ist 'url' ein fertiger String
        response = await fetch(url);
        const dict_response = await response.json();
        data = { 
            "error": null, 
            "status_code": response.status, 
            "valid": dict_response['valid'], 
            "msg": dict_response['msg'], 
            "taken": dict_response['taken']
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
    
    // Gibt true zurück, wenn die E-Mail FREI (not taken) ist, andernfalls false
    if (data['taken'] === true) {
        return false;
    }
    if (data['taken'] === false) {
        return true;
    }
    return false; // Fallback, falls 'taken' undefined ist
}

 