/**
 * Fetch a Google DevSite or Codelab page via HTTP and extract the main content container element.
 * 
 * @param {string} url - URL of the DevSite or Codelab page to fetch and parse.
 * @param {boolean} get_text - If True, returns only the text content of the extracted element. If False, returns the raw HTML string.
 * @param {boolean} strip - If True, strips whitespace when extracting text.
 * @param {object} kwargs - Optional arguments passed directly to fetch (e.g. headers, method).
 * @returns {Promise<string>} Extracted content from the page (HTML string or flat plain text).
 */
async function get_devsite_content_or_codelab_element_in_google_article_over_url_via_requests_and_bs4(url = '', get_text = false, strip = true, kwargs = {}) {
    if (!url || typeof url !== 'string' || !url.trim()) {
        return '';
    }

    // Standard Browser-Header, um Blockaden durch Google zu vermeiden
    const defaultHeaders = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    };

    try {
        const response = await fetch(url.trim(), {
            method: 'GET',
            ...kwargs,
            headers: {
                ...defaultHeaders,
                ...(kwargs.headers || {})
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const html = await response.text();

        // 1. Suche nach <devsite-content>...</devsite-content>
        // 2. Falls nicht vorhanden, Suche nach <google-codelab>...</google-codelab>
        let contentMatch = html.match(/<devsite-content[^>]*>([\s\S]*?)<\/devsite-content>/i);
        if (!contentMatch) {
            contentMatch = html.match(/<google-codelab[^>]*>([\s\S]*?)<\/google-codelab>/i);
        }

        if (!contentMatch) {
            return '';
        }

        // Das gesamte gematchte Element (inklusive umschließender Tags)
        const fullElementStr = contentMatch[0];

        if (get_text) {
            let innerHtml = contentMatch[1];

            // Entferne Scripte, Styles, Noscripts und SVGs samt Inhalt, um den Text sauber zu halten
            innerHtml = innerHtml.replace(/<(script|style|noscript|svg)[^>]*>[\s\S]*?<\/\1>/gi, '');
            
            // Entferne alle HTML-Tags
            innerHtml = innerHtml.replace(/<[^>]+>/g, ' ');
            
            // HTML-Entities dekodieren
            innerHtml = innerHtml.replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>');

            if (strip) {
                // Whitespaces zu einem flachen Fließtext bereinigen (verhindert tokenisierte '+'-Anzeigen in Node)
                return innerHtml.replace(/[\t\r\n]+/g, ' ').split(' ').map(w => w.trim()).filter(w => w.length > 0).join(' ');
            }
            return innerHtml;
        } else {
            // Gibt den rohen HTML-String des Elements zurück (analog zu str(content_el).strip())
            return fullElementStr.trim();
        }

    } catch (e) {
        // Fehler abfangen und analg zur Python-Logik einen leeren String zurückgeben
        return '';
    }
}

// Beispiel-Aufrufe (entspricht deinem Testlauf)
// (async () => { const targetUrl = 'https://developer.chrome.com/docs/ai/built-in-apis'; console.log("--- TEST 1: RAW HTML ---"); const rawHtml = await get_devsite_content_or_codelab_element_in_google_article_over_url_via_requests_and_bs4(targetUrl, false); console.log(rawHtml.substring(0, 300) + "..."); console.log("\n--- TEST 2: CLEAN TEXT ---"); const cleanText = await get_devsite_content_or_codelab_element_in_google_article_over_url_via_requests_and_bs4(targetUrl, true); console.log(cleanText.substring(0, 300) + "..."); })();
