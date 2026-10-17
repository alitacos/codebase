const axios = require("axios");
const cheerio = require("cheerio");

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function collectDefaultGithubTopicsDictOfGithubTopicsPagesByRangeWithoutLangParamsViaAxiosNCheerio({ urlBaseTopics = "https://github.com/topics", topicPages = [1, 2, 3, 4, 5, 6], allowRedirects = true, jsonPayload = null, dataPayload = null, queryPayload = null, timeout = 3000, retries = 3, delay = 2000, cookies = null, headers = {} } = {}) {

    const topics = [];

    for (const pageNum of topicPages) {
        let error = null;

        for (let attempt = 0; attempt < retries; attempt++) {
            try {
                const response = await axios({
                    method: "GET",
                    url: urlBaseTopics,
                    params: {
                        page: pageNum,
                        ...(queryPayload || {})
                    },
                    data: dataPayload,
                    headers: {
                        ...(headers || {}),
                        ...(cookies ? {
                            Cookie: Object.entries(cookies)
                                .map(([k, v]) => `${k}=${v}`)
                                .join("; ")
                        } : {})
                    },
                    maxRedirects: allowRedirects ? 5 : 0,
                    timeout
                });

                if (response.status === 200) {
                    const $ = cheerio.load(response.data);

                    $("a.no-underline.flex-1.d-flex.flex-column").each((_, element) => {
                        const topicHref = $(element).attr("href");
                        const topicName = $(element)
                            .find("p.f3.lh-condensed.mb-0.mt-1.Link--primary")
                            .text()
                            .trim();

                        const id = topicHref.split("/").pop();
                        const topicUrl = `https://github.com/topics/${id}`;

                        topics.push({
                            name: topicName,
                            url: topicUrl,
                            id
                        });
                    });

                    break; // success
                }

            } catch (e) {
                error = e;
            }

            if (attempt < retries - 1) {
                await sleep(delay);
            }
        }

        if (error) {
            // Optional:
            // console.error(`Page ${pageNum}:`, error.message);
        }
    }

    return topics;
}

// (async () => { const topics = await collectDefaultGithubTopicsDictOfGithubTopicsPagesByRangeWithoutLangParamsViaAxiosNCheerio(); console.log(topics); })();
