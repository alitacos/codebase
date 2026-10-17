async function getCategoriesIdsFromArxivViaBs4RequestIntoStructuredJsonList( url = 'https://arxiv.org', retries = 3, delay = 2, ...requestKwargs ) {
    let soup = null;

    for (let attempt = 0; attempt < retries; attempt++) {
        try {
            const response = await fetch(url.trim(), requestKwargs);
            const raw = await response.text();

            soup = new DOMParser().parseFromString(raw, 'text/html');

            break;

        } catch (e) {
            if (attempt < retries - 1)
                await new Promise(resolve => setTimeout(resolve, delay * 1000));
        }
    }

    if (!soup)
        return [];

    const data = [];

    try {
        for (const h2 of soup.querySelectorAll('h2')) {
            try {
                if (h2.textContent.toLowerCase() !== 'arxiv accessibility forum') {
                    const domain_data = { domain: { id: h2.textContent.toLowerCase(), categories: [] } };

                    const ul = h2.nextElementSibling;

                    if (!ul)
                        continue;

                    for (const li of ul.querySelectorAll('li')) {
                        const category_data = { id: null, name: null, sub_categories: [] };

                        const a = [...li.querySelectorAll('a')].find(x => x.getAttribute('href')?.startsWith('/archive/'));

                        if (a) {
                            const href = a.getAttribute('href');
                            category_data.id = href.split('/archive/').pop();
                            category_data.name = a.textContent.trim();
                        }

                        if (category_data.name && !['recent', 'new'].includes(category_data.name.toLowerCase())) {
                            const sub_categories = [...li.querySelectorAll('a')].filter(x => {
                                const href = x.getAttribute('href');
                                return href && href.startsWith('/list/') && href.endsWith('/recent');
                            });

                            for (const sub_category of sub_categories) {
                                if (!['recent', 'new'].includes(sub_category.textContent.trim().toLowerCase())) {
                                    category_data.sub_categories.push({
                                        id: sub_category.id,
                                        name: sub_category.textContent.trim()
                                    });
                                }
                            }

                            if (category_data.id && category_data.name)
                                domain_data.domain.categories.push(category_data);
                        }
                    }

                    if (domain_data.domain.categories.length)
                        data.push(domain_data);
                }

            } catch (e2) {}
        }

        return JSON.parse(JSON.stringify(data.filter(i => i)));

    } catch (e3) {
        return [];
    }
}