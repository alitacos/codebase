def check_profile_data_in_wise_id_eligibility(token:str='')->dict:
    import requests

    url = "https://wise.com/gateway/v1/signups"

    # Correct JSON payload
    payload = {
        "userParams": {
            "email": "alitakos@grr.la",
            "locale": "de-DE",
            "guestId": "b658e789-fe84-411c-b195-cea9920fc71a",
            "isConsentSeen": True
        },
  "challenge": token if token else '',
  "captcha": {
    "token": token if token else '',
    "type": "TURNSTILE"
  },
  "clientId": "transferwise_web",
  "flowId": "default"
}
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "Origin": "https://wise.com",
        "Referer": "https://wise.com/register?redirectUrl=%2Fonboarding%3Forigin%3DSTANDARD&country=DE"
    }

    cookies = {
        "__cf_bm": "c9B3iPJoGAnw2uK.5IrZNDZ49FCq7B4.vD62Ws0ex78-1750069106-1.0.1.1-n5UfMDTn_gXU6zygPwpMwqQFAQ5NN14scM_xfm1FLMFvl7AXt9VuLuPFxatUu2AZCyt.2JftJavO1TFS0dNbRsDhHFXGFbgE4O1FtUAC956ssjKHccxBE7nmcCFCHYmN",
        "appToken": "dad99d7d8e52c2c8aaf9fda788d8acdc",
        "gid": "b658e789-fe84-411c-b195-cea9920fc71a",
        "twCookieConsent": '{"policyId":"2023-10-16","expiry":1765793920041,"isEu":true,"status":"rejected"}',
        "twCookieConsentGTM": "false"
    }


    response = requests.post(url, json=payload, headers=headers, cookies=cookies)

    
    try:
        return response.json()  # <- FIXED: call the method using ()
    except Exception as e:
        return {"error": str(e), "status_code": response.status_code, "text": response.text}
#example usage:
#check_profile_data_in_wise_id_eligibility(token='3dbc5408-6d4c-41d1-95e5-fd93590ba354',profileId = "71258968" ) #out: {'eligible': True, 'eligibilityCode': 'eligible', 'accountType': 'FULL', 'ineligibilityReason': None}
#check_profile_data_in_wise_id_eligibility(token="0.LH5jlqOTtdB4WdfzH73dbY8YWVnSQG0DnW3Ayl5-N-CbS3ImjQlrkDNySDuUFWuPJ16CyHC_yRvCyWfvBy87qDJUogOmIMpZmFH2ealJYRKEYX6qZ5xAlSxIImRIXUhNngPqjGxKRohJa8SRl_pOcs6sgCYYCerM4fZE9acJa_LnqhcFTvoXE4E0vTD1TTG_QXtB_BYVUEFxQTgUxi-B3PBf8GL0JEuu6rNKiRl3FF-jfQyMqbKn-JIcYknXr0LkHDhJKtH-YRbVrf0NjswavOagjzi1Kt4bXH8igPJ2xhmffEpL1_2fmF2aDEojqCD9dTIN5KEm14GLIJar-Yq5M_UCBg0a5vIfj00br8ODgR4URMbv6hknCX6kGWaeArdPLO6BY9zjOQo_gqtK8StY0YXqbcctJhGWD57VVjiTcx1RC4cslTNcPNnB259OEv1_LGOZ0FtrXGTSRU-Fzfu7b2M8fLKk6Ze1PD8cLxKkoDWAkZOzEIfuPW_z5BqAM1yXy0Z3nmqKh8FGWtmeXinzhnVpB1GfFifCxWZyt9Y6cd6N3hgBYYqFBgt7_wP5pG-hxdNMvPs2YHvsmvDMVhIwRxzw_Zs8jwRcvbUbXSS7M8nw5YkI-fDjH3e30LNXdHf1Bv95kbuPx7p_uz6R7EoDYxCmhOVt07UlU9TkJKNlNcUaTzTqe_g21Damc4eISNb1FAm_kVZ7UHkkLX8aU5yA8LpzYtw76tdnTHEblplr-0fRtqWJeeoP8wz_OgZtWFv7hROoDdQFFXeboaasvuIT2OwUs6eS961r2hCsii0GoXjRltGmoepkkajmgkXKCmPJspEmRV_eWVHivOxHa3GCAQQUsH8-5ePIw-KQ8hJbkB4PUjYTyJlwr2a5Yxv8WD8W.COYglNI0d3sXuzQuWFA4Rw.8e133bd4426a01615e975b6ad16ecae50b4c1d770add6a10f23b5fed8b300fc6",profileId = "b658e789-fe84-411c-b195-cea9920fc71a" ) #out: {'error': 'unauthorized', 'message': 'Unauthorized', 'path': None, 'status': 403, 'timestamp': '2025-06-10T23:56:07.613860833Z'} # so if token not match it handles correctly the error

