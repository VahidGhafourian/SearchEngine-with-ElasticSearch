import os
import time
text = open('topicnames', 'r').read()
text = text[1:len(text)-1].replace("'", '')
topicNames = text.split(',')
for i in range(len(topicNames)):
    os.system('/home/vahid/anaconda3/bin/scrapy crawl '+ topicNames[i].replace(' ', '') + " -s JOBDIR=crawlhistory/virgoolposts "  " -o ps_" + topicNames[i].replace(' ', '') + '.json')
