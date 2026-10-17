async function get_article_urls_over_infosecwriteups_sitemap(xml_url = "https://infosecwriteups.com/sitemap/sitemap.xml") {
    const headers = {
        "User-Agent": "Mozilla/5.0"
    };

    const response = await fetch(xml_url, { headers });

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    const xml = await response.text();

    const locs = [...xml.matchAll(/<loc>(.*?)<\/loc>/g)].map(i => i[1].trim());

    let urls = [];

    for (const url of locs) {
        if (url.includes("/tagged/")) continue;

        if (url.endsWith(".xml")) {
            urls.push(...await get_article_urls_over_infosecwriteups_sitemap(url));
        } else {
            urls.push(url);
        }
    }

    return [...new Set(urls)].sort();
}

//(async () => { console.log(await get_article_urls_over_infosecwriteups_sitemap("https://infosecwriteups.com/sitemap/sitemap.xml")); })();