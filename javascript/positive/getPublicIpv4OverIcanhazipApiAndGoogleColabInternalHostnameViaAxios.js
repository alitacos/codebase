const axios = require("axios");

async function getPublicIpv4OverIcanhazipApiAndGoogleColabInternalHostnameViaAxios() {
    let publicIp = null;
    let internalHostname = null;

    try {
        const response = await axios.get("https://icanhazip.com", {
            responseType: "text"
        });
        publicIp = String(response.data).trim();
    } catch (e) {
        publicIp = null;
    }

    try {
        internalHostname = require("os").hostname();
    } catch (e) {
        internalHostname = null;
    }

    return [publicIp, internalHostname];
}

// Example:
// (async () => { const [publicIp, internalHostname] = await getPublicIpv4OverIcanhazipApiAndGoogleColabInternalHostnameViaAxios(); console.log(publicIp); console.log(internalHostname); })();
