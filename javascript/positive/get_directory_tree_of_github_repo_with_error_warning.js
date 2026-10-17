async function get_directory_tree_of_github_repo_with_error_warning(repo = "") {
    const folders = new Set();
    const files = new Set();
    const unprocessed_folders = new Set();

    async function get_html(url) {
        try {
            const r = await fetch(url, {
                headers: {
                    "User-Agent": "Mozilla/5.0"
                }
            });

            if (!r.ok) return null;

            return await r.text();
        } catch (e) {
            return null;
        }
    }

    function extract_links(html, repo_full_name) {
        if (!html || !repo_full_name) return false;

        const found_hrefs = new Set();

        try {
            const matches = [...html.matchAll(/href="([^"]+)"/g)];

            for (const match of matches) {
                const href = match[1];

                if (
                    href.startsWith(`/${repo_full_name}/tree/`) ||
                    href.startsWith(`/${repo_full_name}/blob/`)
                ) {
                    found_hrefs.add(href);
                }
            }
        } catch (e) {
            return false;
        }

        if (!found_hrefs.size) return false;

        for (const href of found_hrefs) {
            const full_link = `https://github.com${href}`;

            if (href.includes("/tree/")) {
                if (!folders.has(full_link) && !unprocessed_folders.has(full_link)) {
                    unprocessed_folders.add(full_link);
                }
            }

            if (href.includes("/blob/")) {
                files.add(full_link);
            }
        }

        return true;
    }

    const base_repo_url = `https://github.com/${repo}`;

    const initial_html = await get_html(base_repo_url);

    if (!extract_links(initial_html, repo)) {
        return {
            error: true,
            folders: folders,
            files: files
        };
    }

    folders.add(base_repo_url);

    while (unprocessed_folders.size) {
        const current_url = [...unprocessed_folders][0];
        unprocessed_folders.delete(current_url);

        folders.add(current_url);

        const current_html = await get_html(current_url);

        if (!extract_links(current_html, repo)) {
            return {
                error: true,
                folders: folders,
                files: files
            };
        }
    }

    return {
        error: false,
        folders: folders,
        files: files
    };
}


// call
// (async () => { console.log(await get_directory_tree_of_github_repo_with_error_warning("asgeirtj/system_prompts_leaks")); })();