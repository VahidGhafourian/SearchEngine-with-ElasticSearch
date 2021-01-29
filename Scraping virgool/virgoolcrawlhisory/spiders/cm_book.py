import scrapy
import time


class bookCmSpider(scrapy.Spider):
    name = 'bookcm'
    allowed_domains = ['virgool.io']
    start_urls = ['https://virgool.io/topic/کتاب']
    page = 1
    topic = 'کتاب'
    goAhead = True
    def parse(self, response):
        print('='*100)
        
        for u in response.xpath("//div/article/footer/div[2]/a/@href").getall():
            time.sleep(0.5)
            yield scrapy.Request(url = u[:len(u)-12], dont_filter=True,  callback = self.postpagepars)
        if not response.xpath("//div/article/div/a/@href").getall():
            self.goAhead = False
        time.sleep(1)
        self.page = self.page + 1
        if self.goAhead:
            yield scrapy.Request(url = self.start_urls[0]+"?page="+str(self.page), callback = self.parse)
            
    def postpagepars(self, response):
        comment_idlist = []
        textlist = []
        parentCommentIdlist = []
        comment_authorIdlist = []
        comment_authorNamelist = []
        post_id = response.xpath('//article/@data-post-id').get()
        cmList = response.xpath('//section[@class="comments"]//div[@class="section-body"]/div[2]')
        
        self.mineComments(cmList.xpath('./div'), None, comment_idlist, comment_authorIdlist, textlist, parentCommentIdlist, comment_authorNamelist)
        for i in range(len(comment_idlist)):
            yield {
                'comment_id': comment_idlist[i],
                'topic': self.topic,
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
