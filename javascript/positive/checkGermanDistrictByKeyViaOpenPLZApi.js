async function checkGermanDistrictByKeyViaOpenPLZApi(query = '', options = {}) {
    /**
     * Fetch districts from OpenPLZ API by federal state input (name, abbreviation, or key).
     * Accepts input as string or number.
     */
    const federalStates = [ {"ags": "01", "name": "Schleswig-Holstein", "short": "SH",'iso-3166-2':'DE-SH'}, {"ags": "02", "name": "Hamburg", "short": "HH",'iso-3166-2':'DE-HH'}, {"ags": "03", "name": "Niedersachsen", "short": "NI",'iso-3166-2':'DE-NI'}, {"ags": "04", "name": "Bremen", "short": "HB",'iso-3166-2':'DE-HB'}, {"ags": "05", "name": "Nordrhein-Westfalen", "short": "NW",'iso-3166-2':'DE-NW'}, {"ags": "06", "name": "Hessen", "short": "HE",'iso-3166-2':'DE-HE'}, {"ags": "07", "name": "Rheinland-Pfalz", "short": "RP",'iso-3166-2':'DE-RP'}, {"ags": "08", "name": "Baden-Württemberg", "short": "BW",'iso-3166-2':'DE-BW'}, {"ags": "09", "name": "Bayern", "short": "BY",'iso-3166-2':'DE-BY'}, {"ags": "10", "name": "Saarland", "short": "SL",'iso-3166-2':'DE-SL'}, {"ags": "11", "name": "Berlin", "short": "BE",'iso-3166-2':'DE-BE'}, {"ags": "12", "name": "Brandenburg", "short": "BB",'iso-3166-2':'DE-BB'}, {"ags": "13", "name": "Mecklenburg-Vorpommern", "short": "MV",'iso-3166-2':'DE-MV'}, {"ags": "14", "name": "Sachsen", "short": "SN",'iso-3166-2':'DE-SN'}, {"ags": "15", "name": "Sachsen-Anhalt", "short": "ST",'iso-3166-2':'DE-ST'}, {"ags": "16", "name": "Thüringen", "short": "TH",'iso-3166-2':'DE-TH'}];
// Helper to sanitize umlauts and normalize strings
    const normalize = (str) => String(str).trim().toLowerCase() .replace(/ü/g, "u") .replace(/ä/g, "a") .replace(/ö/g, "o");

    let processedQuery = query;

    try {
        // Convert number input to string with leading zero if needed (e.g., 8 -> "08")
        if (typeof query === 'number') {
            processedQuery = String(query).padStart(2, '0');
        } else {
            processedQuery = normalize(query);
        }

        let stateKey = null;
        for (const state of federalStates) {
            const agsNormal = state.ags;
            const agsNoZero = state.ags.replace(/^0+/, ''); // Python's lstrip("0")
            const nameNormal = normalize(state.name);
            const shortNormal = state.short.toLowerCase();

            if (processedQuery === agsNormal || processedQuery === agsNoZero || processedQuery === nameNormal || processedQuery === shortNormal) { stateKey = state.ags; break;
            }
        }

        if (!stateKey) {
            return { error: 'Could not resolve input', status: null, query: query, data: [] };
        }

        // Perform the API request using native fetch
        const url = `https://openplzapi.org/de/FederalStates/${stateKey}/Districts`;
        const response = await fetch(url, options);

        if (response.ok) { // checks for status 200-299
            const data = await response.json();
            return { error: false, status: response.status, query: query, data: data };
        }

        return { error: `unexpected status code ${response.status}`, status: response.status, query: query, data: [] };

    } catch (e) {
        return { error: `${e.message}, ${e.name}`, status: null, query: query, data: [] };
    }
}

// --- Example Usage ---
//(async () => { console.log("--- Test mit Kürzel 'HE' ---"); const resultByShort = await checkGermanDistrictByKeyViaOpenPLZApi("HE"); console.log(JSON.stringify(resultByShort, null, 2)); console.log("\n--- Test mit AGS-Nummer 6 ---"); const resultByNumber = await checkGermanDistrictByKeyViaOpenPLZApi(6); console.log(`Gefundene Landkreise: ${resultByNumber.data.length}`); if (resultByNumber.data.length > 0) { console.log("Erster Eintrag:", resultByNumber.data[0]); } console.log("\n--- Test mit Name 'Hessen' ---"); const resultByName = await checkGermanDistrictByKeyViaOpenPLZApi("Hessen"); console.log(`Erfolgreich? ${!resultByName.error}`); console.log("\n--- Test mit ungültiger Eingabe ---"); const resultError = await checkGermanDistrictByKeyViaOpenPLZApi("Fantasieland"); console.log(resultError); })();
