const axios = require("axios");
const cheerio = require("cheerio");
// Not working.often get blocked
async function getUrlTitle(url = "") {
    try {
        const response = await axios.get(url, {
            headers: {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            },
            timeout: 10000
        });

        const $ = cheerio.load(response.data);

        return {
            status: response.status,
            title: $("title").first().text().trim()
        };

    } catch (e) {
        return {
            status: null,
            title: "",
            error: String(e)
        };
    }
}


// (async()=>{    console.log(await getUrlTitle("https://www.quora.com"));})();