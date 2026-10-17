async function getTotalGithubRepositoriesByTopicAndLanguageId(topic = '', lang = '*') {
    try {
        const cleanTopic = topic.trim().toLowerCase();
        const cleanLang = lang.trim().toLowerCase();

        let url = `https://github.com/topics/${encodeURIComponent(cleanTopic)}`;

        if (cleanLang && !['*', 'all'].includes(cleanLang)) {
            url += `?l=${encodeURIComponent(cleanLang)}`;
        }

        const response = await fetch(url, {
            headers: {
                "User-Agent": "Mozilla/5.0"
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }

        const html = await response.text();

        // GitHub page text extraction
        const text = html
            .replace(/<[^>]*>/g, ' ')
            .replace(/\s+/g, ' ');

        const match = text.match(
            /([\d,]+)\s+public repositories matching this topic/i
        );

        if (!match) {
            throw new Error("Repository count not found");
        }

        return Number(match[1].replace(/,/g, ''));

    } catch (e) {
        console.error(e.message);
        return null;
    }
}


// Example usage:
//(async () => { console.log( await getTotalGithubRepositoriesByTopicAndLanguageId('google') ); console.log( await getTotalGithubRepositoriesByTopicAndLanguageId( 'machine-learning', 'python' ) ); })();
