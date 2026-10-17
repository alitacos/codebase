async function check_if_email_is_available_in_twitter_as_boolean(email = '') {
    if (!email) {
        email = '';
    }
    
    // HIER IST IHRE URL: Der Platzhalter {email} wird direkt durch den echten Wert ersetzt
    const url = `https://api.x.com/i/users/email_available.json?email={email}`.replace('{email}', encodeURIComponent(email));

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

// === example usage ===
//(async () => { console.log(await check_if_email_is_available_in_twitter_as_boolean('f')); console.log(await check_if_email_is_available_in_twitter_as_boolean('anon@grr.la')); console.log(await check_if_email_is_available_in_twitter_as_boolean('alitakos9s0@gmail.com')); })();