async function getTotalGithubRepositoriesByTopicAndLanguageId(topic = '', lang = '*') {
    /*
        Retrieves the total number of GitHub repositories for a given topic
        and optional programming language filter.

        Args:
            topic (string): GitHub topic name (example: "machine-learning", "python")
            lang (string): Programming language filter ("python", "javascript", "*" or "all")

        Returns:
            number | null: Total repository count, or null if an error occurs.
    */

    try {
        const cleanTopic = topic.trim().toLowerCase();
        const cleanLang = lang.trim().toLowerCase();

        let url;

        if (cleanLang && !['*', 'all'].includes(cleanLang)) {
            url = `https://github.com/topics/${encodeURIComponent(cleanTopic)}?l=${encodeURIComponent(cleanLang)}`;
        } else {
            url = `https://github.com/topics/${encodeURIComponent(cleanTopic)}`;
        }

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }

        const html = await response.text();

        // Extract repository count from GitHub page
        const match = html.match(
            /<span[^>]*class="[^"]*Counter[^"]*"[^>]*>([\d,\.]+)<\/span>/i
        );

        if (!match) {
            throw new Error('Repository count not found');
        }

        const totalTopicRepos = match[1]
            .replace(/[^\d]/g, '');

        return parseInt(totalTopicRepos, 10);

    } catch (e) {
        console.error(e.message);
        return null;
    }
}


// Example usage:
//(async () => { const result = await getTotalGithubRepositoriesByTopicAndLanguageId( 'google' ); console.log(result); })();