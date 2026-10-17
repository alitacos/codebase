async function getTotalGithubRepositoriesByTopicAndLanguageIdViaApi(
    topic = '',
    lang = '*',
    githubToken = ''
) {
    if (!githubToken) {
        throw new Error("GitHub token is required");
    }

    const searchQuery = `topic:${topic} ${
        lang !== '*' ? `language:${lang}` : ''
    }`;

    const query = `
    query($query:String!) {
        search(
            query:$query,
            type:REPOSITORY,
            first:1
        ) {
            repositoryCount
        }
    }`;

    const response = await fetch("https://api.github.com/graphql", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${githubToken}`
        },
        body: JSON.stringify({
            query,
            variables: {
                query: searchQuery
            }
        })
    });

    const json = await response.json();

    if (json.errors) {
        throw new Error(JSON.stringify(json.errors));
    }

    return json.data.search.repositoryCount;
}


// Example:
//(async () => { const total = await getTotalGithubRepositoriesByTopicAndLanguageIdViaApi( "machine-learning", "python", "ghp_your_real_token_here" ); console.log(total); })();