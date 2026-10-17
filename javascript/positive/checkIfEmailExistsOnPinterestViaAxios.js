const axios = require("axios");

async function checkIfEmailExistsOnPinterestViaAxios(email="") {
    if (!email) {
        return false;
    }

    try {
        const sourceUrl = "/password/reset/";
        const dataPayload = {"options": {"url": "/v3/register/exists/", "data": {"email": email}}, "context": {}};
        const queryParams = {"source_url": sourceUrl, "data": JSON.stringify(dataPayload), "_": "1750075105176"};
        const baseUrl = "https://de.pinterest.com/resource/ApiResource/get/";

        const headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36", "Accept": "application/json, text/javascript, */*; q=0.01", "Referer": "https://de.pinterest.com/", "X-Requested-With": "XMLHttpRequest", "X-Pinterest-AppState": "active", "X-Pinterest-PWS-Handler": "www/password/reset.js", "X-Pinterest-Source-Url": sourceUrl, "X-App-Version": "d8c18cb"};

        const cookies = {"csrftoken": "0538a04e1f481bb0c00141c16c159970"};

        const response = await axios.get(baseUrl, {
            headers: {...headers, Cookie: Object.entries(cookies).map(([k,v]) => `${k}=${v}`).join("; ")},
            params: queryParams
        });

        const output = response.data;
        return output?.resource_response?.data || false;

    } catch (e) {
        return null;
    }
}


//example usage:
//(async () => { console.log(await checkIfEmailExistsOnPinterestViaRequests("example@gmail.com")); //True console.log(await checkIfEmailExistsOnPinterestViaAxios("os@gmail.com")); //False })();