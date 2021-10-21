import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class VRoidCrawlSpider(CrawlSpider):
    name = "VRoidCrawlSpider"
    
    allowed_domains = ["hub.vroid.com"]
    urls = [
        "https://hub.vroid.com/en/models"
    ]

    rules = [
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        # Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('/en/characters/', )), callback='parse_item'),
    ]


    def start_requests(self):
        print("\n\n========== Crawling Spider ==========\n\n")
        print("\n\n========== Start Request ==========\n\n")
        urls = [
            "https://hub.vroid.com/en/models"
        ]
        for url in urls:
            yield scrapy.Request(url=url,  callback=self.parse_main_page)

    def parse_main_page(self, response):
        print("\n\n========== Main Page Call Back ==========\n\n")

    def parse_item(self, response):

        # Find Model Name:
        # Type: <a></a>
        # Element Class: ModelViewer-character-3hh9N
        # Example:
        # <a class="ModelViewer-character-3hh9N" href="/en/characters/8810551854751208803">Katsumi By Syne.Creatorツ</a>

        # The Selector was acting VERY strangely, returning the rest of the document as well.
        modelName = response.css('.ModelViewer-character-3hh9N').xpath("text()").get()
        modelLink = response.css('.ModelViewer-character-3hh9N').xpath("@href").get()
        foundModel = AnimeModel(modelName, modelLink)
        print(foundModel)
        
    def parse_additional_page(self, response, item):
        print("\n\n========== Parse Additional Header ==========\n\n")
        item['additional_data'] = response.xpath('//p[@id="additional_data"]/text()').get()
        return item

        

