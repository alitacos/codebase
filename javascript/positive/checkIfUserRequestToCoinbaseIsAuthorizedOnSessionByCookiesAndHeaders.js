/**
 * Validiert, ob ein Benutzer bei Coinbase autorisiert ist.
 * @param {Object} [cookies=null] - Ein Objekt mit den Session-Cookies.
 * @param {Object} [headers=null] - Ein Objekt mit den HTTP-Headern.
 * @param {boolean} [verbose=false] - Aktiviert detaillierte Fehlerausgaben.
 * @returns {Promise<boolean>} Gibt true zurück bei Autorisierung, sonst false.
 */
async function checkIfUserRequestToCoinbaseIsAuthorizedOnSessionByCookiesAndHeaders(cookies = null, headers = null, verbose = false) {
    const url = 'https://accounts.coinbase.com/api/v1/user';
    
    // Header-Objekt vorbereiten
    const requestHeaders = { ...headers };

    // In JavaScript (Node/Browser) müssen Cookies manuell in den 'Cookie'-Header formatiert werden,
    // wenn sie als Objekt übergeben werden.
    if (cookies && Object.keys(cookies).length > 0) {
        const cookieString = Object.entries(cookies)
            .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
            .join('; ');
        requestHeaders['Cookie'] = cookieString;
    }

    let response;
    try {
        response = await fetch(url, {
            method: 'GET',
            headers: requestHeaders
        });

        const json = await response.json();

        if (json && json.message === 'The request is unauthorized.') {
            return false;
        } else {
            return true;
        }
    } catch (e) {
        if (verbose) {
            // Falls der Request fehlschlägt, bevor eine Antwort kommt, existiert response nicht
            console.error({
                error: e.message,
                status_code: response ? response.status : 'N/A',
                text: response ? await response.text().catch(() => 'No text content') : 'N/A'
            });
        }
        return false;
    }
}

// --- Beispiel für die Verwendung ---
//(async () => { const isAuthorized = await checkIfUserRequestToCoinbaseIsAuthorizedOnSessionByCookiesAndHeaders(null, null, true); console.log(isAuthorized); })();
