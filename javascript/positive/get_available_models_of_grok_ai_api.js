async function get_available_models_of_grok_ai_api(api_key = "", retries = 3, delay = 5) {

    const url = "https://api.groq.com/openai/v1/models";

    if (!api_key) {
        return {
            error: "Failed to query. Provide a valid api_key argument",
            status: null,
            object: null,
            data: []
        };
    }

    const headers = {
        "Authorization": `Bearer ${api_key}`,
        "Content-Type": "application/json"
    };

    let status_code = null;
    let last_error = null;

    for (let attempt = 0; attempt < Number(retries); attempt++) {
        try {
            const response = await fetch(url, {
                method: "GET",
                headers
            });

            status_code = response.status;

            if (status_code === 200) {
                const data = await response.json();

                return {
                    error: null,
                    status: status_code,
                    object: data.object || null,
                    data: data.data || []
                };
            }

            if (status_code === 429) {
                await new Promise(resolve => setTimeout(resolve, 5000));
                continue;
            }

            await new Promise(resolve => setTimeout(resolve, Number(delay) * 1000));

        } catch (e) {
            last_error = String(e);
            await new Promise(resolve => setTimeout(resolve, Number(delay) * 1000));
        }
    }

    return {
        error: last_error || `Request failed with status ${status_code}`,
        status: status_code,
        object: null,
        data: []
    };
}


// call
//(async () => { console.log(await get_available_models_of_grok_ai_api("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")); })();