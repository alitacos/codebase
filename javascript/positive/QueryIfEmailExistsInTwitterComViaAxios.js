const axios = require("axios");

async function QueryIfEmailExistsInTwitterComViaAxios(email = "") {
    if (!email) {
        email = "";
    }

    try {
        const response = await axios.get(
            `https://api.x.com/i/users/email_available.json?email=${encodeURIComponent(email)}`,
            {
                validateStatus: () => true
            }
        );

        let data;

        try {
            const dictResponse = response.data;

            data = {
                error: null,
                status_code: response.status,
                valid: dictResponse.valid,
                msg: dictResponse.msg,
                taken: dictResponse.taken
            };
        } catch (e) {
            data = {
                error: String(e),
                status_code: response.status,
                valid: false,
                msg: null,
                taken: null
            };
        }

        if (!data) {
            return false;
        }

        return data.taken;

    } catch (e) {
        return false;
    }
}

// (async () => {  console.log(await QueryIfEmailExistsInTwitterComViaAxios("f")); // false console.log(await checkIfEmailExistsAlreadyInTwitterCom("anon@gmail.com")); // true console.log(await checkIfEmailExistsAlreadyInTwitterCom("alitakos90@gmail.com")); // false })();
