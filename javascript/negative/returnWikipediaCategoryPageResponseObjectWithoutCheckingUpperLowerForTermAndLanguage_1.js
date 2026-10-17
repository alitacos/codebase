async function returnWikipediaCategoryPageResponseObjectWithoutCheckingUpperLowerForTermAndLanguage(term = '', verbose = false, retries = 2, delay = 2, langcode = 'en', headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/104.0 Safari/537.36" }, ...kwargs) {

    let status_code = null;
    let error = null;
    let raw = null;

    if (!term) {
        return null;
    }

    for (let attempt = 0; attempt < Number(retries); attempt++) {
        try {
            if (Buffer.isBuffer(term)) {
                term = term.toString('utf-8');
            }

            const url = `https://${String(langcode).toLowerCase().trim() || 'en'}.wikipedia.org/wiki/Category:${String(term).trim()}`;

            const req = await fetch(url, { headers: headers, ...kwargs });
            status_code = req.status;
            raw = await req.clone().text();

            if (status_code !== 200) {
                error = `Error: Status code ${status_code}`;
            }

            if (!error) {
                if (verbose) {
                    console.log({ error: error, status: status_code, Response: req, raw: raw });
                }
                return req;
            }

            if (attempt < retries - 1) {
                await new Promise(resolve => setTimeout(resolve, delay * 1000));
                continue;
            }

        } catch (e) {
            error = String(e);

            if (verbose) {
                console.log({ error: error, status: status_code, Response: null, raw: raw });
            }

            if (attempt < retries - 1) {
                await new Promise(resolve => setTimeout(resolve, delay * 1000));
            }
        }
    }

    if (verbose) {
        console.log({ error: error, status: status_code, Response: null, raw: raw });
    }

    return null;
}

//returnWikipediaCategoryPageResponseObjectWithoutCheckingUpperLowerForTermAndLanguage('medicine', true);