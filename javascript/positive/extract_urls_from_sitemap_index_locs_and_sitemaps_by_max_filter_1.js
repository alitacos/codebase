/**
 * XML Sitemap Index And URL Extractor
 * 
 * Downloads and parses a sitemap XML document, recursively traverses sitemap indexes, 
 * collects discovered sitemap URLs, extracts webpage URLs from standard sitemaps, 
 * and stops collecting webpage URLs once the specified maximum limit is reached.
 * 
 * @param {string} url - URL of the sitemap XML file to process.
 * @param {number} allowedSize - Maximum number of webpage URLs to collect before stopping.
 * @returns {Promise<{sitemaps: string[], web_urls: string[]}>} Structured object containing sorted sitemaps and web URLs.
 */
async function extract_urls_from_sitemap_index_locs_and_sitemaps_by_max_filter(url = "", allowedSize = 10000) {
    if (!url || typeof url !== 'string' || !url.trim()) {
        return { sitemaps: [], web_urls: [] };
    }

    // Hilfsfunktion: Prüft, ob eine URL auf eine XML-Sitemap verweist
    const is_xml_sitemap = (targetUrl) => {
        const lowerUrl = targetUrl.toLowerCase();
        return lowerUrl.endsWith(".xml") || lowerUrl.includes("sitemap");
    };

    // Warteschlangen und Sets initialisieren
    const unprocessed_sitemaps = [url.trim()];
    const processed_sitemaps = new Set();
    const collected_web_urls = new Set();

    const headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    };

    // Schleife läuft, solange Sitemaps in der Queue sind und das Limit nicht erreicht ist
    while (unprocessed_sitemaps.length > 0 && collected_web_urls.size < allowedSize) {
        const current_sitemap_url = unprocessed_sitemaps.shift();

        if (processed_sitemaps.has(current_sitemap_url)) {
            continue;
        }

        processed_sitemaps.add(current_sitemap_url);
        console.log(`Fetching sitemap: ${current_sitemap_url}`);

        try {
            // Fetch mit einem 15-Sekunden-Timeout einrichten
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 15000);

            const response = await fetch(current_sitemap_url, { headers, signal: controller.signal });
            clearTimeout(timeoutId);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const xmlText = await response.text();

            // 1. Unter-Sitemaps extrahieren (Sitemap-Index Struktur: <sitemap><loc>...</loc></sitemap>)
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

            // 2. Echte Web-URLs extrahieren (Standard-Sitemap Struktur: <url><loc>...</loc></url>)
            const urlRegex = /<url[^>]*>([\s\S]*?)<\/url>/gi;
            let urlMatch;
            while ((urlMatch = urlRegex.exec(xmlText)) !== null) {
                const urlBlock = urlMatch[1];
                const locMatch = /<loc[^>]*>([\s\S]*?)<\/loc>/i.exec(urlBlock);
                
                if (locMatch && locMatch[1]) {
                    const web_url = locMatch[1].trim();

                    // Falls Sitemaps in <url>-Tags versteckt sind (Hugging-Face Sonderfall)
                    if (is_xml_sitemap(web_url)) {
                        if (!processed_sitemaps.has(web_url) && !unprocessed_sitemaps.includes(web_url)) {
                            unprocessed_sitemaps.push(web_url);
                        }
                    } else {
                        // Strikte Prüfung gegen das definierte Limit (.size des Sets)
                        if (collected_web_urls.size < allowedSize) {
                            collected_web_urls.add(web_url);
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

    // Rückgabe beider Welten sauber sortiert als flache Arrays verpackt in einem Objekt
    return {
        sitemaps: Array.from(processed_sitemaps).sort(),
        web_urls: Array.from(collected_web_urls).sort()
    };
}

// === Beispiel für den Aufruf ===
// (async () => { const result = await extract_urls_from_sitemap_index_locs_and_sitemaps_by_max_filter("https://huggingface.co/sitemap.xml", 10); console.log(`Gefundene Sitemaps (${result.sitemaps.length}):`, result.sitemaps); console.log(`Gesammelte Web-URLs (${result.web_urls.length}):`, result.web_urls); })();