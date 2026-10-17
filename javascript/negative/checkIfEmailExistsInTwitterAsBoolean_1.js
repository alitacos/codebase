async function checkIfEmailExistsInTwitterAsBoolean(email = '') {
    if (!email) email = '';
    const url = `https://api.x.com/i/users/email_available.json?email={encodeURIComponent(email)}`;
    let response;
    let data = {};

    try {
        response = await fetch(url, { 
            method: 'GET', 
            headers: HEADERS
        });

        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            const textPreview = await response.text();
            throw new Error(`Kein JSON empfangen. Status: ${response.status}. Vorschau: ${textPreview.slice(0, 150)}`);
        }

        const dict_response = await response.json();
        
        data = { 
            "error": null, 
            "status_code": response.status, 
            "valid": dict_response.valid, 
            "msg": dict_response.msg, 
            "taken": dict_response.taken 
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

    console.log("Daten:", data);
    
    return data.taken ?? '';
}
