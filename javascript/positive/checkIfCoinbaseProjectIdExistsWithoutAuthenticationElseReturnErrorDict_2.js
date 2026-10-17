async function checkIfCoinbaseProjectIdExistsWithoutAuthenticationElseReturnErrorDict(projectId = '') {
    // Validiert die Existenz einer gegebenen Projekt-ID in Coinbase
    const url = `https://login.coinbase.com/api/v2/profile-menu?client_options.project_id=${projectId}`;
    
    let response;
    try {
        // Führt die Netzwerkanfrage nativ im Browser aus
        response = await fetch(url);
        
        // Liest den JSON-Inhalt der Antwort
        const data = await response.json();
        
        // Prüft direkt, ob der Schlüssel 'actions' im Objekt existiert (entspricht Python .keys())
        if ('actions' in data) {
            return true;
        } else {
            return false;
        }
    } catch (e) {
        // Fehler-Abfangblock analog zum Python-Code
        return {
            error: e.message,
            status_code: response ? response.status : null,
            text: response ? await response.text().catch(() => '') : ''
        };
    }
}

// Beispiel-Aufruf: Wartet auf das Ergebnis und gibt es sauber in der Konsole aus
// (async () => { const result1 = await checkIfCoinbaseProjectIdExistsWithoutAuthenticationElseReturnErrorDict("2HsV58rJs04aIQObDvkWJtYcIo4"); console.log(result1); const result2 = await checkIfCoinbaseProjectIdExistsWithoutAuthenticationElseReturnErrorDict("2HsV58rJs04aIQObDvkWJtcIo4"); console.log(result2); })();
