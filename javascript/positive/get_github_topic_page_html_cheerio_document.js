const cheerio = require("cheerio");

async function get_github_topic_page_html_cheerio_document(topic = null, page = 1, lang = null) {
    function build_github_topic_url(topic = null) {
        return topic && typeof topic === "string" ? `https://github.com/topics/${topic.trim().toLowerCase()}` : null;
    }

    function get_github_topics_page_query_string_parameters_by_page_and_lang_args(page = null, lang = null) {
        page = Number(page);

        if (!Number.isInteger(page)) return {};

        if (lang) return { page: page, l: String(lang).trim().toLowerCase() };

        return { page: page };
    }

    async function get_request_and_parse_content_to_soup_over_url_and_query_params_dict(url = "", params = {}) {
        try {
            const query = new URLSearchParams(params).toString();
            const response = await fetch(`${url}?${query}`);

            if (!response.ok) return null;

            const html = await response.text();

            return cheerio.load(html);
        } catch (e) {
            return null;
        }
    }

    const url = build_github_topic_url(topic);

    const params = url ? get_github_topics_page_query_string_parameters_by_page_and_lang_args(page, lang) : null;

    return url ? await get_request_and_parse_content_to_soup_over_url_and_query_params_dict(url, params || {}) : null;
}


// call
//(async () => { console.log(await get_github_topic_page_html_cheerio_document("python")); })();