
async function check_if_email_exists_in_twitter_as_boolean(email = '') {
    if (!email) {
        email = '';
    }
    // KORREKTUR: Backticks und ${email} für die korrekte Variablen-Einsetzung
    const url = `https://x.com{email}`;
    let response;
    let data;
    try {
        response = await axios.get(url);
        const dict_response = response.data;
        data = { 
            "error": null, 
            "status_code": response.status, 
            "valid": dict_response['valid'], 
            "msg": dict_response['msg'], 
            "taken": dict_response['taken']
        };
    } catch (e) {
        const statusCode = e.response ? e.response.status : 500;
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
 