/**
 * Hilfsfunktion für das Delay (entspricht time.sleep)
 */
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

/**
 * Überprüft, ob ein Username auf ladies.de existiert.
 */
async function checkIfUsernameExistsInLadiesDe({
    username = '',
    retries = 3,
    delay = 2,
    url = "https://login.ladies.de/api/validate/registration?locale=de",
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://login.ladies.de/register",
        "Sec-CH-UA": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "X-XSRF-TOKEN": "eyJpdiI6InZEOHBFQ2N0MzVyNlQvMzhaeGIzWWc9PSIsInZhbHVlIjoiaVZqY092VklPYTBHK2dRVEN3OHVXZnBrQm5wM01ONDBwN3JXM3h5a0VQK0FwK25OWEVWcFlTTWRXWmZyRDdZVWt4UTB5emE4YlVpdHgxbEdjVUlndW8zRytycjJKblU2Z2gwU3dRRlpqMTRlVDVVM3MwNUJaS3k5WmUwK2RwNmIiLCJtYWMiOiJhYjkwZjI3OTY4YzJmZjQyZTMwNDJmMzJkMDc5MjY0OWU5OTg1MmQxMGFlZjM4MTA1YmJlMWE5MTBmM2RlZGQ2IiwidGFnIjoiIn0="
    },
    cookies = {}, // Kann als String im Header 'Cookie' übergeben werden, falls nötig
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

    // Cookie-Header hinzufügen, falls Cookies übergeben wurden
    const finalHeaders = { ...headers };
    if (Object.keys(cookies).length > 0) {
        finalHeaders["Cookie"] = Object.entries(cookies).map(([k, v]) => `${k}=${v}`).join('; ');
    }

    let lastError = null;

    for (let i = 0; i < retries; i++) {
        try {
            // Payload als URLSearchParams (entspricht standard x-www-form-urlencoded in Python requests.post)
            const payload = new URLSearchParams({
                "_token": "ahfwDBub7MZtsvNQhzF8Ai5b9VyMjFizySCcWlCg",
                "my_name_ZabeTCUgoDL6jrvQ": "",
                "valid_from": "eyJpdiI6IlVDL0NvWWNZWXI3N0pJeXJWd1g0ZlE9PSIsInZhbHVlIjoiSGpjaS9lZUZ6YXRDTVJJNUtZbTNQQT09IiwibWFjIjoiOTc2M2Y5MDQxNWIzM2E3ZDI5MjcyZTMzMTJlOGEyMDUxMGZiMzRhZjFjZWJiMTYxY2IyZjliZWM3N2IxZTM4NSIsInRhZyI6IiJ9",
                "name": username.trim(),
                "email": "",
                "password": "",
                "password_confirmation": ""
            });

            // HTTP POST-Anfrage absetzen
            const response = await fetch(url, {
                method: 'POST',
                headers: finalHeaders,
                body: payload,
                redirect: allowRedirects ? 'follow' : 'manual'
            });

            if (response.status === 422) {
                const responseText = await response.text();
                
                // Content-Formatierung analog zur Python-Logik
                let contentText = null;
                if (responseText) {
                    contentText = responseText
                        .replace(/\t/g, '\n')
                        .trim()
                        .split('\n')
                        .map(line => line.trim())
                        .filter(line => line !== '')
                        .join('\n');
                }

                // JSON parsen für die Fehlerprüfung
                let info = {};
                try { info = JSON.parse(responseText); } catch (e) { }

                const errors = info.errors || {};
                const nameErrors = errors.name || [];
                const message = info.message || '';

                const targetString = 'Dieser Name ist bereits vergeben.';
                const isTaken = nameErrors.includes(targetString) || message.includes(targetString);

                if (isTaken) {
                    return {
                        error: false,
                        status: 422,
                        username: username,
                        content: contentText,
                        title: null,
                        available: false,
                        exists: true
                    };
                }

                return {
                    error: false,
                    status: 422,
                    username: username,
                    content: contentText,
                    title: null,
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

// --- Ausführungsbeispiel ---
// async function main() { console.log("--- Test 1: anonymous ---"); const res1 = await checkIfUsernameExistsInLadiesDe({ username: 'anonymous' }); console.log(res1); console.log("\n--- Test 2: alitakos90papatoliosalex ---"); const res2 = await checkIfUsernameExistsInLadiesDe({ username: 'alitakos90papatoliosalex' }); console.log(res2); } main();