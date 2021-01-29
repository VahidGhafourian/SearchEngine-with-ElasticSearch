import scrapy
import time


class SoftwareengineeringCmSpider(scrapy.Spider):
    name = 'softwareEngineering-cm'
    allowed_domains = ['virgool.io']
    start_urls = ['https://virgool.io/topic/مهندسی-نرم-افزار']
    page = 1
    pageSize = 3 #Before run plaese update this variable.
    topic = 'مهندسی نرم افزار'
    def parse(self, response):
        print('='*100)
        
        for u in response.xpath("//div/article/footer/div[2]/a/@href").getall():
            print("Page founded ========" , u)
            time.sleep(0.5)
            yield scrapy.Request(url = u[:len(u)-12], dont_filter=True,  callback = self.postpagepars)
            
        time.sleep(1.5)
        self.page = self.page + 1
        if self.page <= self.pageSize:
            yield scrapy.Request(url = self.start_urls[0]+"?page="+str(self.page), callback = self.parse)

# yield scrapy.Request(url = "https://coderlife.ir/%D8%AA%D9%88%D8%B3%D8%B9%D9%87-%D9%86%D8%B1%D9%85%D8%A7%D9%81%D8%B2%D8%A7%D8%B1-%D8%A8%D8%A7-%D8%B1%D9%88%D8%B4-tdd-%DB%8C%D8%A7-test-driven-development-jyedanj9l01a", dont_filter=True, callback = self.postpagepars)
            
    def postpagepars(self, response):
        print('*'*100)
        print('*'*100)
        comment_idlist = []
        textlist = []
        parentCommentIdlist = []
        comment_authorIdlist = []
        comment_authorNamelist = []
        post_id = response.xpath('//article/@data-post-id').get()
        cmList = response.xpath('//section[@class="comments"]//div[@class="section-body"]/div[2]')
        print(len(cmList), type(cmList))
        
        self.mineComments(cmList.xpath('./div'), None, comment_idlist, comment_authorIdlist, textlist, parentCommentIdlist, comment_authorNamelist)
        for i in range(len(comment_idlist)):
            yield {
                'comment_id': comment_idlist[i],
                'topic': topic,
                'comment_author_name': comment_authorNamelist[i],
                'comment_author_id': comment_authorIdlist[i],
                'comment_text': textlist[i],
                'comment_parent_id': parentCommentIdlist[i],
                'post_id': post_id
            }
        
    def mineComments(self, response, parentCommentId, comment_idlist, comment_authorIdlist, textlist, parentCommentIdlist, comment_authorNamelist):
        
        for cmBox in response.xpath('./div'):
            comment_id = cmBox.xpath('.//form/input[@id="commentParentId"]/@value').get()
            if (cmBox.xpath('./div[3]')):
                self.mineComments(cmBox.xpath('./div[3]'), comment_id, comment_idlist, comment_authorIdlist, textlist, parentCommentIdlist, comment_authorNamelist)
            textli = cmBox.xpath('./div[1]/div[2]/text()').getall()
            text = ''.join(textli)
            text = text.replace("\n", "")
            author_name = cmBox.xpath('./div[1]/div[1]//a[@class="name"]/text()').get()
            author_id = cmBox.xpath('./div[1]/div[1]//a[@class="name"]/@href').get()
            author_id = author_id[author_id.find('@'):]

            comment_idlist.append(comment_id)
            textlist.append(text)
            parentCommentIdlist.append(parentCommentId)
            comment_authorIdlist.append(author_id)
            comment_authorNamelist.append(author_name)

        
        
        