const cheerio = require('cheerio'); // Nutze require um den SyntaxError zu vermeiden

/**
 * Ruft eine Webseite ab und parst sie mit cheerio (äquivalent zu BeautifulSoup).
 *
 * @param {string} url - Die Ziel-URL.
 * @param {string|null} element - HTML-Tag Name (z.B. "div", "span").
 * @param {string|null} class_ - CSS-Klassenname zum Filtern.
 * @returns {Promise<Object|null>} Die gesamte "Soup" (Cheerio-Instanz) oder null.
 */
async function getCheerioObjectFromUrlByClassOfElement(url = null, element = null, class_ = null) {
    if (!url) return null;

    try {
        // 1. HTML-Inhalt via fetch abrufen
        const response = await fetch(url);
        if (!response.ok) return null;
        
        const html = await response.text();

        // 2. HTML parsen (Cheerio initialisieren -> entspricht BeautifulSoup(html, 'html.parser'))
        const $ = cheerio.load(html);

        // --- Logik-Pfade analog zum Python-Original ---
        
        // Fall 1: Weder Element noch Klasse angegeben -> Ganze Soup zurückgeben
        if (!element && !class_) {
            return $; 
        }
        // Fall 2: Nur Element angegeben -> Gibt das ganze Objekt zurück
        else if (element && !class_) {
            return $; 
        }
        // Fall 3: Nur Klasse angegeben -> Gibt das ganze Objekt zurück
        else if (class_ && !element) {
            return $; 
        }
        // Fall 4: Sowohl Element als auch Klasse angegeben
        else if (element && class_) {
            try {
                // Prüft, ob das Element mit der Klasse existiert (wie im Python-Original)
                const exists = $(`${element}.${class_}`).length > 0;
                return $; // Gibt das volle Soup-Objekt zurück
            } catch (error) {
                // Fallback bei Fehlern
                return $;
            }
        } else {
            return null;
        }

    } catch (error) {
        // Fängt Netzwerkfehler oder Parse-Fehler ab
        return null;
    }
}
//(async () => { return await getCheerioObjectFromUrlByClassOfElement( 'https://google.com', 'div', 'container' ); })();
