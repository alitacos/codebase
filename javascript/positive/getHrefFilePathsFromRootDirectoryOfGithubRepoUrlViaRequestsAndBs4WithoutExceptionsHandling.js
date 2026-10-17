async function getHrefFilePathsFromRootDirectoryOfGithubRepoUrlViaRequestsAndBs4WithoutExceptionsHandling(url = '') {
    const cheerio = require("cheerio");

    async function getRootPaths(url) {
        const response = await fetch(url);
        const html = await response.text();

        const $ = cheerio.load(html);

        return $("div.application-main td.react-directory-row-name-cell-small-screen")
            .map((_, i) => $(i).find("a.Link--primary").attr("href"))
            .get()
            .filter(i => i);
    }

    const rootPaths = await getRootPaths(url);

    return [...new Set(rootPaths.filter(i => i && i.includes('/tree/')))].sort();
}


// example usage:
(async()=>{console.log(await getHrefFilePathsFromRootDirectoryOfGithubRepoUrlViaRequestsAndBs4WithoutExceptionsHandling('https://github.com/google-research/google-research'));})();