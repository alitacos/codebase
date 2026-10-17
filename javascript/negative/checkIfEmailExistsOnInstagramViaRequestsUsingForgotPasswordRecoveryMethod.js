async function checkIfEmailExistsOnInstagramViaRequestsUsingForgotPasswordRecoveryMethod(
    email = '',
    csrfToken = '',
    cookies = {},
    headers = {},
    payload = {}
) {
    const url = "https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/";

    if (!Object.keys(cookies).length) {
        cookies = {
            // "csrftoken": "QdU1jSZtmXQDGNEZSIko9RyaULjbUZ26",
            // "ig_did": "AF72D69E-A8AE-4D77-B7C5-4BED3C04619A",
            // "mid": "aFBQOQALAAG-7p-hT6pUQb6WlDzk",
            // "datr": "OVBQaDl9XJU8lUc6cr2NYRIV",
            // "dpr": "1.25",
            // "wd": "638x730"
        };
    }

    if (!Object.keys(headers).length) {
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "X-CSRFToken": csrfToken || "QdU1jSZtmXQDGNEZSIko9RyaULj"
        };
    }

    if (!Object.keys(payload).length) {
        payload = {
            email_or_username: email.trim(),
            jazoest: "22739"
        };
    }

    try {
        const cookieString = Object.entries(cookies)
            .map(([key, value]) => `${key}=${value}`)
            .join("; ");

        if (cookieString) {
            headers["Cookie"] = cookieString;
        }

        const body = new URLSearchParams(payload).toString();

        const response = await fetch(url, {
            method: "POST",
            headers: {
                ...headers,
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body
        });

        const statusCode = response.status;
        const json = await response.json();

        const responseString = JSON.stringify(json);

        if (
            responseString.includes(
                `We sent an email to ${email} with a link to get back into your account.`
            )
        ) {
            return {
                error: null,
                status_code: statusCode,
                message: json.toast_message,
                available: 0
            };
        } 
        
        if (responseString.includes("No users found")) {
            return {
                error: null,
                status_code: statusCode,
                message: json.message,
                available: 1
            };
        }

        if (responseString.includes("CSRF token missing or incorrect")) {
            return {
                error: json.message,
                status_code: statusCode,
                message: null,
                available: null
            };
        }

        return {
            error: "unknown error",
            status_code: statusCode,
            message: json,
            available: null
        };

    } catch (e) {
        return {
            error: e.message,
            status_code: null,
            message: null,
            available: null
        };
    }
}


// Example usage
// (async () => {    const result = await checkIfEmailExistsOnInstagramViaRequestsUsingForgotPasswordRecoveryMethod(        "example@gmail.com"    );    console.log(result);})();
// [out]: {'error': 'Expecting value: line 1 column 1 (char 0)', 'status_code': None, 'message': None, 'available': None}
