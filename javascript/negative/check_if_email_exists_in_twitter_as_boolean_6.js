
async function check_if_email_exists_in_twitter_as_boolean(email = '') {
    if (!email) {
        email = '';
    }
    const url = `https://api.x.com/i/users/email_available.json?email={email}`;
    let response;
    let data;
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
    if (!data) {
        return false;
    }
    console.log(data);
    if (data) {
        return data['taken'] !== undefined ? data['taken'] : '';
    }
}
 