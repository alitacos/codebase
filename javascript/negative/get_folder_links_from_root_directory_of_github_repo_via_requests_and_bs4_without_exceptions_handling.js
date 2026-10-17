async function get_folder_links_from_root_directory_of_github_repo_via_requests_and_bs4_without_exceptions_handling(repo = "") {
    function get_root_paths(html) {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, "text/html");

        return [...doc.querySelectorAll("td.react-directory-row-name-cell-small-screen a.Link--primary")]
            .map(i => i.getAttribute("href"));
    }

    const url = `https://github.com/${repo.trim().replace(/^\/|\/$/g, "")}`;

    const response = await fetch(url);

    const html = await response.text();

    const root_paths = get_root_paths(html);

    return [...new Set(root_paths)]
        .filter(i => i && i.includes("/tree/"))
        .sort()
        .map(i => `https://github.com/${i.replace(/^\/|\/$/g, "")}`);
}


//get_folder_links_from_root_directory_of_github_repo_via_requests_and_bs4_without_exceptions_handling("selenium/selenium").then(console.log);
