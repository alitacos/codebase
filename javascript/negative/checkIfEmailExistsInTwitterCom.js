async function checkIfEmailExistsInTwitterCom(email = "") {
    try {
        const response = await axios.get(
            "https://api.x.com/i/users/email_available.json",
            {
                params: { email }
            }
        );

        const dictResponse = response.data;

        const data = {
            error: null,
            status_code: response.status,
            valid: dictResponse.valid,
            msg: dictResponse.msg,
            taken: dictResponse.taken
        };

        return data.taken;
    } catch (e) {
        return false;
    }
}

// Example:


//(async () => { console.log(await checkIfEmailExistsAlreadyInTwitterCom("f")); console.log(await checkIfEmailExistsAlreadyInTwitterCom("anon@gmail.com")); console.log(await checkIfEmailExistsInTwitterCom("alitakos90@gmail.com")); })();
 