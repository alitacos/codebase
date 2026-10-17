#negative
async function getTotalGithubRepositoriesByTopicAndLanguageIdViaApi(topic = '', lang = '*') {
    const query = `
    query {
      search(
        query: "topic:${topic} ${lang !== '*' ? `language:${lang}` : ''}",
        type: REPOSITORY,
        first: 1
      ) {
        repositoryCount
      }
    }`;

    const response = await fetch("https://api.github.com/graphql", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer YOUR_GITHUB_TOKEN"
        },
        body: JSON.stringify({ query })
    });

    const json = await response.json();

    return json?.data?.search?.repositoryCount ?? null;
}
//(async () => { const total = await getTotalGithubRepositoriesByTopicAndLanguageIdViaApi( "machine-learning", "python" ); console.log(total); })();
