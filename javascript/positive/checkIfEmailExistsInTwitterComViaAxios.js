const axios = require("axios");

async function checkIfEmailExistsInTwitterComViaAxios(email = "") {
    try {
        const response = await axios.get(
            `https://api.x.com/i/users/email_available.json?email=${encodeURIComponent(email)}`,
            {
                validateStatus: () => true
            }
        );

        console.log(response.status);
        console.log(response.headers["content-type"]);
        console.log(response.data);

    } catch (e) {
        console.log(e.message);
    }
}

//(async () => { await checkIfEmailExistsInTwitterComViaAxios("anon@gmail.com"); })();