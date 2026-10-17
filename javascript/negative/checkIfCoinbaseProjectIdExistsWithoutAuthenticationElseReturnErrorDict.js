const request = require('sync-request');

function checkIfCoinbaseProjectIdExistsWithoutAuthenticationElseReturnErrorDict(projectId = '') {
    const url = `https://login.coinbase.com/api/v2/profile-menu?client_options.project_id=${projectId}`;
    
    let response;
    try {
        response = request('GET', url, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }
        });

        // Parsen des JSON-Bodys (entspricht response.json() in Python)
        const data = JSON.parse(response.getBody('utf8'));
        
        // Holt alle Keys des Objekts (entspricht .keys() in Python)
        const keys = Object.keys(data);
        
        if (keys.includes('actions')) {
            return true;
        } else {
            return false;
        }
    } catch (e) {
        // Fehler-Abfangblock analog zum Python 'except Exception as e'
        return {
            error: e.message,
            status_code: response ? response.statusCode : null,
            text: response ? response.getBody('utf8') : ''
        };
    }
}

//console.log(checkIfCoinbaseProjectIdExistsWithoutAuthenticationElseReturnErrorDict("2HsV58rJs04aIQObDvkWJtYcIo4")); // True
//console.log(checkIfCoinbaseProjectIdExistsWithoutAuthenticationElseReturnErrorDict("2HsV58rJs04aIQObDvkWJtcIo4")); // False
