import cheerio from 'cheerio';
// Hinweis: Ab Node.js 18 ist 'fetch' nativ integriert. 
// Falls Sie eine ältere Version nutzen, installieren Sie 'node-fetch' und importieren es hier.

/**
 * Wartet für eine bestimmte Anzahl an Millisekunden (Hilfsfunktion für das Delay)
 */
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

/**
 * Überprüft, ob ein Benutzername auf slides.com existiert.
 */
async function checkIfUsernameExistsInSlidesComViaCheerio(options = {}) {
    const {
        username = '',
        retries = 3,
        delay = 2, // in Sekunden
        url = 'https://slides.com/',
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9, image/avif,image/webp,*/*;q=0.8"
        },
        // Hinweis: Die Fetch-API verarbeitet Cookies im Header-String.
        // Bei Bedarf als 'Cookie': 'schluessel=wert' an die Headers übergeben.
        redirect = 'manual' // Entspricht 'allow_redirects=False'
    } = options;

    // Validierung des Benutzernamens
    if (!username || typeof username !== 'string' || !username.trim()) {
        return {
            error: 'invalid <username> value',
            status: null,
            username: username,
            content: null,
            title: null,
            available: false,
            exists: false
        };
    }

    const cleanUrl = url.trim().replace(/\/+$/, '');
    const cleanUsername = username.trim().replace(/^\/+|\/+$/g, '');
    const targetUrl = `${cleanUrl}/${cleanUsername}`;

    let lastError = null;

    for (let i = 0; i < retries; i++) {
        try {
            const response = await fetch(targetUrl, {
                method: 'GET',
                headers: headers,
                redirect: redirect
            });

            const html = await response.text();
            const $ = cheerio.load(html);

            // Text-Formatierung (Nachbildung der Python-Logik)
            const getCleanText = (element) => {
                return element.text()
                    .replace(/\t/g, '\n')
                    .split('\n')
                    .map(line => line.trim())
                    .filter(line => line.length > 0)
                    .join('\n');
            };

            if (response.status === 200) {
                const title = $('title').text().trim() || null;
                const content = getCleanText($('body')) || null;

                return {
                    error: false,
                    status: 200,
                    username: username,
                    content: content,
                    title: title,
                    available: false,
                    exists: true
                };
            }

            if (response.status === 404) {
                const title = $('title').text().trim() || null;
                const errorHeader = $('.errors-header');
                const content = errorHeader.length ? getCleanText(errorHeader) : null;

                return {
                    error: false,
                    status: 404,
                    username: username,
                    content: content,
                    title: title,
                    available: true,
                    exists: false
                };
            }

            lastError = `unexpected status_code ${response.status}`;
            await sleep(delay * 1000);

        } catch (error) {
            lastError = error.message;
            await sleep(delay * 1000);
        }
    }

    return {
        error: lastError,
        status: null,
        username: username,
        content: null,
        title: null,
        available: null,
        exists: null
    };
}

// === Beispiel für die Verwendung ===
// (async () => { const result = await checkIfUsernameExistsInSlidesComViaCheerio({ username: 'anna' }); console.log(result); })();
 