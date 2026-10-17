const axios = require("axios");

async function testToPostSmsOverFinkMessageMoverServerViaAxios(url="http://202.144.156.212:21186/cgi-bin/sendsms", username="admin", password="admin", sender="+4917600000000", recipient="", message="", priority=3, method="mt", phase=2, silent=0, interactive=1, headers={"Content-Type": "application/x-www-form-urlencoded"}) {

    try {
        const PARAMS = {"username": username.trim(),"password": password.trim(),"from": sender.trim(),"to": recipient.trim(),"text": message.trim(),"priority": Number(priority),"phase": Number(phase),"silent": Number(silent),"method": method,"interactive": Number(interactive)};

        const response = await axios.get(url, {params: PARAMS, headers: headers});

        try {
            return response.data;
        } catch (e1) {
            return response.data;
        }

    } catch (e) {
        return e;
    }
}


// example usage:
//(async () => { console.log( await testToPostSmsOverFinkMessageMoverServer( "http://202.144.156.212:21186/cgi-bin/sendsms", "admin", "admin", "+4917600000000", "+4917600000000", "hellow world!" ) ); })();