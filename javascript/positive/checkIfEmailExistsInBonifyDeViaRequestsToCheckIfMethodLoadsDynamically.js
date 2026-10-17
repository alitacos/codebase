const axios = require("axios");
const cheerio = require("cheerio");


async function checkIfEmailExistsInBonifyDeViaRequestsToCheckIfMethodLoadsDynamically(email="", cookies=null, headers=null, payload=null) {

    if (!email) {
        throw new Error("Email must be provided");
    }


    const url = "https://sso.bonify.de/oauth2/authorize";


    if (!payload) {
        payload = {"email": email.trim()};
    }


    if (!headers) {
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/137.0.0.0 Safari/537.36"
        };
    }


    if (!cookies) {
        cookies = {};
    }


    try {

        const response = await axios.post(url, payload, {
            headers: {
                ...headers,
                Cookie: Object.entries(cookies).map(([k,v]) => `${k}=${v}`).join("; ")
            },
            timeout: 30000,
            validateStatus: () => true
        });


        if (response.status < 200 || response.status >= 300) {
            return {
                error: "invalid method!",
                status_code: response.status,
                message: "BONIFY.de loads dynamically. visit via selenium https://my.bonify.de/login to start.",
                available: null
            };
        }


        try {

            const result = response.data;

            return {
                error: null,
                status_code: response.status,
                message: result,
                available: null
            };

        } catch (e1) {


            try {

                const soup = cheerio.load(response.data);

                const h1 = soup("h1").text().trim().replace(/\s+/g, " ");

                if (h1.startsWith("404")) {

                    return {
                        error: "invalid method! " + h1,
                        status_code: 404,
                        message: "BONIFY.de loads dynamically. visit via selenium https://my.bonify.de/login to start.",
                        available: null
                    };

                } else {

                    return {
                        error: "invalid method! " + (h1 || soup("body").text().trim().replace(/\s+/g, " ")),
                        status_code: 404,
                        message: "BONIFY.de loads dynamically. visit via selenium https://my.bonify.de/login to start.",
                        available: null
                    };

                }


            } catch (e2) {

                return {
                    error: String(e2),
                    status_code: response.status,
                    message: "BONIFY.de loads dynamically. visit via selenium https://my.bonify.de/login to start.",
                    available: null
                };

            }

        }


    } catch (e1) {

        return {
            error: "invalid method!",
            status_code: null,
            message: "BONIFY.de loads dynamically. visit via selenium https://my.bonify.de/login to start.",
            available: null
        };

    }

}


// example usage:
//(async () => { console.log( await checkIfEmailExistsInBonifyDeViaRequestsToCheckIfMethodLoadsDynamically("unknown@gmail.com") ); })();