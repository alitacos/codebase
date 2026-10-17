async function check_if_email_is_available_in_twitter_and_get_infodict(email = '') {
    if (!email) {
        email = '';
    }
    
    let response;
    let data = {};
    try {
        // Das URL-Objekt baut die URL inklusive des Query-Parameters perfekt und sicher zusammen
        const url = new URL('https://api.x.com/i/users/email_available.json');
        url.searchParams.append('email', email);

        response = await fetch(url.toString());
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
    
    return data;
}

// === WICHTIG: Der Aufruf MUSS mit await umschlossen sein, um "Promise <pending>" zu verhindern ===
//(async () => { const info = await check_if_email_is_available_in_twitter_and_get_infodict('anon@gmail.com'); console.log(info); })();