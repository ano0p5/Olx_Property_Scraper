import scrapy

class OlxScrapy(scrapy.Spider):
    name = "olx"

    def start_requests(self):
        url = 'https://www.olx.in/kozhikode_g4058877/for-rent-houses-apartments_c1723'
        yield scrapy.Request(url=url, callback=self.parse_listing_page)

    def parse_listing_page(self, response):
        url_prefix = "https://www.olx.in"
        
         # Extracting product URLs from the start URL
        for listing in response.xpath("//li[@class='_1DNjI']"):
            relative_url = listing.css('a::attr(href)').get()
            if relative_url:
                listing_url = url_prefix + relative_url
                yield scrapy.Request(url=listing_url, callback=self.parse_listing)

        # Handle Pagination
        next_page_url = response.css('link[rel="next"]::attr(href)').get()  
        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse_listing_page)

    def parse_listing(self, response):
        yield {
            'property_name': response.css('h1[data-aut-id="itemTitle"]::text').get(default='N/A'),
            'property_id': response.xpath("//div[@class='_1-oS0']//strong/text()").getall()[2] if response.xpath("//div[@class='_1-oS0']//strong/text()").getall() else 'N/A',
            'breadcrumbs': response.xpath("//ol[@class='rui-2Pidb']/li/a[@class='_26_tZ']/text()").getall() or ['N/A'],
            'price': response.css('span[data-aut-id="itemPrice"]::text').get(default='N/A'),
            'image_url': response.css('div._23Jeb img::attr(src)').get(default='N/A'),
            'description': response.css('div[data-aut-id="itemDescriptionContent"] p::text').getall() or ['N/A'],
            'seller_name': response.xpath('//div[@class="eHFQs"]/text()').get(default='N/A'),
            'location': response.xpath('//span[@class="_1RkZP"]/text()').get(default='N/A'),
            'property_type': response.xpath('//span[@class="B6X7c"]/text()').get(default='N/A'),
            'bathrooms': response.xpath('//span[@data-aut-id="value_bathrooms"]/text()').get(default='N/A'),
            'bedrooms': response.xpath('//span[@data-aut-id="value_rooms"]/text()').get(default='N/A'),
        }