async function checkIfEmailExistsInTwitterAsBoolean(email = '') {
    if (!email) {
        email = '';
    }

    const url = `https://api.x.com/i/users/email_available.json?email=${encodeURIComponent(email)}`;

    let data;

    try {
        const response = await fetch(url);
        const dictResponse = await response.json();

        data = {
            error: null,
            status_code: response.status,
            valid: dictResponse.valid,
            msg: dictResponse.msg,
            taken: dictResponse.taken
        };
    } catch (e) {
        data = {
            error: e.message,
            status_code: 0,
            valid: false,
            msg: null,
            taken: null
        };
    }

    if (!data) {
        return false;
    }

    console.log(data);

    return data.taken ?? false;
}


// Example usage:
//(async () => { console.log( await checkIfEmailExistsInTwitterAsBoolean('f') ); console.log( await checkIfEmailExistsInTwitterAsBoolean('anonymous@grr.la') ); console.log( await checkIfEmailExistsInTwitterAsBoolean('anonymous@gmail.com') ); })();