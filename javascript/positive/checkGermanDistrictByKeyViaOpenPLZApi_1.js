async function checkGermanDistrictByKeyViaOpenPLZApi( query = '', options = {} ){
    // Set up defaults matching your Python signature
    const headers = options.headers || { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36", "Accept": "*/*" };
    const allowRedirects = options.allowRedirects !== undefined ? options.allowRedirects : false;
    const timeout = options.timeout !== undefined ? options.timeout : 3; // in seconds

    const federalStates = [ {"ags": "01", "name": "Schleswig-Holstein", "short": "SH",'iso-3166-2':'DE-SH'}, {"ags": "02", "name": "Hamburg", "short": "HH",'iso-3166-2':'DE-HH'}, {"ags": "03", "name": "Niedersachsen", "short": "NI",'iso-3166-2':'DE-NI'}, {"ags": "04", "name": "Bremen", "short": "HB",'iso-3166-2':'DE-HB'}, {"ags": "05", "name": "Nordrhein-Westfalen", "short": "NW",'iso-3166-2':'DE-NW'}, {"ags": "06", "name": "Hessen", "short": "HE",'iso-3166-2':'DE-HE'}, {"ags": "07", "name": "Rheinland-Pfalz", "short": "RP",'iso-3166-2':'DE-RP'}, {"ags": "08", "name": "Baden-Württemberg", "short": "BW",'iso-3166-2':'DE-BW'}, {"ags": "09", "name": "Bayern", "short": "BY",'iso-3166-2':'DE-BY'}, {"ags": "10", "name": "Saarland", "short": "SL",'iso-3166-2':'DE-SL'}, {"ags": "11", "name": "Berlin", "short": "BE",'iso-3166-2':'DE-BE'}, {"ags": "12", "name": "Brandenburg", "short": "BB",'iso-3166-2':'DE-BB'}, {"ags": "13", "name": "Mecklenburg-Vorpommern", "short": "MV",'iso-3166-2':'DE-MV'}, {"ags": "14", "name": "Sachsen", "short": "SN",'iso-3166-2':'DE-SN'}, {"ags": "15", "name": "Sachsen-Anhalt", "short": "ST",'iso-3166-2':'DE-ST'}, {"ags": "16", "name": "Thüringen", "short": "TH",'iso-3166-2':'DE-TH'}];


    try {
        let cleanQuery = '';
        
        // Convert int input to string with leading zero if needed
        if (typeof query === 'number') {
            cleanQuery = String(query).padStart(2, '0');
        } else {
            cleanQuery = String(query);
        }

        // Clean query string (lowercase and replace umlauts)
        cleanQuery = cleanQuery.trim().toLowerCase() .replace(/ü/g, "u") .replace(/ä/g, "a") .replace(/ö/g, "o");

        let stateKey = null;

        for (const state of federalStates) {
            const cleanStateName = state.name.toLowerCase() .replace(/ü/g, "u") .replace(/ä/g, "a") .replace(/ö/g, "o");
            
            // Remove leading zero from ags for comparison
            const agsNoLeadingZero = state.ags.replace(/^0+/, '');

            // Check matching conditions
            if ( cleanQuery === state.ags || cleanQuery === agsNoLeadingZero || cleanQuery === cleanStateName || cleanQuery === state.short.toLowerCase() ){
                stateKey = state.ags;
                break;
            }
        }

        // If no federal state matches the query, exit early
        if (!stateKey) {
            return { error: 'Could not resolve input to a federal state', status: null, query: query, data: [] };
        }

        // Setup fetch configuration, including a timeout mechanism
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), timeout * 1000);

        const fetchOptions = { method: 'GET', headers: headers, redirect: allowRedirects ? 'follow' : 'manual', signal: controller.signal };

        const response = await fetch(`https://openplzapi.org/de/FederalStates/${stateKey}/Districts`, fetchOptions);
        clearTimeout(timeoutId);

        if (response.status === 200) {
            const jsonData = await response.json();
            return { error: false, status: response.status, query: query, data: jsonData };
        }

        return { error: `unexpected status code ${response.status}`, status: response.status, query: query, data: [] };

    } catch (e) {
        return { error: `${e.message}, ${e.name}`, status: null, query: query, data: [] };
    }
}

 
// Example usage
// (async () => { console.log("--- Test 1: Standard-Abfrage (Kürzel 'NW') ---"); const test1 = await checkGermanDistrictByKeyViaOpenPLZApi("NW"); console.log(`Erfolg: ${!test1.error}, Status: ${test1.status}, Landkreise gefunden: ${test1.data.length}`); if (test1.data.length > 0) console.log("Erster Eintrag:", test1.data[0]); console.log("\n--- Test 2: Abfrage mit sehr kurzem Timeout (0.01 Sekunden) ---"); const test2 = await checkGermanDistrictByKeyViaOpenPLZApi("Bayern", { timeout: 0.01 }); console.log(`Fehlermeldung bei Timeout: "${test2.error}"`); console.log("\n--- Test 3: Abfrage mit Custom-Headers (Zahl 9 für Bayern) ---"); const customOptions = { headers: { "User-Agent": "MyCustomApp/1.0", "Accept": "application/json" }, allowRedirects: true, timeout: 5 }; const test3 = await checkGermanDistrictByKeyViaOpenPLZApi(9, customOptions); console.log(`Erfolg: ${!test3.error}, Status: ${test3.status}`); console.log("\n--- Test 4: Ungültiges Bundesland ---"); const test4 = await checkGermanDistrictByKeyViaOpenPLZApi("Mallorca"); console.log(test4); })();
