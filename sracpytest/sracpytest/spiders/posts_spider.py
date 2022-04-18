import scrapy
import string
import csv

class PostsSpider(scrapy.Spider):
    name = "names"
    
    letter = list(string.ascii_lowercase)
    start_urls = []
    for x in letter:
        for p in range(0,500):
            start_urls.append('https://www.pages-annuaire.net/particuliers/ville/Nanterre/' + x + '?p=' + str(p))
    
    
    p=1
    x=0
    
    def parse(self, response):
        if response.status == 200:
            anchors = response.css('div.col-md-3 ul li a::attr(href)').getall()
            for i in anchors:
                link = 'https://www.pages-annuaire.net' + i 
                yield scrapy.Request(link, callback= self.parse_inner)
        

    def parse_inner(self, response):
        name = response.css('h1::text').get()
        adres = response.css('h2').get()
        adres = adres.replace('<h2>', '')
        adres = adres.replace('</h2>', '')
        adres = adres.replace('<br>', ' ')
        with open('annuaire-scraper.csv','a', newline='') as f:
            w = csv.writer(f)
            w.writerow([name,adres])