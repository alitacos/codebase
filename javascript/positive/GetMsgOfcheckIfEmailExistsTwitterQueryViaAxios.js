const axios = require("axios");
async function GetMsgOfcheckIfEmailExistsTwitterQueryViaAxios(email = "") {
    try {
        const response = await axios.get(
            `https://api.x.com/i/users/email_available.json?email=${encodeURIComponent(email)}`
        );

        return response.data.msg;

    } catch (e) {
        return null;
    }
}

// Example
// (async () => { console.log(await GetMsgOfcheckIfEmailExistsTwitterQueryViaAxios("anon@gmail.com")); })();