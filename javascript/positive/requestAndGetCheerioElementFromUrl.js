// Falls in Node.js genutzt, installiere cheerio zuerst via: npm install cheerio
//import * as cheerio from 'cheerio';
const cheerio = require('cheerio'); // Nutze require um den SyntaxError zu vermeiden

/**
 * Ruft eine Webseite ab und parst sie mit cheerio (ähnlich zu BeautifulSoup).
 * Filtert optional nach HTML-Tag und CSS-Klasse.
 *
 * @param {string} url - Die Ziel-URL.
 * @param {string|null} element - HTML-Tag Name (z.B. "div", "span").
 * @param {string|null} class_ - CSS-Klassenname zum Filtern.
 * @returns {Promise<Object|null>} Cheerio-Instanz, gefilterte Elemente oder null.
 */
async function requestAndGetCheerioElementFromUrl(url = null, element = null, class_ = null) {
    if (!url) return null;

    try {
        // 1. HTML-Inhalt via fetch abrufen
        const response = await fetch(url);
        if (!response.ok) return null;
        
        const html = await response.text();

        // 2. HTML parsen (Cheerio initialisieren -> entspricht BeautifulSoup(html, 'html.parser'))
        const $ = cheerio.load(html);

        // --- Logik-Pfade analog zum Python-Original ---
        
        // Fall 1: Weder Element noch Klasse angegeben -> Ganze "Soup" zurückgeben
        if (!element && !class_) {
            return $; 
        }
        // Fall 2: Nur Element angegeben -> Alle passenden Tags finden
        else if (element && !class_) {
            return $(element); 
        }
        // Fall 3: Nur Klasse angegeben -> Gibt im Original das *ganze* soup-Objekt zurück
        else if (class_ && !element) {
            return $; 
        }
        // Fall 4: Sowohl Element als auch Klasse angegeben
        else if (element && class_) {
            try {
                // Sucht nach 'tag.klasse' (z.B. 'div.container')
                // HINWEIS: Das Python-Original führt die Suche aus, gibt danach aber 'soup' (alles) zurück.
                $(`${element}.${class_}`); 
                return $; 
            } catch (error) {
                // Fallback bei Fehlern: Nur nach Element filtern
                return $(element);
            }
        } else {
            return null;
        }

    } catch (error) {
        // Fängt Netzwerkfehler oder Parse-Fehler ab
        return null;
    }
}

// --- Testaufruf ---
// (async () => { const $soup = await requestAndGetCheerioElementFromUrl('https://www.google.com'); if ($soup) { // Ausgabe des Seitentitels zum Testen (äquivalent zu soup.title.text) console.log("Gefundener Titel:", $soup('title').text()); } else { console.log("Fehler beim Abruf."); } })();