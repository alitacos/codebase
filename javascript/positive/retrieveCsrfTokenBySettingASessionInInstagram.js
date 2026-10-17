async function retrieveCsrfTokenBySettingASessionInInstagram() {
    const headers = {
        "User-Agent":"Mozilla/5.0",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    };

    const response = await fetch("https://www.instagram.com/", {
        method:"GET",
        headers:headers
    });

    const cookies = response.headers.get("set-cookie") || "";

    const match = cookies.match(/csrftoken=([^;]+)/);

    return match ? match[1] : null;
}


// example usage:
//(async()=>{console.log(await retrieveCsrfTokenBySettingASessionInInstagram());})();