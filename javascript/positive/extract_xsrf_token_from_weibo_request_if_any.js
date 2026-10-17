async function extract_xsrf_token_from_weibo_request_if_any(r = null) {
    let splits = [];

    if (r && typeof r === "object" && r.headers) {
        const cookie = r.headers.get ? r.headers.get("set-cookie") : r.headers["Set-Cookie"];
        if (cookie) splits = cookie.replace(/,/g, ";").split(";").filter(i => i.trim());
    }

    if (r && typeof r === "object" && !r.headers) {
        const cookie = r["Set-Cookie"] || r["set-cookie"];
        if (cookie) splits = cookie.replace(/,/g, ";").split(";").filter(i => i.trim());
    }

    if (typeof r !== "string" && !splits.length) {
        try {
            r = String(r);
        } catch (e) {
            r = "";
        }
    }

    if (typeof r === "string") {
        if (r.includes("https://m.weibo.cn/n/")) {
            try {
                const response = await fetch(r.trim());
                const cookie = response.headers.get("set-cookie");
                r = cookie || r;
            } catch (e) {
                // keep original string
            }
        }

        splits = r.replace(/,/g, ";").split(";").filter(i => i.trim());
    }

    if (!splits.length) return "";

    const items = splits
        .filter(sp => sp.includes("="))
        .map(sp => {
            const parts = sp.split("=");
            return [parts[0].trim(), parts.slice(1).join("=").trim()];
        });

    const xsrf = items.find(i => i[0].includes("XSRF-TOKEN") && i[1] !== "deleted");

    return xsrf ? xsrf[1] : "";
}


// examples:
// (async () => { console.log(await extract_xsrf_token_from_weibo_request_if_any("https://m.weibo.cn/n/s")); })();
// (async () => { console.log(await extract_xsrf_token_from_weibo_request_if_any({"Set-Cookie":"XSRF-TOKEN=deleted; XSRF-TOKEN=aabf5a; path=/"})); })();