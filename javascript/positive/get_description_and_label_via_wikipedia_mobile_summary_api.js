async function get_description_and_label_via_wikipedia_mobile_summary_api(
    term = "",
    lang = "de",
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/125 Safari/537.36",
        "Accept": "application/json"
    }
) {
    if (!term || !term.trim()) {
        return {};
    }

    const result = {
        term: term.trim(),
        label: "Unbekannt",
        description: ""
    };

    const term_encoded = term.trim().replace(/ /g, "_");

    try {
        const html_url = `https://${lang}.m.wikipedia.org/wiki/${encodeURIComponent(term_encoded)}`;

        const response = await fetch(html_url, {
            headers,
            signal: AbortSignal.timeout(5000)
        });

        if (response.status === 200) {
            const text = await response.text();

            if (text.includes("<p>")) {
                const start = text.indexOf("<p>") + 3;
                const end = text.indexOf("</p>", start);

                let clean_text = text.substring(start, end);

                clean_text = clean_text.replace(/<[^>]+>/g, "");

                result.description = clean_text.slice(0, 200) + "...";
                result.label = "Aus Webseite extrahiert";
            }
        }
    } catch (e) {
        return result;
    }

    return result;
}


// call
// (async () => { console.log(await get_description_and_label_via_wikipedia_mobile_summary_api("location")); })();