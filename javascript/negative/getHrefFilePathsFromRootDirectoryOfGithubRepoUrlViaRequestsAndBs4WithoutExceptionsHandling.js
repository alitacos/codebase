async function getHrefFilePathsFromRootDirectoryOfGithubRepoUrlViaRequestsAndBs4WithoutExceptionsHandling(url = '') {
    async function getRootPaths(url) {
        const response = await fetch(url);
        const html = await response.text();

        const parser = new DOMParser();
        const doc = parser.parseFromString(html, "text/html");

        return [...doc.querySelectorAll("div.application-main td.react-directory-row-name-cell-small-screen")]
            .map(i => i.querySelector("a.Link--primary")?.getAttribute("href"))
            .filter(i => i);
    }

    const rootPaths = await getRootPaths(url);

    return [...new Set(rootPaths.filter(i => i && i.includes('/tree/')))]
        .sort();
}


// example usage:
// (async()=>{console.log(await getHrefFilePathsFromRootDirectoryOfGithubRepoUrlViaRequestsAndBs4WithoutExceptionsHandling('https://github.com/google-research/google-research'));})();