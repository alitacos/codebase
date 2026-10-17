async function getJobtermSuggestionsInfoOverArgeJobboerseApiViaRequests(query = '', angebotsart = 1, limit = 100, retries = 3, delay = 2, url = 'https://rest.arbeitsagentur.de/jobboerse/suggest-service/ed/v2/jobsuche/vorschlaege', headers = {"X-API-Key":"jobboerse-jobsuche","Accept":"application/json"}, cookies = {}, allowRedirects = false) {
    if (!query || typeof query !== 'string' || !query.trim()) {
        return {error:'missing <query> value of job term',suggestions:[],terms:[]};
    }

    let last_error = null;

    for (let i = 0; i < retries; i++) {
        try {
            const params = new URLSearchParams({
                angebotsart: angebotsart,
                limit: limit,
                suchbegriff: query,
                typeahead: 'true'
            });

            const cookieString = Object.entries(cookies).map(([k,v]) => `${k}=${v}`).join('; ');

            const fetchHeaders = {...headers};

            if (cookieString) {
                fetchHeaders["Cookie"] = cookieString;
            }

            const response = await fetch(`${url}?${params.toString()}`, {
                method:"GET",
                headers:fetchHeaders,
                redirect:allowRedirects ? "follow" : "manual"
            });

            if (response.status === 200) {
                const suggestions_info = await response.json();

                if (suggestions_info) {
                    return {
                        error:false,
                        suggestions:suggestions_info.filter(i => i),
                        terms:suggestions_info.filter(i => i && typeof i === 'object' && i.vorschlag).map(i => i.vorschlag || '')
                    };
                }

                return {error:false,suggestions:[],terms:[]};
            }

            last_error = `unexpected status_code ${response.status}`;

        } catch (e) {
            last_error = String(e);
        }

        await new Promise(resolve => setTimeout(resolve, delay * 1000));
    }

    return {error:last_error,suggestions:[],terms:[]};
}


// example usage:
// (async()=>{console.log(await getJobtermSuggestionsInfoOverArgeJobboerseApiViaRequests('it'));})();