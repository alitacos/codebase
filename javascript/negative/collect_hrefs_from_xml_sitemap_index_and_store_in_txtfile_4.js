async function collect_hrefs_from_xml_sitemap_index_and_store_in_txtfile(
    index_url = '',
    unprocessed_file = '',
    destination = 'processed.txt'
) {
    const fs = require("fs/promises");
    const path = require("path");

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
        url = url.toLowerCase();

        return url.endsWith(".xml") || url.includes("sitemap");
    }


    function decode_xml(value) {
        return value
            .replace(/&amp;/g, "&")
            .replace(/&lt;/g, "<")
            .replace(/&gt;/g, ">")
            .replace(/&quot;/g, '"')
            .replace(/&#39;/g, "'");
    }


    async function collect_hrefs_from_xml_sitemap(
        index_url,
        unprocessed_file,
        processed_file
    ) {

        await ensure_file(unprocessed_file);
        await ensure_file(processed_file);


        if (
            !(await is_link_in_file(processed_file, index_url)) &&
            !(await is_link_in_file(unprocessed_file, index_url))
        ) {
            await fs.appendFile(
                unprocessed_file,
                index_url + "\n",
                "utf8"
            );
        }


        while (true) {

            const current_sitemap =
                await get_next_sitemap(unprocessed_file);


            if (!current_sitemap) {

                console.log(
                    "\nAlle Sitemaps erfolgreich verarbeitet!"
                );

                break;
            }


            console.log(
                `\nÖffne Sitemap: ${current_sitemap}`
            );


            try {

                const controller = new AbortController();

                const timeout = setTimeout(
                    () => controller.abort(),
                    15000
                );


                const response = await fetch(
                    current_sitemap,
                    {
                        signal: controller.signal
                    }
                );


                clearTimeout(timeout);


                if (!response.ok) {
                    throw new Error(
                        `HTTP ${response.status}`
                    );
                }


                const xml = await response.text();


                const locs = [
                    ...xml.matchAll(
                        /<loc(?:\s[^>]*)?>([\s\S]*?)<\/loc>/gi
                    )
                ];


                for (const match of locs) {

                    const link = decode_xml(
                        match[1].trim()
                    );


                    let parsed_url;

                    try {

                        parsed_url = new URL(link);

                    } catch {

                        continue;

                    }


                    if (
                        !(
                            parsed_url.protocol === "http:" ||
                            parsed_url.protocol === "https:"
                        )
                    ) {
                        continue;
                    }


                    if (!parsed_url.hostname) {
                        continue;
                    }


                    if (is_xml_sitemap(link)) {


                        if (
                            !(await is_link_in_file(
                                unprocessed_file,
                                link
                            )) &&
                            !(await is_link_in_file(
                                processed_file,
                                link
                            ))
                        ) {

                            await fs.appendFile(
                                unprocessed_file,
                                link + "\n",
                                "utf8"
                            );


                            console.log(
                                ` -> Sub-Sitemap gemerkt: ${link}`
                            );
                        }


                    } else {


                        if (
                            !(await is_link_in_file(
                                processed_file,
                                link
                            ))
                        ) {

                            await fs.appendFile(
                                processed_file,
                                link + "\n",
                                "utf8"
                            );


                            console.log(
                                ` -> Web-URL direkt gespeichert: ${link}`
                            );
                        }
                    }
                }


                if (
                    !(await is_link_in_file(
                        processed_file,
                        current_sitemap
                    ))
                ) {

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