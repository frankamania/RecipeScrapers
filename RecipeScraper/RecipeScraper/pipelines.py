# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

def cleanText(item):

    for key,val in item.items():

        if val is not None and type(val) == str:
            if val.strip() == '':
                val=None
            else:
                val = val.strip()
            item[key] = val



    return item

class RecipescraperPipeline:
    def process_item(self, item, spider):

        return item
