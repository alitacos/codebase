/**
 * XML Sitemap URL Extractor
 * 
 * Downloads a sitemap XML document, recursively traverses sitemap indexes if found,
 * collects all web-page URLs up to allowedSize, removes duplicates, and returns a sorted list.
 * 
 * @param {string} url - The starting URL of the sitemap XML document.
 * @param {number} allowedSize - The maximum number of unique web URLs to collect.
 * @returns {Promise<string[]>} Sorted unique list of web URLs.
 */
async function extract_urls_from_sitemap_index_locs_by_max_filter(url = "", allowedSize = 10000) {
    if (!url || typeof url !== 'string' || !url.trim()) {
        return [];
    }

    // Hilfsfunktion: Prüft, ob eine URL auf eine XML-Sitemap verweist
    const is_xml_sitemap = (targetUrl) => {
        const lowerUrl = targetUrl.toLowerCase();
        return lowerUrl.endsWith(".xml") || lowerUrl.includes("sitemap");
    };

    // Warteschlangen und Sets initialisieren
    const unprocessed_sitemaps = [url.trim()];
    const processed_sitemaps = new Set();
    const collected_urls = new Set();

    const headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    };

    // Schleife läuft, solange Sitemaps in der Warteschlange sind und das Limit nicht erreicht ist
    while (unprocessed_sitemaps.length > 0 && collected_urls.size < allowedSize) {
        const current_sitemap_url = unprocessed_sitemaps.shift();

        // Überspringen, falls wir diese Sitemap schon verarbeitet haben
        if (processed_sitemaps.has(current_sitemap_url)) {
            continue;
        }

        processed_sitemaps.add(current_sitemap_url);
        console.log(`Fetching sitemap: ${current_sitemap_url}`);

        try {
            // Fetch mit einem 15-Sekunden Timeout (analog zu timeout=15)
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 15000);

            const response = await fetch(current_sitemap_url, { headers, signal: controller.signal });
            clearTimeout(timeoutId);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const xmlText = await response.text();

            // 1. Prüfen auf Unter-Sitemaps (<sitemap>...<loc>...</loc>...</sitemap>)
            // Greift gezielt nur <loc> innerhalb von <sitemap>-Blöcken ab (beachtet Namespaces flexibel)
            const sitemapRegex = /<sitemap[^>]*>([\s\S]*?)<\/sitemap>/gi;
            let sitemapMatch;
            while ((sitemapMatch = sitemapRegex.exec(xmlText)) !== null) {
                const sitemapBlock = sitemapMatch[1];
                const locMatch = /<loc[^>]*>([\s\S]*?)<\/loc>/i.exec(sitemapBlock);
                
                if (locMatch && locMatch[1]) {
                    const sub_url = locMatch[1].trim();
                    if (is_xml_sitemap(sub_url) && !processed_sitemaps.has(sub_url)) {
                        unprocessed_sitemaps.push(sub_url);
                    }
                }
            }

            // 2. Prüfen auf echte Web-URLs (<url>...<loc>...</loc>...</url>)
            // Greift gezielt nur <loc> innerhalb von <url>-Blöcken ab
            const urlRegex = /<url[^>]*>([\s\S]*?)<\/url>/gi;
            let urlMatch;
            while ((urlMatch = urlRegex.exec(xmlText)) !== null) {
                const urlBlock = urlMatch[1];
                const locMatch = /<loc[^>]*>([\s\S]*?)<\/ soul><\/loc>/i.exec(urlBlock) || /<loc[^>]*>([\s\S]*?)<\/loc>/i.exec(urlBlock);
                
                if (locMatch && locMatch[1]) {
                    const web_url = locMatch[1].trim();

                    // Nur hinzufügen, wenn es keine XML ist und das Limit nicht gesprengt wird
                    if (!is_xml_sitemap(web_url)) {
                        if (collected_urls.size < allowedSize) {
                            collected_urls.add(web_url);
                        } else {
                            break; // Limit mitten im XML erreicht, Schleife für diese Datei abbrechen
                        }
                    }
                }
            }

        } catch (e) {
            console.log(`Error fetching/parsing ${current_sitemap_url}: ${e.message}`);
        }
    }

    // Gibt die eindeutigen Web-URLs sortiert zurück (Array.from + .sort())
    return Array.from(collected_urls).sort();
}

// === Beispiel für den Aufruf (funktioniert sowohl für Sitemap-Indexe als auch normale XMLs) ===
// (async () => { const urls_list = await extract_urls_from_sitemap_index_locs_by_max_filter("https://huggingface.co/sitemap.xml", 10); console.log(`Gesammelte URLs (${urls_list.length}):`, urls_list); })();
