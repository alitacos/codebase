async function get_public_ip_via_fetch_over_icanhazip_api() {
    try {
        const response = await fetch("https://icanhazip.com");

        if (!response.ok) return "";

        return (await response.text()).trim();
    } catch (e) {
        return "";
    }
}


// (async () => { console.log(await get_public_ip_via_fetch_over_icanhazip_api()); })();