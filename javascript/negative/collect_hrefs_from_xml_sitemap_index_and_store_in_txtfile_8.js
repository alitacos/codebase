async function collect_hrefs_from_xml_sitemap_index_and_store_in_txtfile(index_url = '', unprocessed_file = '', destination = 'processed.txt') {
    /*
      XML Sitemap Index Collector
    
        Recursively processes an XML sitemap index, discovers nested sitemap files and webpage URLs,
        stores pending sitemap URLs in an unprocessed queue file, and writes processed sitemap URLs
        and discovered webpage URLs into the destination text file while avoiding duplicates through streamed XML parsing.
    */

    const fs = require("fs/promises");
    const path = require("path");
    const { XMLParser } = require("fast-xml-parser");

    async function ensure_file(file_path) {
        const directory = path.dirname(path.resolve(file_path));
        await fs.mkdir(directory, { recursive: true });

        try {
            await fs.access(file_path);
        } catch {
            await fs.writeFile(file_path, "", "utf8");
        }
    }

    async function is_link_in_file(file_path, target_link) {
        if (!file_path) {
            return false;
        }

        try {
            const content = await fs.readFile(file_path, "utf8");

            for (const line of content.split("\n")) {
                if (line.trim() === target_link) {
                    return true;
                }
            }
        } catch {
            return false;
        }

        return false;
    }

    async function remove_link_from_unprocessed(file_path, link_to_remove) {
        const temp_path = file_path + ".tmp";

        const content = await fs.readFile(file_path, "utf8");

        const filtered = content
            .split("\n")
            .filter(line => line.trim() !== link_to_remove)
            .join("\n");

        await fs.writeFile(temp_path, filtered, "utf8");
        await fs.rename(temp_path, file_path);
    }

    async function get_next_sitemap(file_path) {
        try {
            const content = await fs.readFile(file_path, "utf8");

            for (const line of content.split("\n")) {
                const cleaned = line.trim();

                if (cleaned) {
                    return cleaned;
                }
            }
        } catch {
            return null;
        }

        return null;
    }

    function is_xml_sitemap(url) {
        return url.toLowerCase().endsWith(".xml") || url.toLowerCase().includes("sitemap");
    }

    async function collect_hrefs_from_xml_sitemap(index_url, unprocessed_file, processed_file) {

        ensure_file(unprocessed_file);
        ensure_file(processed_file);

        if (
            !await is_link_in_file(processed_file, index_url) &&
            !await is_link_in_file(unprocessed_file, index_url)
        ) {
            await fs.appendFile(unprocessed_file, index_url + "\n", "utf8");
        }

        while (true) {

            const current_sitemap = await get_next_sitemap(unprocessed_file);

            if (!current_sitemap) {
                console.log("\nAlle Sitemaps erfolgreich verarbeitet!");
                break;
            }

            console.log(`\nÖffne Sitemap: ${current_sitemap}`);

            try {

                const response = await fetch(current_sitemap);

                if (!response.ok) {
                    throw new Error(`HTTP ${response.status} ${response.statusText}`);
                }

                const xml = await response.text();

                const parser = new XMLParser({
                    ignoreAttributes: false
                });

                const parsed = parser.parse(xml);

                let locations = [];

                function extract_locations(obj) {

                    if (!obj || typeof obj !== "object") {
                        return;
                    }

                    for (const key of Object.keys(obj)) {

                        if (key === "loc") {

                            if (Array.isArray(obj[key])) {
                                locations.push(...obj[key]);
                            } else {
                                locations.push(obj[key]);
                            }

                        } else if (typeof obj[key] === "object") {
                            extract_locations(obj[key]);
                        }
                    }
                }

                extract_locations(parsed);

                for (const item of locations) {

                    const link = String(item).trim();

                    let parsed_url;

                    try {
                        parsed_url = new URL(link);
                    } catch {
                        continue;
                    }

                    if (
                        ["http:", "https:"].includes(parsed_url.protocol) &&
                        parsed_url.hostname
                    ) {

                        if (is_xml_sitemap(link)) {

                            if (
                                !await is_link_in_file(unprocessed_file, link) &&
                                !await is_link_in_file(processed_file, link)
                            ) {

                                await fs.appendFile(
                                    unprocessed_file,
                                    link + "\n",
                                    "utf8"
                                );

                                console.log(` -> Sub-Sitemap gemerkt: ${link}`);
                            }

                        } else {

                            if (!await is_link_in_file(processed_file, link)) {

                                await fs.appendFile(
                                    processed_file,
                                    link + "\n",
                                    "utf8"
                                );

                                console.log(` -> Web-URL direkt gespeichert: ${link}`);
                            }
                        }
                    }
                }

                if (!await is_link_in_file(processed_file, current_sitemap)) {

                    await fs.appendFile(
                        processed_file,
                        current_sitemap + "\n",
                        "utf8"
                    );
                }

                await remove_link_from_unprocessed(
                    unprocessed_file,
                    current_sitemap
                );

            } catch (e) {

                console.log(
                    `Fehler bei Sitemap ${current_sitemap}: ${e}`
                );

                await fs.appendFile(
                    processed_file,
                    `${current_sitemap} (FAILED: ${e})\n`,
                    "utf8"
                );

                await remove_link_from_unprocessed(
                    unprocessed_file,
                    current_sitemap
                );
            }
        }
    }

    return await collect_hrefs_from_xml_sitemap(
        index_url,
        unprocessed_file,
        destination
    );
}