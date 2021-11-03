import scrapy
from scrapy.spiders import SitemapSpider


def cleanText(item):
    for key, val in item.items():

        if val is not None and type(val) == str:
            if val.strip() == '':
                val = None
            else:
                val = val.strip()
            item[key] = val

    return item

unique_keys = []
class VegrecipesofindiaSpider(SitemapSpider):
    name = 'vegrecipesofindia'
    allowed_domains = ['www.vegrecipesofindia.com']
    #start_urls = ['http://www.vegrecipesofindia.com/']
    sitemap_urls = ['https://www.vegrecipesofindia.com/sitemap_index.xml']

    dataset_keys = ['Dough Resting Time', 'freezing time', 'Steeping Time', 'Macerating Time', 'Refrigerating time', 'Leavening Time', 'Sun Drying Time',
                    'Setting Time', 'Fermenting Time', 'resting time',
                    'fermenting time', 'keeping in sunlight', 'natural pressure release', 'Chickpeas Soaking Time', 'Resting Time', 'Marinating Time',
                    'Shaping Modak', 'Brewing Time', 'Leavening time', 'cooling time', 'Pickling Time', 'Soaking time', 'Blending Time', 'Cook Time',
                    'Total Time', 'Prep Time', 'Soaking Time', 'soaking time','Cuisine', 'Difficulty Level', 'Course', 'Diet']



    def parse(self, response):
        for recipie in  response.css('div.wprm-recipe-container'):

            dataset = {}
            dataset['name'] = recipie.css('h2.wprm-recipe-name.wprm-block-text-normal::text').get()
            dataset['author'] = recipie.css('p.entry-author a::text').get()

            for field_name in self.dataset_keys:
                dataset[field_name] = ''

            for recipe_time in recipie.css('div.wprm-recipe-times-container div.wprm-recipe-block-container'):

                key = recipe_time.css('span.wprm-recipe-details-label.wprm-block-text-normal::text').get()
                if key is not None:
                    key = key.strip()

                value = " ".join([x.strip() for x in recipe_time.xpath('.//span[@class="wprm-recipe-time wprm-block-text-bold"]//text()').getall()])

                dataset[key] = value

            for recipe_meta in recipie.css('div.wprm-recipe-meta-container div.wprm-recipe-block-container'):

                key = recipe_meta.css('span.wprm-recipe-details-label.wprm-block-text-normal::text').get()

                if key is not None:
                    key = key.strip()
                    unique_keys.append(key)
                value = " ".join([x.strip() for x in recipe_meta.css('span.wprm-block-text-bold::text').getall()])
                dataset[key] = value


            dataset['servings'] = recipie.css('div.wprm-recipe-ingredients-servings span.wprm-recipe-servings-with-unit input.wprm-recipe-servings::attr(value)').get()
            dataset['servings_unit'] = recipie.css('div.wprm-recipe-ingredients-servings span.wprm-recipe-servings-with-unit span.wprm-recipe-servings-unit.wprm-recipe-details-unit::text').get()

            dataset['ingredients'] = []
            dataset['instructions'] = []

            for ingredients in recipie.css('ul.wprm-recipe-ingredients li.wprm-recipe-ingredient'):
                dataset['ingredients'].append(cleanText({
                    "amount": ingredients.css('span.wprm-recipe-ingredient-amount::text').get(),
                    "unit": ingredients.css('span.wprm-recipe-ingredient-unit::text').get(),
                    "name": ingredients.css('span.wprm-recipe-ingredient-name::text').get(),
                    "notes": ingredients.css('span.wprm-recipe-ingredient-notes::text').get(),
                }))


            for instructions in recipie.css('div.wprm-recipe-instructions-container div.wprm-recipe-instruction-group'):

                instruction_section = instructions.css('h4.wprm-recipe-group-name.wprm-recipe-instruction-group-name::text').get()
                if instruction_section is not None:
                    instruction_section = instruction_section.strip()

                dataset['instructions'].append({
                    "title": instruction_section,
                    "instructions": [instruction.strip() for instruction in instructions.css('ul.wprm-recipe-instructions li div.wprm-recipe-instruction-text span::text').getall()],
                })



            yield cleanText(dataset)



