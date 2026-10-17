async function check_if_email_is_available_in_twitter_and_get_infodict(email = '') {
    if (!email) {
        email = '';
    }
    
    // Der Platzhalter {email} wird durch den echten, codierten Wert ersetzt
    const url = `https://x.com{email}`.replace('{email}', encodeURIComponent(email));

    let response;
    let data = {};
    try {
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
    
    // Gibt das gesamte JSON-Objekt zurück
    return data;
}

// === Beispielaufruf ===
//(async () => { const info = await check_if_email_is_available_in_twitter_and_get_infodict('alitakos9s0@gmail.com'); console.log(info); })();