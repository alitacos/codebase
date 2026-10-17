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

    const parser = new DOMParser();
    const doc = parser.parseFromString(text, "text/html");

    const titleElement = doc.querySelector("title");

    const title = titleElement ? titleElement.textContent : null;

    const raw = doc.body
        ? doc.body.textContent
            .trim()
            .split("\n")
            .filter(i => i && i.trim())
            .map(i => i.trim())
            .join("")
        : "";

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
 
