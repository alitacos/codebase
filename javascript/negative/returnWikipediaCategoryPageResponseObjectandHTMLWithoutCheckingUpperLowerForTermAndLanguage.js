async function returnWikipediaCategoryPageResponseObjectandHTMLWithoutCheckingUpperLowerForTermAndLanguage(
    term = '',
    verbose = false,
    retries = 2,
    delay = 2,
    langcode = 'en',
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/104.0 Safari/537.36"
    },
    ...kwargs
) {
    let status_code = null;
    let error = null;

    if (!term) {
        return null;
    }

    for (let attempt = 0; attempt < Number(retries); attempt++) {
        try {
            if (Buffer.isBuffer(term) || term instanceof Uint8Array) {
                term = new TextDecoder("utf-8").decode(term);
            }

            const lang = langcode ? String(langcode).toLowerCase().trim() : "en";

            const url = `https://${lang}.wikipedia.org/wiki/Category:${String(term).trim()}`;

            const response = await fetch(url, {
                method: "GET",
                headers: headers,
                ...kwargs
            });

            status_code = response.status;

            if (status_code !== 200) {
                error = `Error: Status code ${status_code}`;
            }

            if (!error) {
                const html = await response.text();

                if (verbose) {
                    console.log({
                        error: error,
                        status: status_code,
                        Response: response,
                        html: html
                    });
                }

                return {
                    response: response,
                    status: status_code,
                    text: html,
                    url: url
                };
            }

            if (attempt < retries - 1) {
                await new Promise(resolve => setTimeout(resolve, delay * 1000));
                continue;
            }

        } catch (e) {
            error = String(e);

            if (verbose) {
                console.log(`Exception: ${error}`);
            }

            if (attempt < retries - 1) {
                await new Promise(resolve => setTimeout(resolve, delay * 1000));
            }
        }
    }

    if (verbose) {
        console.log({
            error: error,
            status: status_code,
            Response: null,
            html: ''
        });
    }

    return null;
}

