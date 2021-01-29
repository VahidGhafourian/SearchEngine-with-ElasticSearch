import scrapy
import time
import json

class PostsSpider(scrapy.Spider):
    name = 'Posts'
    allowed_domains = ['virgool.io']
    start_urls = ['https://virgool.io/api/v1.2/topics?type=interests']
    starturl = 'https://virgool.io'
    page = 1
    goAhead = True
    goNextTopic = True
    def parse(self, response):
        print('='*100)
        res = json.loads(response.xpath('/html/body/p/text()').get())
        topics = res["topics"]
        topic_urls = []
        
        for topic in topics:
            topic_urls.append(topic['url'])
        
        for url in topic_urls:
            self.goAhead = True
            print('+'*100)
            print(url)
            yield scrapy.Request(url = url, callback = self.parseTopic, meta={'starturl': url})
            
    def parseTopic(self, response):
        for u in response.xpath("//div/article/div/a/@href").getall():
            yield scrapy.Request(url = u, dont_filter=True, callback = self.postpagepars, meta={'starturl': response.meta['starturl']})
        if not response.xpath("//div/article/div/a/@href").getall():
            self.goAhead = False
            print('#'*100)
        time.sleep(2)
        self.page = self.page + 1
        if self.goAhead:
            yield scrapy.Request(url = response.meta['starturl']+"?page="+str(self.page), callback = self.parseTopic, meta={'starturl': response.meta['starturl']})
        else :
            print("OO"*100)
            self.goNextTopic = True
        
        
    def postpagepars(self, response):
        print('*'*100)
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
            'topic': response.meta['starturl'][25:],
            'author_name' : author_name,
            'author_id': author_id,
            'title': title,
            'text': text,
            'likes': num_likes,
            'comments': num_comments,
            'tags': tags
        }
   
