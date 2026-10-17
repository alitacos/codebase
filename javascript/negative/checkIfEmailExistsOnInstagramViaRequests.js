async function async function checkIfEmailExistsOnInstagramViaRequests(email = '', retries = 3, delay = 2, csrfToken = 'QdU1jSZtmXQDGNEZSIko9RyaULj', url = 'https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/', headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36","Accept":"*/*","Accept-Language":"en-US,en;q=0.9"}, ...kwargs) {
    if (!email || typeof email !== 'string' || !email.trim()) {
        return {email:email,error:'ValueError',status_code:null,message:'Invalid <email>',available:false,exists:false,isdeleted:false};
    }

    try {
        headers["X-CSRFToken"] = csrfToken;
    } catch (e1) {
        return {email:email,error:e1,status_code:null,message:null,available:null,exists:null,isdeleted:null};
    }

    let errorMessage = null;
    let statusCode = null;

    for (let attempt = 0; attempt < Number(retries); attempt++) {
        try {
            const payload = new URLSearchParams({
                email_or_username: email.trim(),
                jazoest: '22739'
            });

            const response = await fetch(url, {
                method:"POST",
                headers:{
                    ...headers,
                    "Content-Type":"application/x-www-form-urlencoded"
                },
                body:payload.toString(),
                ...kwargs
            });

            statusCode = response.status;

            if (response.status === 200) {
                let jsonResponse;

                try {
                    jsonResponse = await response.json();
                } catch (e) {
                    return {email:email,error:'JSONDecodeError',status_code:statusCode,message:'Response body is not valid JSON',available:null,exists:null,isdeleted:null};
                }

                const responseString = JSON.stringify(jsonResponse);

                if (responseString.includes(`We sent an email to ${email} with a link to get back into your account.`)) {
                    return {email:email,error:false,status_code:statusCode,message:jsonResponse.toast_message || '',available:false,exists:true,isdeleted:null};
                }

                if (responseString.includes('No users found')) {
                    return {email:email,error:false,status_code:statusCode,message:jsonResponse.message || '',available:true,exists:false,isdeleted:null};
                }

                if (responseString.includes('CSRF token missing or incorrect')) {
                    return {email:email,error:true,status_code:statusCode,message:jsonResponse.message || '',available:null,exists:null,isdeleted:null};
                }

            } else {
                errorMessage = `Unexpected status code: ${statusCode}`;
            }

        } catch (e) {
            errorMessage = String(e);
        }

        if (attempt < retries - 1) {
            await new Promise(resolve => setTimeout(resolve, delay * 1000));
        }
    }

    return {
        email:email,
        error:errorMessage || 'Request failed',
        status_code:statusCode,
        message:String(errorMessage),
        available:null,
        exists:null,
        isdeleted:null
    };
}


// example usage:
//(async()=>{console.log(await checkIfEmailExistsOnInstagramViaRequests('alitakos90@gmail.com',3,2,'koN-IKObKCU3XhXelQjKUA'));})();(email = '', retries = 3, delay = 2, csrfToken = 'QdU1jSZtmXQDGNEZSIko9RyaULj', url = 'https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/', headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36","Accept":"*/*","Accept-Language":"en-US,en;q=0.9"}, ...kwargs) {
    if (!email || typeof email !== 'string' || !email.trim()) {
        return {email:email,error:'ValueError',status_code:null,message:'Invalid <email>',available:false,exists:false,isdeleted:false};
    }

    try {
        headers["X-CSRFToken"] = csrfToken;
    } catch (e1) {
        return {email:email,error:e1,status_code:null,message:null,available:null,exists:null,isdeleted:null};
    }

    let errorMessage = null;
    let statusCode = null;

    for (let attempt = 0; attempt < Number(retries); attempt++) {
        try {
            const payload = new URLSearchParams({
                email_or_username: email.trim(),
                jazoest: '22739'
            });

            const response = await fetch(url, {
                method:"POST",
                headers:{
                    ...headers,
                    "Content-Type":"application/x-www-form-urlencoded"
                },
                body:payload.toString(),
                ...kwargs
            });

            statusCode = response.status;

            if (response.status === 200) {
                let jsonResponse;

                try {
                    jsonResponse = await response.json();
                } catch (e) {
                    return {email:email,error:'JSONDecodeError',status_code:statusCode,message:'Response body is not valid JSON',available:null,exists:null,isdeleted:null};
                }

                const responseString = JSON.stringify(jsonResponse);

                if (responseString.includes(`We sent an email to ${email} with a link to get back into your account.`)) {
                    return {email:email,error:false,status_code:statusCode,message:jsonResponse.toast_message || '',available:false,exists:true,isdeleted:null};
                }

                if (responseString.includes('No users found')) {
                    return {email:email,error:false,status_code:statusCode,message:jsonResponse.message || '',available:true,exists:false,isdeleted:null};
                }

                if (responseString.includes('CSRF token missing or incorrect')) {
                    return {email:email,error:true,status_code:statusCode,message:jsonResponse.message || '',available:null,exists:null,isdeleted:null};
                }

            } else {
                errorMessage = `Unexpected status code: ${statusCode}`;
            }

        } catch (e) {
            errorMessage = String(e);
        }

        if (attempt < retries - 1) {
            await new Promise(resolve => setTimeout(resolve, delay * 1000));
        }
    }

    return {
        email:email,
        error:errorMessage || 'Request failed',
        status_code:statusCode,
        message:String(errorMessage),
        available:null,
        exists:null,
        isdeleted:null
    };
}


// example usage:
//(async()=>{console.log(await checkIfEmailExistsOnInstagramViaRequests('alitakos90@gmail.com',3,2,'koN-IKObKCU3XhXelQjKUA'));})();