// Falls in Node.js genutzt, installiere zuerst cheerio: npm install cheerio
// Falls im Browser genutzt, muss fetch und ein DOMParser verwendet werden.
//import * as cheerio from 'cheerio'; 
const cheerio = require('cheerio'); // Nutze require um den SyntaxError zu vermeiden

/**
 * Hilfsfunktion für die Verzögerung (Sleep/Delay) bei Retries
 */
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

/**
 * Ruft die Telefonvorwahl für eine deutsche Postleitzahl ab.
 * 
 * @param {string|number} postalcode - Deutsche Postleitzahl (4-5 Ziffern).
 * @param {number} retries - Anzahl der Wiederholungsversuche bei Fehlern.
 * @param {number} delay - Verzögerung in Sekunden zwischen den Versuchen.
 * @param {string} url - Ziel-URL für die Abfrage.
 * @param {Object} headers - Optionale HTTP-Header.
 * @param {string} cookies - Optionale Cookie-Zeichenkette.
 * @param {boolean} allowRedirects - Ob Weiterleitungen erlaubt sind.
 * @returns {Promise<Object>} Ergebnisobjekt mit Vorwahl oder Fehlermeldung.
 */
async function fetchAreaDialCodeByGermanPostalcodePerPlzVorwahlApiViaCheerio(
    postalcode = '', 
    retries = 3, 
    delay = 2, 
    url = 'https://www.plz-vorwahl.de/', 
    headers = {}, 
    cookies = {}, 
    allowRedirects = false
) {
    const pcString = String(postalcode).trim();

    // Validierung der Postleitzahl (analog zum Python-Code)
    if (!postalcode || isNaN(pcString) || pcString === '' || ![4, 5].includes(pcString.length)) {
        return { error: 'invalid postalcode', status: null, query: postalcode, dial_code: '' };
    }

    // PLZ auf 5 Stellen mit führenden Nullen formatieren
    const formattedPlz = pcString.padStart(5, '0');
    
    // URL mit Query-Parameter aufbauen (?s=XXXXX)
    const targetUrl = new URL(url);
    targetUrl.searchParams.append('s', formattedPlz);

    // Header vorbereiten (inklusive Cookies, falls vorhanden)
    const fetchHeaders = { ...headers };
    if (Object.keys(cookies).length > 0) {
        // Konvertiert Cookie-Objekt {key: "val"} in "key=val" String für den Header
        fetchHeaders['Cookie'] = Object.entries(cookies)
            .map(([key, val]) => `${key}=${val}`)
            .join('; ');
    }

    let lastError = null;
    let status = null;

    for (let i = 0; i < retries; i++) {
        try {
            const response = await fetch(targetUrl.toString(), {
                method: 'GET',
                headers: fetchHeaders,
                redirect: allowRedirects ? 'follow' : 'manual'
            });

            status = response.status;

            if (status === 200) {
                const html = await response.text();
                const $ = cheerio.load(html);
                
                // Extrahiere den Text aus body -> .post_title
                const titleText = $('body').find('div.post_title').text() || '';
                
                // HTML Parsing Logik analog zu Python: 
                // Splitten bei '–', filtern nach 'Vorwahl ', und Ziffern extrahieren
                const segments = titleText.split('–');
                let dialCode = '';

                for (const segment of segments) {
                    if (segment && segment.includes('Vorwahl ')) {
                        // Findet alle zusammenhängenden Zahlenfolgen im Segment
                        const matches = segment.match(/\d+/g); 
                        if (matches && matches.length > 0) {
                            dialCode = matches[0]; // Nimm die erste gefundene Zahl
                            break;
                        }
                    }
                }

                return {
                    error: false,
                    status: 200,
                    query: pcString,
                    dial_code: dialCode
                };
            }

            lastError = `unexpected status code ${status}`;
            if (i < retries - 1) await sleep(delay * 1000);

        } catch (error) {
            lastError = error.message;
            status = null;
            if (i < retries - 1) await sleep(delay * 1000);
        }
    }

    return { error: lastError, status: status, query: pcString, dial_code: '' };
}

// --- Testaufruf ---
// (async () => { const result = await fetchAreaDialCodeByGermanPostalcodePerPlzVorwahlApiViaCheerio('70197'); console.log(result); })();