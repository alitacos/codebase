async function checkIfUsernameExistsInBlogspotViaRequestsAndBs4(
    username = '',
    retries = 3,
    delay = 2000,
    allowRedirects = true
) {
    /*
        Checks whether a Blogspot username exists, is available,
        or has been removed by fetching the blog page and parsing HTML.

        Returns:
        {
            error,
            status,
            username,
            content,
            redirect,
            title,
            available,
            exists,
            isdeleted
        }
    */

    if (!username || typeof username !== "string" || !username.trim()) {
        return {
            error: "invalid <username> value",
            status: null,
            username,
            content: null,
            redirect: null,
            title: null,
            available: false,
            exists: false,
            isdeleted: false
        };
    }

    const headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    };

    let lastError = null;

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    function cleanText(html) {
        return html
            .replace(/<script[\s\S]*?<\/script>/gi, "")
            .replace(/<style[\s\S]*?<\/style>/gi, "")
            .replace(/<[^>]+>/g, "")
            .split("\n")
            .map(x => x.trim())
            .filter(Boolean)
            .join("\n");
    }

    function extractH1(html) {
        const match = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);

        if (!match) return null;

        return match[1]
            .replace(/<[^>]+>/g, "")
            .trim();
    }

    for (let attempt = 0; attempt < retries; attempt++) {
        try {
            const url = `https://${username}.blogspot.com`;

            const response = await fetch(url, {
                method: "GET",
                headers,
                redirect: allowRedirects ? "follow" : "manual"
            });

            const html = await response.text();

            const status = response.status;
            const finalUrl = response.url;

            const h1 = extractH1(html);
            const content = cleanText(html);


            if ([200, 404].includes(status)) {

                if (status === 404) {

                    if (h1 && [
                        "Blog nicht gefunden.",
                        "Blog not found"
                    ].includes(h1)) {
                        return {
                            error: false,
                            status,
                            username,
                            content,
                            redirect: finalUrl,
                            title: h1,
                            available: true,
                            exists: false,
                            isdeleted: false
                        };
                    }


                    if (h1 && [
                        "Blog wurde entfernt.",
                        "Blog has been removed"
                    ].includes(h1)) {
                        return {
                            error: false,
                            status,
                            username,
                            content,
                            redirect: finalUrl,
                            title: h1,
                            available: true,
                            exists: false,
                            isdeleted: true
                        };
                    }
                }


                if (status === 200) {
                    return {
                        error: false,
                        status,
                        username,
                        content,
                        redirect: finalUrl,
                        title: h1,
                        available: false,
                        exists: true,
                        isdeleted: false
                    };
                }
            }


            lastError = `unexpected status code: ${status}`;
            await sleep(delay * 1000);

        } catch (e) {
            lastError = e.message;
            await sleep(delay * 1000);
        }
    }


    return {
        error: lastError,
        status: null,
        username,
        content: null,
        redirect: null,
        title: null,
        available: null,
        exists: null,
        isdeleted: null
    };
}


// Example usage
(async () => {
    console.log(
        await checkIfUsernameExistsInBlogspotViaRequestsAndBs4(
            "mrxx",
            3,
            2,
            true
        )
    );

    console.log(
        await checkIfUsernameExistsInBlogspotViaRequestsAndBs4(
            "alitakos90"
        )
    );

    console.log(
        await checkIfUsernameExistsInBlogspotViaRequestsAndBs4(
            "adacic"
        )
    );
})();