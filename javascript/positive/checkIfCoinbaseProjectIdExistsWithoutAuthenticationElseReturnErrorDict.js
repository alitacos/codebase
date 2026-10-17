async function checkIfCoinbaseProjectIdExistsWithoutAuthenticationElseReturnErrorDict(projectId = '') {
    const url = `https://login.coinbase.com/api/v2/profile-menu?client_options.project_id=${projectId}`;
    
    let response;
    try {
        response = await fetch(url);
        const data = await response.json();
        
        // Prüft, ob der Schlüssel 'actions' im Objekt existiert
        if ('actions' in data) {
            return true;
        } else {
            return false;
        }
    } catch (e) {
        return {
            error: e.message,
            status_code: response ? response.status : null,
            text: response ? await response.text().catch(() => '') : ''
        };
    }
}

// Beispiel-Aufruf (in einer asynchronen Umgebung):

// (async () => { console.log(await checkIfCoinbaseProjectIdExistsWithoutAuthenticationElseReturnErrorDict("2HsV58rJs04aIQObDvkWJtYcIo4")); // true console.log(await checkIfCoinbaseProjectIdExistsWithoutAuthenticationElseReturnErrorDict("2HsV58rJs04aIQObDvkWJtcIo4")); // false })();
