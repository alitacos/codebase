const dns = require('dns');

// Zwingt Node.js, IPv4 anstelle von IPv6 zu bevorzugen (löst den 'fetch failed' Netzwerk-Absturz)
if (typeof dns.setDefaultResultOrder === 'function') {
    dns.setDefaultResultOrder('ipv4first');
}

// Verhindert Verbindungsabbruch bei lokalen SSL-/Proxy-Strukturen
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

async function check_if_email_is_available_in_twitter_as_boolean(email = '') {
    if (!email) {
        email = '';
    }
    const url = `https://api.x.com/i/users/email_available.json?email={email}`;
    let response;
    let data = {};
    try {
        response = await fetch(url);
        
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