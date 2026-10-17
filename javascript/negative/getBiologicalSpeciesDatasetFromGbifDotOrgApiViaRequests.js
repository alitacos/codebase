async function getBiologicalSpeciesDatasetFromGbifDotOrgApiViaRequests() {
    const species = [];

    for (const i of [1, 6, 52, 54, 216, 220, 797, 811, 1470, 7707728]) {
        try {
            const url = `https://api.gbif.org/v1/species/${i}`;

            const r = await fetch(url);

            if (!r.ok) {
                throw new Error(`HTTP error ${r.status}`);
            }

            const data = await r.json();

            for (const item of data) {
                if (!species.includes(item)) {
                    species.push(item);
                }
            }

        } catch (e) {
            console.log(`Request error for ID ${i}: ${e}`);
        }
    }

    return species;
}


// example usage:
//(async()=>{console.log(await getBiologicalSpeciesDatasetFromGbifDotOrgApiViaRequests());})();