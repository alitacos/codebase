async function fetch_all_root_servers_info_to_dict_from_iana_server() {
    const url = "https://www.iana.org/domains/root/servers";

    const headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "max-age=0",
        "referer": "https://www.iana.org/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/139 Safari/537.36"
    };

    const response = await fetch(url, { headers });

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    const html = await response.text();

    const rows = [...html.matchAll(/<tr[^>]*>([\s\S]*?)<\/tr>/gi)]
        .map(i => i[1])
        .filter(i => i.includes("<td"));

    const result = [];

    for (const row of rows) {
        const cells = [...row.matchAll(/<td[^>]*>([\s\S]*?)<\/td>/gi)]
            .map(i => i[1].replace(/<[^>]*>/g, "").trim());

        if (!cells.length) continue;

        const ip_values = (cells[cells.length - 2] || "").split(",").map(i => i.trim());

        result.push({
            hostname: cells[0] || "",
            ip4: ip_values[0] || "",
            ip6: ip_values[1] || "",
            operator: cells.length === 3 ? cells[2] : "",
            class: "root_server"
        });
    }

    return result;
}


// call
//(async () => { console.log(await fetch_all_root_servers_info_to_dict_from_iana_server()); })();