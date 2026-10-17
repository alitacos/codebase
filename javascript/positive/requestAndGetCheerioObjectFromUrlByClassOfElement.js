// Installieren mit: npm install cheerio
const cheerio = require('cheerio'); // Nutze require statt import

async function requestAndGetCheerioObjectFromUrlByClassOfElement(url = null, element = null, class_ = null) {
    if (!url) return null;

    try {
        const response = await fetch(url);
        if (!response.ok) return null;
        
        const html = await response.text();
        const $ = cheerio.load(html);

        if (!element && !class_) {
            return $; 
        }
        else if (element && !class_) {
            return $(element); 
        }
        else if (class_ && !element) {
            return $; 
        }
        else if (element && class_) {
            try {
                // Gibt die tatsächlich gefilterten Elemente zurück (Bugfix zum Python-Original)
                return $(`${element}.${class_}`); 
            } catch (error) {
                return $(element);
            }
        } else {
            return null;
        }

    } catch (error) {
        return null;
    }
}

// --- Testaufruf ---
// (async () => { const $elements = await requestAndGetCheerioObjectFromUrlByClassOfElement('https://www.google.com', 'title'); if ($elements) { console.log("Gefundener Text:", typeof $elements === 'function' ? $elements('title').text() : $elements.text()); } else { console.log("Fehler beim Abruf."); } })();
