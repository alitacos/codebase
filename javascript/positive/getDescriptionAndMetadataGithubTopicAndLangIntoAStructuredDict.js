async function getDescriptionAndMetadataGithubTopicAndLangIntoAStructuredDict(topicUiid = null, lang = null, retries = 3, delay = 2, ...args) {
    const headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/91.0.4472.124 Safari/537.36"
    };

    const options = {
        headers:headers,
        ...args
    };

    const url = lang
        ? `https://github.com/topics/${topicUiid}?l=${lang.trim()}`
        : `https://github.com/topics/${topicUiid}`;

    let error = null;
    let statusCode = null;
    let totalPages = null;
    let totalRepos = null;

    for (let attempt = 0; attempt < retries; attempt++) {
        try {
            const response = await fetch(url, options);

            statusCode = response.status;

            if (response.status === 200) {
                const html = await response.text();

                const reposMatch = html.match(/([\d,]+)\s+matching this topic/);

                totalRepos = reposMatch
                    ? parseInt(reposMatch[1].replace(/,/g, ''))
                    : 0;

                totalPages = totalRepos > 0 ? Math.ceil(totalRepos / 20) : 0;

                return {
                    error:error,
                    status:response.status,
                    topic:topicUiid,
                    total_pages:totalPages,
                    total_repositories:totalRepos,
                    programming_language:lang ? lang : 'all'
                };
            }

        } catch (e) {
            error = String(e);
        }

        if (attempt < retries - 1) {
            await new Promise(resolve => setTimeout(resolve, delay * 1000));
        }
    }

    return {
        error:error,
        status:statusCode,
        topic:topicUiid,
        total_pages:totalPages,
        total_repositories:totalRepos,
        programming_language:lang ? lang : 'all'
    };
}


// example usage:
//(async()=>{console.log(await getDescriptionAndMetadataGithubTopicAndLangIntoAStructuredDict('google'));})();