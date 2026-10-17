async function checkIfUsernameExistsInBlogspotViaRequestsAndBs4(username = '', retries = 3, delay = 2, allowRedirects = true) {
    if (!username || typeof username !== 'string' || !username.trim()) {
        return {error:'invalid <username> value',status:null,username:username,content:null,redirect:null,title:null,available:false,exists:false,isdeleted:false};
    }

    const headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    };

    const cookies = {};
    let last_error = null;

    for (let i = 0; i < retries; i++) {
        try {
            const url = `https://${username}.blogspot.com`;

            const r = await fetch(url, {
                method:"GET",
                headers:headers,
                redirect:allowRedirects ? "follow" : "manual"
            });

            const html = await r.text();

            const h1_match = html.match(/<h1[^>]*>(.*?)<\/h1>/is);
            const h1 = h1_match ? h1_match[1].replace(/<[^>]*>/g,'').trim() : null;

            const content = html
                .replace(/<script[\s\S]*?<\/script>/gi,'')
                .replace(/<style[\s\S]*?<\/style>/gi,'')
                .replace(/<[^>]+>/g,'')
                .trim()
                .split('\n')
                .map(i => i.trim())
                .filter(i => i && i.trim())
                .join('\n');

            if ([200,404].includes(r.status)) {

                if (r.status === 404) {
                    if (h1 && ["Blog nicht gefunden.","Blog not found"].includes(h1)) {
                        return {error:false,status:r.status,username:username,content:content,redirect:r.url,title:h1,available:true,exists:false,isdeleted:false};
                    }

                    if (h1 && ["Blog wurde entfernt.","Blog has been removed"].includes(h1)) {
                        return {error:false,status:r.status,username:username,content:content,redirect:r.url,title:h1,available:true,exists:false,isdeleted:true};
                    }
                }

                if (r.status === 200) {
                    return {error:false,status:r.status,username:username,content:content,redirect:r.url,title:h1,available:false,exists:true,isdeleted:false};
                }
            }

            last_error = `unexpected status code: ${r.status}`;
            await new Promise(resolve => setTimeout(resolve, delay * 1000));

        } catch (e) {
            last_error = String(e);
            await new Promise(resolve => setTimeout(resolve, delay * 1000));
        }
    }

    return {error:last_error,status:null,username:username,content:null,redirect:null,title:null,available:null,exists:null,isdeleted:null};
}


// example usage:
//(async()=>{console.log(await checkIfUsernameExistsInBlogspotViaRequestsAndBs4('mrxx'));console.log(await checkIfUsernameExistsInBlogspotViaRequestsAndBs4('alitakos90'));console.log(await checkIfUsernameExistsInBlogspotViaRequestsAndBs4('adacic'));})();