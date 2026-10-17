async function checkIfUsernameExistsInProtonmailViaRequests(username = '', retries = 3, delay = 2, allowRedirects = true) {
    const url = 'https://account.protonmail.com/api/users/available';

    const headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "Accept":"application/json",
        "x-pm-appversion":"Other"
    };

    if (!username || typeof username !== 'string' || !username.trim()) {
        return {error:'invalid <username> value',status_code:null,username:username,content:null,title:null,available:false,exists:false,redirect:null,isdeleted:null};
    }

    let last_error = null;
    let status_code = null;
    let content = null;
    let redirect = null;

    for (let i = 0; i < retries; i++) {
        try {
            const params = new URLSearchParams({
                Name: username.trim()
            });

            const r = await fetch(`${url}?${params.toString()}`, {
                method:"GET",
                headers:headers,
                redirect:allowRedirects ? "follow" : "manual"
            });

            status_code = r.status;
            redirect = r.url;

            let title = null;

            try {
                content = await r.json();
            } catch (e) {
                const text = await r.text();
                content = text ? text.trim() : null;

                const titleMatch = text.match(/<title[^>]*>(.*?)<\/title>/i);
                title = titleMatch ? titleMatch[1].trim() : null;
            }

            if (content && typeof content === "object" && content.Code) {
                if (content.Code === 1000) {
                    return {
                        error:false,
                        status_code:status_code,
                        username:username,
                        content:content,
                        title:title,
                        available:true,
                        exists:false,
                        redirect:redirect,
                        isdeleted:null
                    };
                }

                if (content.Code === 12106) {
                    return {
                        error:false,
                        status_code:status_code,
                        username:username,
                        content:content,
                        title:title,
                        available:false,
                        exists:true,
                        redirect:redirect,
                        isdeleted:null
                    };
                }
            }

            last_error = 'unexpected response structure';

        } catch (e) {
            last_error = String(e);
        }

        await new Promise(resolve => setTimeout(resolve, delay * 1000));
    }

    return {
        error:last_error,
        status_code:status_code,
        username:username,
        content:content,
        title:null,
        available:null,
        exists:null,
        redirect:redirect,
        isdeleted:null
    };
}


// example usage:
//(async()=>{console.log(await checkIfUsernameExistsInProtonmailViaRequests('test'));})();