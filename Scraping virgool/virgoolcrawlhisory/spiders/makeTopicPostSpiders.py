import scrapy
import json

class MaketopicpostspidersSpider(scrapy.Spider):
    name = 'makeTopicPostSpiders'
    allowed_domains = ['virgool.io']
    start_urls = ['https://virgool.io/api/v1.2/topics?type=interests']

    def parse(self, response):
        print('='*100)
        res = json.loads(response.xpath('/html/body/p/text()').get())
        topics = res["topics"]
        topic_urls = []
        topic_name = []
        for topic in topics:
            topic_urls.append(topic['url'])
            topic_name.append(topic['name'])
        #names = open('topicnames', 'x')
        #names.write(str(topic_name))
        #names.close()
        for i in range(len(topic_urls)):
            print(topic_name[i], topic_urls[i][25:])
            topicTemp = open('topic_cmTemplate.py', 'r')
            text = topicTemp.read()
            text = text.replace('$',topic_urls[i][25:])
            text = text.replace('&',topic_name[i])
            topici = open('./spiders/'+"cm_"+topic_name[i]+'.py', "x")
            topici.write(text)
            topici.close()
            topicTemp.close()

