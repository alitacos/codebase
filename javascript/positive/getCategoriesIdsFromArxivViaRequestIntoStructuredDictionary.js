async function getCategoriesIdsFromArxivViaRequestIntoStructuredDictionary() {
    try {
        const response = await fetch('https://arxiv.org');

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }

        const html = await response.text();

        // Requires cheerio in Node.js:
        // npm install cheerio
        const cheerio = require('cheerio');

        const $ = cheerio.load(html);

        const data = [];

        $('h2').each((_, h2) => {
            const title = $(h2).text().trim();

            if (title.toLowerCase() === 'arxiv accessibility forum') {
                return;
            }

            const domainData = {
                domain: {
                    id: title.toLowerCase(),
                    categories: []
                }
            };

            const ul = $(h2).nextAll('ul').first();

            ul.find('li').each((_, li) => {
                const categoryData = {
                    id: null,
                    name: null,
                    sub_categories: []
                };

                const archiveLink = $(li)
                    .find('a')
                    .filter((_, a) => {
                        const href = $(a).attr('href');
                        return href && href.startsWith('/archive/');
                    })
                    .first();

                if (archiveLink.length) {
                    const href = archiveLink.attr('href');
                    categoryData.id = href.split('/archive/')[1];
                    categoryData.name = archiveLink.text().trim();
                }

                if (
                    categoryData.name &&
                    !['recent', 'new'].includes(categoryData.name.toLowerCase())
                ) {
                    $(li)
                        .find('a')
                        .filter((_, a) => {
                            const href = $(a).attr('href');
                            return (
                                href &&
                                href.startsWith('/list/') &&
                                href.endsWith('/recent')
                            );
                        })
                        .each((_, subCategory) => {
                            const subName = $(subCategory).text().trim();

                            if (!['recent', 'new'].includes(subName.toLowerCase())) {
                                categoryData.sub_categories.push({
                                    id: $(subCategory).attr('id') || null,
                                    name: subName
                                });
                            }
                        });

                    if (categoryData.id && categoryData.name) {
                        domainData.domain.categories.push(categoryData);
                    }
                }
            });

            if (domainData.domain.categories.length > 0) {
                data.push(domainData);
            }
        });

        return data;

    } catch (e) {
        console.error(`Error: ${e.message}`);
        return [];
    }
}


// Example usage:
//(async () => { const arxivCategories = await getCategoriesIdsFromArxivViaRequestIntoStructuredDictionary(); console.log(JSON.stringify(arxivCategories, null, 2)); })();