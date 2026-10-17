async function fetch_wonderhowto_links_from_default_sitemap_links(output_path = "", sitemaps = []) {
    const xmls = [...new Set(sitemaps)].sort();

    const startlinks = new Set();

    async function get_sitemap_links(sitemap_url) {
        try {
            const r = await fetch(sitemap_url, {
                headers: {
                    "User-Agent": "Mozilla/5.0"
                }
            });

            if (!r.ok) {
                throw new Error(`HTTP ${r.status}`);
            }

            const xml = await r.text();

            return [...xml.matchAll(/<loc>(.*?)<\/loc>/g)]
                .map(i => i[1].trim());

        } catch (e) {
            console.log(`Error fetching sitemap: ${e.message}`);
            return [];
        }
    }

    for (const xml_url of xmls) {
        if (!xml_url) {
            console.log("Please provide a sitemap URL.");
            continue;
        }

        const all_links = await get_sitemap_links(xml_url);

        all_links.forEach(i => startlinks.add(i));

        if (all_links.length) {
            console.log(`found ${all_links.length} for ${xml_url}`);
        } else {
            console.log("No links found or an error occurred.");
        }
    }

    const result = [...startlinks].sort();

    if (output_path && result.length) {
        const fs = require("fs");
        const path = require("path");

        const directory = path.dirname(output_path);

        if (directory && directory !== ".") {
            fs.mkdirSync(directory, { recursive: true });
        }

        fs.writeFileSync(output_path, result.join("\n"), "utf8");

        console.log(`data successfully stored in ${output_path}`);
    }

    return result;
}


// call
// (async () => { console.log(await fetch_wonderhowto_links_from_default_sitemap_links("", ["https://www.wonderhowto.com/sitemap.xml"])); })();