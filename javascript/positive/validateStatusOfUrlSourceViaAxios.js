const axios = require("axios");

async function validateStatusOfUrlSourceViaAxios(
    source = "",
    cookies = {},
    params = {},
    headers = {},
    verbose = true
) {
    if (!source) {
        if (verbose) {
            console.log("source (str) object is missing");
        }
        return null;
    }

    try {
        await axios.get(source, {
            params,
            headers: {
                ...headers,
                ...(Object.keys(cookies).length > 0
                    ? {
                          Cookie: Object.entries(cookies)
                              .map(([key, value]) => `${key}=${value}`)
                              .join("; ")
                      }
                    : {})
            },
            validateStatus: (status) => status >= 200 && status < 300
        });

        return true;

    } catch (e) {
        if (verbose) {
            console.log(e.message);
        }
        return false;
    }
}

// Example usage:
//(async () => { console.log( await validateStatusOfUrlSourceViaAxios( "http://localhost:8888/lab/tree/Untitled.ipynb" ) ); })();