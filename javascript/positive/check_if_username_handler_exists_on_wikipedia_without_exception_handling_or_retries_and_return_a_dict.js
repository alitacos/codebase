async function check_if_username_handler_exists_on_wikipedia_without_exception_handling_or_retries_and_return_a_dict(
    target = '',
    allow_redirects = true
) {
    const headers = {
        "user-agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/104.0 Safari/537.36"
    };

    const url = `https://www.wikipedia.org/wiki/User:${target}`;

    const response = await fetch(url, {
        method: "GET",
        headers,
        redirect: allow_redirects ? "follow" : "manual"
    });

    const text = await response.text();

    const titleMatch = text.match(/<title[^>]*>(.*?)<\/title>/i);
    const title = titleMatch
        ? titleMatch[1].replace(/&amp;/g, "&")
        : null;

    const raw = text
        .replace(/<script[\s\S]*?<\/script>/gi, "")
        .replace(/<style[\s\S]*?<\/style>/gi, "")
        .replace(/<[^>]+>/g, " ")
        .replace(/\s+/g, " ")
        .trim();

    let exists = null;
    let available = null;

    if (response.status === 200) {
        exists = true;
        available = false;
    }

    if (response.status === 404) {
        exists = false;
        available = true;
    }

    return {
        title,
        status_code: response.status,
        raw,
        redirect: response.url,
        exists,
        available
    };
}

