const cheerio = require('cheerio');

/**
 * Hilfsfunktion für das Delay (entspricht time.sleep)
 */
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

/**
 * Überprüft, ob ein Username auf slides.com existiert.
 */
async function checkIfUsernameExistsInSlidesComViaRequestsAndBs4({
    username = '',
    retries = 3,
    delay = 2,
    url = 'https://slides.com/',
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9, image/avif,image/webp,*/*;q=0.8"
    },
    cookies = {},
    allowRedirects = false
} = {}) {

    // 1. Validierung (Analog zu Python)
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

    // Cookie-Header zusammenbauen, falls vorhanden
    const finalHeaders = { ...headers };
    if (Object.keys(cookies).length > 0) {
        finalHeaders["Cookie"] = Object.entries(cookies).map(([k, v]) => `${k}=${v}`).join('; ');
    }

    // URL sauber formatieren
    const cleanUrl = url.trim().replace(/\/+$/, '');
    const cleanUsername = username.trim().replace(/^\/+|\/+$/g, '');
    const targetUrl = `${cleanUrl}/${cleanUsername}`;

    let lastError = null;

    for (let i = 0; i < retries; i++) {
        try {
            // HTTP GET-Anfrage absetzen
            const response = await fetch(targetUrl, {
                method: 'GET',
                headers: finalHeaders,
                redirect: allowRedirects ? 'follow' : 'manual'
            });

            const responseText = await response.text();
            
            // Cheerio lädt das HTML (äquivalent zu BeautifulSoup)
            const $ = cheerio.load(responseText);

            // Hilfsfunktion zur Text-Formatierung (Tabs entfernen, Splitten, Bereinigen)
            const formatText = (text) => {
                if (!text) return null;
                return text
                    .replace(/\t/g, '\n')
                    .trim()
                    .split('\n')
                    .map(line => line.trim())
                    .filter(line => line !== '')
                    .join('\n');
            };

            const title = $('title').text().trim() || null;

            // 2. Status 200: User existiert
            if (response.status === 200) {
                // Gesamten Textinhalt der Seite holen (entspricht soup.get_text())
                const fullText = $('body').text(); 
                
                return {
                    error: false,
                    status: 200,
                    username: username,
                    content: formatText(fullText),
                    title: title,
                    available: false,
                    exists: true
                };
            }

            // 3. Status 404: User existiert nicht
            if (response.status === 404) {
                // Sucht nach <div class="errors-header">
                const errorDivText = $('div.errors-header').text();

                return {
                    error: false,
                    status: 404,
                    username: username,
                    content: formatText(errorDivText),
                    title: title,
                    available: true,
                    exists: false
                };
            }

            lastError = `unexpected status_code ${response.status}`;
            await sleep(delay * 1000);
            continue;

        } catch (e) {
            lastError = e.message;
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

// --- example usage ---
// async function main() { console.log("--- Test: anna ---"); const result = await checkIfUsernameExistsInSlidesComViaRequestsAndBs4({ username: 'anna' }); console.log(result); } main();
