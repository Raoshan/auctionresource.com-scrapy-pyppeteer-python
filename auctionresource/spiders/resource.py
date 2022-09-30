import scrapy
import pandas as pd
df = pd.read_csv('F:\Web Scraping\Golabal\keywords.csv')
base_url = 'https://auctionresource.com/Search?sort=&fromDate=&toDate=&category=&manufacturer=&model=&q={}&zipCode=&distance=&page=1'

class ResourceSpider(scrapy.Spider):
    name = 'resource'
    def start_requests(self):
        for index in df:
            yield scrapy.Request(base_url.format(index), meta={"pyppeteer": True},cb_kwargs={'index':index})

    def parse(self, response, index):
        total_pages = response.xpath('//*[@id="pageForm"]/div/select/option[last()]/text()').get()       
        current_page = ""
        try:
            current_page =response.css('[selected]::text').extract()[1]       
            # print(current_page)
        except:
            pass    
        link = response.url
       
        if total_pages and current_page:
            if int(current_page) ==1:
                for i in range(2, int(total_pages)+1): 
                    min = 'page='+str(i-1)
                    max = 'page='+str(i)
                    link = link.replace(min,max)    
                    # print(link)                                             
                    yield response.follow(link, cb_kwargs={'index':index})

        links = response.css("h3.hidden-xs a::attr(href)")
        for link in links:
            yield response.follow("https://auctionresource.com"+link.get(), callback=self.parse_item, cb_kwargs={'index':index})  
       
    def parse_item(self, response, index): 
        print(".................")  
        product_url = response.url
        print(product_url)
        image = response.css('img.img-responsive::attr(src)').get().strip()
        print(image)
       
        auction_date = response.css('.list-unstyled li::text').get().strip()
        print(auction_date)
        loc = response.xpath("//div[@class='card card-block card-primary']//div[2]/div[2]/text()").get()
        location = loc.strip()
        print(location)
        product_name = response.css('h2.no-mt.mb-1::text').get().strip()
        print(product_name)
        lot = response.css('div h4::text').get().strip()
        lot_number = lot[5:]
        print(lot_number)
        auctioner = response.css('h3.section-title::text').get().strip()
        print(auctioner)
        description = response.css('div.card-block p::text').get().strip()
        print(description)
        
        yield{
            
            'product_url' : response.url,           
            'item_type' :index.strip(),            
            'image_link' : image,          
            'auction_date' : auction_date,            
            'location' : location,           
            'product_name' : product_name,            
            'lot_id' : lot_number,          
            'auctioner' : auctioner,
            'website' : 'auctionresource',
            'description' : description             
        }