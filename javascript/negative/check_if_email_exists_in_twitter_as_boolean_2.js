
async function check_if_email_exists_in_twitter_as_boolean(email = '') {
    if (!email) {
        email = '';
    }
    const url = `https://api.x.com/i/users/email_available.json?email={email}`;
    let response;
    let data;
    try {
        response = await axios.get(url);
        const dict_response = response.data;
        const isvalid = ['Diese E-Mail-Adresse wird bereits verwendet', 'Verfügbar!'].includes(dict_response['msg']) ? true : false; 
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