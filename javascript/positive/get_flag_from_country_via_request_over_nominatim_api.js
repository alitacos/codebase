async function get_flag_from_country_via_request_over_nominatim_api(city = "", country = "") {
    if (!country && city) {
        const url = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(city)}&format=json&addressdetails=1&limit=1`;

        const r = await fetch(url, {
            headers: {
                "User-Agent": "city-flag-lookup/1.0"
            }
        });

        if (!r.ok) return "";

        const data = await r.json();

        if (!data.length) return "";

        country = data[0]?.address?.country_code || "";
    }

    if (!country) return "";

    return `https://flagcdn.com/w320/${country.toLowerCase()}.png`;
}

//(async function() { console.log(await get_flag_url("Stuttgart")); console.log(await get_flag_url("", "Germany")); })();