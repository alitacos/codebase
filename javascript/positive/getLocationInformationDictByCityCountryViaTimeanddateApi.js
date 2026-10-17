async function getLocationInformationDictByCityCountryViaTimeanddateApi(country = '', city = '', verbos = false) {
    try {
        const url = 'https://www.timeanddate.com/scripts/completion.php';
        const outs = [];

        if (city) {
            const req = await fetch(`${url}?query=${encodeURIComponent(city)}`);
            const raw = await req.text();
            const lines = raw.split('\n');

            for (const line of lines) {
                if (city.toLowerCase().includes(line.toLowerCase())) {
                    const item = line.split('\t');

                    try {
                        outs.push({
                            clock_data_url:`https://www.timeanddate.com/scripts/completion.php/${item[0]}`,
                            zone_json:`https://www.timeanddate.com/scripts/completion.php?mode=tzmappos&p1=${item[1]}`,
                            iso_alpha_2_code:item[2],
                            country_state_code:item[3],
                            place:item[4],
                            sub_region:item[5],
                            country:item[6],
                            flag:item[7]
                        });
                    } catch (e1) {}
                }
            }
        }

        if (country && (!city || outs.length === 0)) {
            const req = await fetch(`${url}?query=${encodeURIComponent(country)}`);
            const raw = await req.text();
            const lines = raw.split('\n');

            for (const line of lines) {
                try {
                    if (country.toLowerCase().includes(line.toLowerCase())) {
                        const item = line.split('\t');

                        outs.push({
                            clock_data_url:`https://www.timeanddate.com/scripts/completion.php/${item[0]}`,
                            zone_json:`https://www.timeanddate.com/scripts/completion.php?mode=tzmappos&p1=${item[1]}`,
                            iso_alpha_2_code:item[2],
                            country_state_code:item[3],
                            place:item[4],
                            sub_region:item[5],
                            country:item[6],
                            flag:item[7]
                        });
                    }
                } catch (e2) {}
            }
        }

        const unique = [...new Set(outs.filter(i => i).map(i => JSON.stringify(i)))];
        return unique.map(i => JSON.parse(i)).sort((a,b) => JSON.stringify(a).localeCompare(JSON.stringify(b)));

    } catch (e) {
        if (verbos) console.log(String(e));
        return [];
    }
}


// example usage:
//(async()=>{console.log(await getLocationInformationDictByCityCountryViaTimeanddateApi('Germany'));console.log(await getLocationInformationDictByCityCountryViaTimeanddateApi('Berlin'));console.log(await getLocationInformationDictByCityCountryViaTimeanddateApi('Stuttgart'));})();