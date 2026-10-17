async function checkGermanFederalStateDataViaLadiesDeApi(regionInput = '') {
    const federalStates =   [{"ags": "01", "name": "Schleswig-Holstein", "short": "SH",'iso-3166-2':'DE-SH'},{"ags": "02", "name": "Hamburg", "short": "HH",'iso-3166-2':'DE-HH'},{"ags": "03", "name": "Niedersachsen", "short": "NI",'iso-3166-2':'DE-NI'},{"ags": "04", "name": "Bremen", "short": "HB",'iso-3166-2':'DE-HB'},{"ags": "05", "name": "Nordrhein-Westfalen", "short": "NW",'iso-3166-2':'DE-NW'},{"ags": "06", "name": "Hessen", "short": "HE",'iso-3166-2':'DE-HE'},{"ags": "07", "name": "Rheinland-Pfalz", "short": "RP",'iso-3166-2':'DE-RP'},{"ags": "08", "name": "Baden-Württemberg", "short": "BW",'iso-3166-2':'DE-BW'},{"ags": "09", "name": "Bayern", "short": "BY",'iso-3166-2':'DE-BY'},{"ags": "10", "name": "Saarland", "short": "SL",'iso-3166-2':'DE-SL'},{"ags": "11", "name": "Berlin", "short": "BE",'iso-3166-2':'DE-BE'},{"ags": "12", "name": "Brandenburg", "short": "BB",'iso-3166-2':'DE-BB'},{"ags": "13", "name": "Mecklenburg-Vorpommern", "short": "MV",'iso-3166-2':'DE-MV'},{"ags": "14", "name": "Sachsen", "short": "SN",'iso-3166-2':'DE-SN'},{"ags": "15", "name": "Sachsen-Anhalt", "short": "ST",'iso-3166-2':'DE-ST'},{"ags": "16", "name": "Thüringen", "short": "TH",'iso-3166-2':'DE-TH'}    ];

    
    const normalize = (text = '') => {
        return String(text) .toLowerCase() .replace(/ü/g, "ue") .replace(/ä/g, "ae") .replace(/ö/g, "oe") .replace(/ß/g, "ss") .trim(); };

    // Normalize input for matching
    let userInput;
    if (typeof regionInput === 'number') {
        userInput = String(regionInput).padStart(2, '0');
    } else {
        userInput = normalize(regionInput);
    }

    // Find matching state
    let matchedState = null;
    for (const state of federalStates) {
        const key = state.ags;
        const name = normalize(state.name);
        const short = state.short.toLowerCase();

        // Check if string matches code without leading zero
        const keyLstrip = key.replace(/^0+/, '');

        if (userInput === key || userInput === keyLstrip || userInput === name || userInput === short) {
            matchedState = state;
            break;
        }
    }

    if (!matchedState) {
        console.log(`Input '${regionInput}' is not a recognized German federal state.`);
        return null;
    }

    // Build URL with query parameters
    const url = new URL("https://www.ladies.de/api/location/");
    url.searchParams.append("searchString", matchedState.name);
    url.searchParams.append("searchAddAlleRegionen", "false");

    try {
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (e) {
        console.log(`Request failed: ${e.message}`);
        return [];
    }
}

// Example Usages:

// (async () => { console.log(await checkGermanFederalStateDataViaLadiesDeApi("BW")); console.log(await checkGermanFederalStateDataViaLadiesDeApi(8)); console.log(await checkGermanFederalStateDataViaLadiesDeApi("baden-wuerttemberg")); })();
