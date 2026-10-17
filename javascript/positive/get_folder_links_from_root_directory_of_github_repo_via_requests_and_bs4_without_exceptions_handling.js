async function get_folder_links_from_root_directory_of_github_repo_via_requests_and_bs4_without_exceptions_handling(repo = "") {
    const url = `https://github.com/${repo.trim().replace(/^\/|\/$/g, "")}`;

    const response = await fetch(url);

    const html = await response.text();

    const $ = cheerio.load(html);

    const root_paths = [];

    $("td.react-directory-row-name-cell-small-screen a.Link--primary").each((_, el) => {
        const href = $(el).attr("href");
        if (href) root_paths.push(href);
    });

    return [...new Set(root_paths)]
        .filter(i => i && i.includes("/tree/"))
        .sort()
        .map(i => `https://github.com/${i.replace(/^\/|\/$/g, "")}`);
}


//get_folder_links_from_root_directory_of_github_repo_via_requests_and_bs4_without_exceptions_handling("selenium/selenium").then(console.log);