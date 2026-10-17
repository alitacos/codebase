const cheerio = require("cheerio");

async function getCategoriesIdsFromArxivViaBs4RequestIntoStructuredJsonList( url = 'https://arxiv.org', retries = 3, delay = 2, ...requestKwargs ) {
    let html = null;

    for (let attempt = 0; attempt < retries; attempt++) {
        try {
            const response = await fetch(url.trim(), requestKwargs);
            html = await response.text();
            break;
        } catch (e) {
            if (attempt < retries - 1)
                await new Promise(resolve => setTimeout(resolve, delay * 1000));
        }
    }

    if (!html)
        return [];

    const $ = cheerio.load(html);
    const data = [];

    try {
        $('h2').each((i, h2) => {
            try {
                if ($(h2).text().toLowerCase() !== 'arxiv accessibility forum') {
                    const domain_data = { domain: { id: $(h2).text().toLowerCase(), categories: [] } };

                    const ul = $(h2).nextAll('ul').first();

                    ul.find('li').each((i, li) => {
                        const category_data = { id: null, name: null, sub_categories: [] };

                        const a = $(li).find('a[href^="/archive/"]').first();

                        if (a.length) {
                            const href = a.attr('href');
                            category_data.id = href.split('/archive/').pop();
                            category_data.name = a.text().trim();
                        }

                        if (category_data.name && !['recent', 'new'].includes(category_data.name.toLowerCase())) {
                            $(li).find('a[href^="/list/"][href$="/recent"]').each((i, sub_category) => {
                                if (!['recent', 'new'].includes($(sub_category).text().trim().toLowerCase())) {
                                    category_data.sub_categories.push({
                                        id: $(sub_category).attr('id'),
                                        name: $(sub_category).text().trim()
                                    });
                                }
                            });

                            if (category_data.id && category_data.name)
                                domain_data.domain.categories.push(category_data);
                        }
                    });

                    if (domain_data.domain.categories.length)
                        data.push(domain_data);
                }
            } catch (e2) {}
        });

        return JSON.parse(JSON.stringify(data.filter(i => i)));

    } catch (e3) {
        return [];
    }
}