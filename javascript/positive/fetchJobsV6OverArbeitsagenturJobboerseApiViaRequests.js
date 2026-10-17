async function fetchJobsV6OverArbeitsagenturJobboerseApiViaRequests( postalcode = '', angebotsart = '1;2;4;34', umkreis = 0, page = 1, size = 250, pav = false, facetten = false, retries = 3, delay = 2, url = 'https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v6/jobs', headers = { 'Accept': 'application/json, text/plain, */*', 'User-Agent': 'Mozilla/5.0', 'Origin': 'https://www.arbeitsagentur.de', 'X-API-Key': 'jobboerse-jobsuche' }, cookies = {}, allow_redirects = false ) {
    if (!postalcode || !['string', 'number'].includes(typeof postalcode) || !String(postalcode).trim() || !String(postalcode).trim().match(/^\d+$/) || ![4, 5].includes(String(postalcode).trim().length))
        return { error: 'invalid <postalcode>', status: null, query: String(postalcode).trim(), records: [] };

    let last_error = null;
    let status_code = null;

    for (let attempt = 0; attempt < retries; attempt++) {
        try {
            const params = new URLSearchParams({
                angebotsart: String(angebotsart).trim(),
                wo: String(parseInt(String(postalcode).trim())).padStart(5, '0'),
                umkreis: String(parseInt(String(umkreis).trim())),
                page: String(parseInt(String(page).trim())),
                size: String(parseInt(String(size).trim())),
                pav: String(pav).trim().toLowerCase(),
                facetten: String(facetten).trim().toLowerCase()
            });

            const response = await fetch(`${url}?${params.toString()}`, {
                method: 'GET',
                headers: headers,
                redirect: allow_redirects ? 'follow' : 'manual'
            });

            status_code = response.status;

            if (status_code === 200) {
                return {
                    error: false,
                    status: 200,
                    query: String(postalcode).trim(),
                    records: await response.json()
                };
            }

            last_error = `unexpected status code ${status_code}`;

            if (attempt < retries - 1)
                await new Promise(resolve => setTimeout(resolve, delay * 1000));

        } catch (e) {
            last_error = String(e);
            status_code = null;

            if (attempt < retries - 1)
                await new Promise(resolve => setTimeout(resolve, delay * 1000));
        }
    }

    return {
        error: last_error,
        status: status_code,
        query: String(postalcode).trim(),
        records: {}
    };
}


// (async function() {   const result = await fetchJobsV6OverArbeitsagenturJobboerseApiViaRequests('70197');
//   console.dir(result, { depth: null });})();