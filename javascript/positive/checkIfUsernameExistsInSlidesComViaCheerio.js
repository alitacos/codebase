const cheerio = require('cheerio');

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function checkIfUsernameExistsInSlidesComViaCheerio(options = {}) {
    const {
        username = '',
        retries = 3,
        delay = 2,
        url = 'https://slides.com',
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9, image/avif,image/webp,*/*;q=0.8"
        },
        redirect = 'manual'
    } = options;

    if (!username || typeof username !== 'string' || !username.trim()) {
        return { error: 'invalid <username> value', status: null, username, content: null, title: null, available: false, exists: false };
    }

    const cleanUrl = url.trim().replace(/\/+$/, '');
    const cleanUsername = username.trim().replace(/^\/+|\/+$/g, '');
    const targetUrl = `${cleanUrl}/${cleanUsername}`;
    let lastError = null;

    for (let i = 0; i < retries; i++) {
        try {
            const response = await fetch(targetUrl, { method: 'GET', headers, redirect });
            const html = await response.text();
            const $ = cheerio.load(html);

            // ÄNDERUNG: Nutzt jetzt Leerzeichen statt Zeilenumbrüche beim Zusammenfügen
            const getCleanText = (element) => {
                return element.text().replace(/[\t\r\n]+/g, ' ').split(' ').map(line => line.trim()).filter(line => line.length > 0).join(' ');
            };

            if (response.status === 200) {
                const titleText = $('title').text().trim() || null;

                $('html').find('script, style, noscript, svg').remove();

                let bodyText = getCleanText($('body')) || '';

                let finalContent = bodyText;
                if (titleText && !bodyText.startsWith(titleText)) {
                    finalContent = `${titleText} ${bodyText}`;
                }

                return { 
                    error: false, 
                    status: 200, 
                    username, 
                    content: finalContent || null, 
                    title: titleText, 
                    available: false, 
                    exists: true 
                };
            }

            if (response.status === 404) {
                const errorHeader = $('.errors-header');
                return { error: false, status: 404, username, content: errorHeader.length ? getCleanText(errorHeader) : null, title: $('title').text().trim() || null, available: true, exists: false };
            }

            lastError = `unexpected status_code ${response.status}`;
            await sleep(delay * 1000);
        } catch (error) {
            lastError = error.message;
            await sleep(delay * 1000);
        }
    }
    return { error: lastError, status: null, username, content: null, title: null, available: null, exists: null };
}

// Example usage :
// (async () => { const result1 = await checkIfUsernameExistsInSlidesComViaCheerio({ username: 'papatolios' }); console.log(result1); const result2 = await checkIfUsernameExistsInSlidesComViaCheerio({ username: 'anon' }); console.log(result2); })();

// retest, not sure if negative or positive. content if 404 is missing