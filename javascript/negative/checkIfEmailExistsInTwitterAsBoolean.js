async function checkIfEmailExistsInTwitterAsBoolean(email = '') {
    if (!email) return false;
    
    const url = `https://x.com{encodeURIComponent(email)}`;
    
    const headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://x.com/',
        'Origin': 'https://x.com'
    };

    let response;
    let data = {};

    try {
        response = await fetch(url, { 
            method: 'GET', 
            headers: headers,
            credentials: 'include'
        });

        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            throw new Error(`X verlangt Authentifizierung. Status: ${response.status}`);
        }

        const dict_response = await response.json();
        
        data = { 
            "error": null, 
            "status_code": response.status, 
            "valid": dict_response.valid ?? false, 
            "msg": dict_response.msg ?? null, 
            "taken": dict_response.taken ?? false 
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
    
    if (!data) return false;
    return data.taken ?? '';
}

 