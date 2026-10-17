async function check_if_username_exists_in_blogspot_via_fetch(username = "", retries = 3, delay = 2, allow_redirects = true) {
    if (!username || typeof username !== "string" || !username.trim()) {
        return {
            error: "invalid <username> value",
            status: null,
            username: username,
            content: null,
            redirect: null,
            title: null,
            available: false,
            exists: false,
            isdeleted: false
        };
    }

    const headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/143 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    };

    let last_error = null;
    let title = null;

    for (let i = 0; i < retries; i++) {
        let status_code = null;

        try {
            const url = `https://${username.trim()}.blogspot.com`;

            const response = await fetch(url, {
                headers,
                redirect: allow_redirects ? "follow" : "manual"
            });

            status_code = response.status;

            const html = await response.text();

            const title_match = html.match(/<h1[^>]*>(.*?)<\/h1>/is);

            title = title_match
                ? title_match[1].replace(/<[^>]+>/g, "").trim()
                : null;

            const raw = html
                .replace(/<script[\s\S]*?<\/script>/gi, "")
                .replace(/<style[\s\S]*?<\/style>/gi, "")
                .replace(/<[^>]+>/g, "\n")
                .split("\n")
                .map(i => i.trim())
                .filter(i => i)
                .join("\n");

            const redirect = response.url;

            if ([200, 404].includes(status_code)) {

                if (status_code === 404) {
                    if (title && ["Blog nicht gefunden.", "Blog not found"].includes(title)) {
                        return {
                            error: false,
                            status: status_code,
                            username,
                            content: raw,
                            redirect,
                            title,
                            available: true,
                            exists: false,
                            isdeleted: false
                        };
                    }

                    if (title && ["Blog wurde entfernt.", "Blog has been removed"].includes(title)) {
                        return {
                            error: false,
                            status: status_code,
                            username,
                            content: raw,
                            redirect,
                            title,
                            available: true,
                            exists: false,
                            isdeleted: true
                        };
                    }
                }

                if (status_code === 200) {
                    return {
                        error: false,
                        status: status_code,
                        username,
                        content: raw,
                        redirect,
                        title,
                        available: false,
                        exists: true,
                        isdeleted: false
                    };
                }
            }

            last_error = `unexpected status code: ${status_code}`;

            await new Promise(resolve => setTimeout(resolve, delay * 1000));

        } catch (e) {
            last_error = String(e);

            await new Promise(resolve => setTimeout(resolve, delay * 1000));
        }
    }

    return {
        error: last_error,
        status: null,
        username,
        content: null,
        redirect: null,
        title,
        available: null,
        exists: null,
        isdeleted: null
    };
}


// calls
// (async () => { console.log(await check_if_username_exists_in_blogspot_via_fetch("anonymous")); })();
// (async () => { console.log(await check_if_username_exists_in_blogspot_via_fetch("alitakos90")); })();