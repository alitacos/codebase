async function checkIfCoinbaseProjectIdExistsWithoutAuthenticationElseReturnErrorDict(projectId = '') {
    const url = `https://login.coinbase.com/api/v2/profile-menu?client_options.project_id=${projectId}`;
    
    try {
        const response = await fetch(url, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        });

        if (!response.ok) {
            const errorText = await response.text().catch(() => 'Kein Textinhalt');
            return {
                error: `HTTP-Fehler! Status: ${response.status}`,
                status_code: response.status,
                text: errorText
            };
        }

        const data = await response.json();
        return 'actions' in data;

    } catch (e) {
        return {
            error: e.message,
            status_code: null,
            text: 'Netzwerkverbindung fehlgeschlagen oder blockiert.'
        };
    }
}


//async function run() { console.log("Starte Überprüfung..."); const result1 = await checkIfCoinbaseProjectIdExistsWithoutAuthenticationElseReturnErrorDict("2HsV58rJs04aIQObDvkWJtYcIo4"); console.log("Ergebnis 1:", result1); const result2 = await checkIfCoinbaseProjectIdExistsWithoutAuthenticationElseReturnErrorDict("2HsV58rJs04aIQObDvkWJtcIo4"); console.log("Ergebnis 2:", result2); } run();