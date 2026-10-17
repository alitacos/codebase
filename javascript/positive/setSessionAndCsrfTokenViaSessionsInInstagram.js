async function setSessionAndCsrfTokenViaSessionsInInstagram() {
    const headers = {
        "User-Agent":"Mozilla/5.0",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    };

    const response = await fetch("https://www.instagram.com/", {
        method:"GET",
        headers:headers
    });

    const cookies = response.headers.get("set-cookie") || "";

    const csrfMatch = cookies.match(/csrftoken=([^;]+)/);
    const csrfToken = csrfMatch ? csrfMatch[1] : null;

    const session = {
        cookies:cookies,
        headers:headers
    };

    return [session, csrfToken];
}


// example usage:
//(async()=>{console.log(await setSessionAndCsrfTokenViaSessionsInInstagram());})();