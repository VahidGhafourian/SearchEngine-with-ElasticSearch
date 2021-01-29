import scrapy
import time

class entrepreneurshipSpider(scrapy.Spider):
    name = 'entrepreneurship'
    allowed_domains = ['virgool.io']
    start_urls = ['https://virgool.io/topic/کارآفرینی']
    topic = 'کارآفرینی'
    page = 1
    goAhead = True
    def parse(self, response):
        print('='*100)
        for u in response.xpath("//div/article/div/a/@href").getall():
            yield scrapy.Request(url = u, dont_filter=True, callback = self.postpagepars)
        time.sleep(1)
        if not response.xpath("//div/article/div/a/@href").getall():
            self.goAhead = False
            print('#'*100)
        self.page = self.page + 1
        if self.goAhead:
            yield scrapy.Request(url = self.start_urls[0]+"?page="+str(self.page), callback = self.parse)
        else :
            print("OO"*100)

#         yield scrapy.Request(url = "https://virgool.io/@haghiri75/linux-isnt-secure-cd1taha8arrl", callback = self.postpagepars)
    def postpagepars(self, response):
        print('*'*100)
        time.sleep(0.5)
        post_id = response.xpath('//article/@data-post-id').get()
        num_likes= int(response.xpath("//footer/div[@class='post-actions']/div/div/a/text()").get())
        num_comments= int(response.xpath("//footer/div[@class='post-actions']/div/button/span/text()").get()[:1])
        authorlink = response.xpath('//header/div/div/a')
        author_name = authorlink.xpath('.//text()').get()
        author_id = authorlink.xpath('.//@href').get()
        author_id = author_id[author_id.find('@'):len(author_id)]
        title = response.xpath('//h1/text()').get()
        quotes = response.xpath("//article/div/div/p/descendant::text()").getall()
        tags = response.xpath("//div[@class='post-tags']/ul/li/a/text()").getall()
        text = ""
        for quote in quotes:
            text = text + quote
            
        text = text.replace("\n", "")
        text = text.replace("\"", "'")
        author_name = author_name.replace("\n", "")
        author_id = author_id.replace("\n", "")
        title = title.replace("\n", "")
        post_id = post_id.replace("\n", "")
        
        yield {
            'id': post_id,
            'topic': self.topic,
            'author_name' : author_name,
            'author_id': author_id,
            'title': title,
            'text': text,
            'likes': num_likes,
            'comments': num_comments,
            'tags': tags
        }
