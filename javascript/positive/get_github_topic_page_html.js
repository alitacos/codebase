async function get_github_topic_page_html(topic = null, page = 1, lang = null) {
    const url = topic && typeof topic === "string" ? `https://github.com/topics/${topic.trim().toLowerCase()}` : null;

    if (!url) return null;

    const params = new URLSearchParams({ page: Number(page) });

    if (lang) params.append("l", lang.trim().toLowerCase());

    const response = await fetch(`${url}?${params.toString()}`, {
        headers: {
            "User-Agent": "Mozilla/5.0"
        }
    });

    if (!response.ok) return null;

    return await response.text();
}


// call
//(async () => { console.log(await get_github_topic_page_html("python")); })();
