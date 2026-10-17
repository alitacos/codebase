async function checkIfEmailExistsOnPinterest(email = "", verbose = false, fetchFn = fetch) {
  if (!email) {
    if (verbose) console.log("Missing email");
    return false;
  }

  try {
    const sourceUrl = "/password/reset/";

    const payload = {
      options: {
        url: "/v3/register/exists/",
        data: { email }
      },
      context: {}
    };

    const params = new URLSearchParams({
      source_url: sourceUrl,
      data: JSON.stringify(payload),
      _: Date.now().toString()
    });

    const response = await fetchFn(
      `https://de.pinterest.com/resource/ApiResource/get/?${params}`,
      {
        headers: {
          "User-Agent": "Mozilla/5.0",
          "Accept": "application/json",
          "X-Requested-With": "XMLHttpRequest",
          "X-Pinterest-AppState": "active",
          "X-Pinterest-Source-Url": sourceUrl
        }
      }
    );

    const output = await response.json();

    if (verbose) {
      console.log("Status:", response.status);
      console.log(output);
    }

    const data = output?.resource_response?.data;

    if (Array.isArray(data)) {
      return {
        ...output,
        available: data.length === 0,
        taken: data.length > 0
      };
    }

    return false;

  } catch (err) {
    if (verbose) console.log(err.message);
    return false;
  }
}


// TEST
(async () => {

  const mockFetch = async () => ({
    status: 200,
    json: async () => ({
      resource_response: {
        data: []
      }
    })
  });


  const result = await checkIfEmailExistsOnPinterest(
    "alitakos90@web.com",
    true,
    mockFetch
  );

  console.log(result);

})();
