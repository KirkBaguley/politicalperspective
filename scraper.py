from bs4 import BeautifulSoup as soup
import requests
from articlesdb import ArticleDB

class Article:

    def __init__(self, source, title,link):
        self.source = source
        self.title = title
        self.link = link
        self.story = ""

    def __repr__(self):
        return "Article"

    def __str__(self):
        return "Source: "+ self.source + ". Title: " + self.title + " Link: " + self.link + " Story: " + self.story

def main():
    nbc_url = 'https://www.nbcnews.com/politics'
    ap_url = 'https://apnews.com/hub/politics'
    fox_url = 'https://www.foxnews.com/politics'

    nbc_r = requests.get(nbc_url)

    nbc_b = soup(nbc_r.content, 'lxml')

    nbc_articles = []
    for news in nbc_b.findAll('h2',{'class':'tease-card__headline'}):
        if 'www.msnbc.com' not in news.a['href']:
            nbc_articles.append(Article("NBC",news.text.strip(),news.a['href']))

    for i in range(len(nbc_articles)):
        page = requests.get(nbc_articles[i].link)
        bsobj = soup(page.content, 'lxml')
        for news in bsobj.findAll('div',{'class':'article-body__content'}):
            nbc_articles[i].story = (news.text.strip())

    fox_r = requests.get(fox_url)

    fox_b = soup(fox_r.content, 'lxml')

    fox_articles = []
    for news in fox_b.findAll('h4',{'class':'title'}):
        if 'video.foxnews' not in news.a['href'] and 'slideshow' not in news.a['href']:
            fox_articles.append(Article("Fox",news.text.strip(),"https://www.foxnews.com"+news.a['href']))

    for i in range(len(fox_articles)):
        try:
            page = requests.get(fox_articles[i].link)
            bsobj = soup(page.content, 'lxml')
            for news in bsobj.findAll('div',{'class':'article-body'}):
                    fox_articles[i].story = news.text.strip()
        except:
            pass

    ap_r = requests.get(ap_url)

    ap_b = soup(ap_r.content, 'lxml')

    ap_articles = []
    for news in ap_b.findAll('a',{'data-key':'card-headline'}):
        link = "https://apnews.com"+news['href']
        title = news.find('h1')
        ap_articles.append(Article("AP",title.text.strip(),link))

    for i in range(len(ap_articles)):
        story = ''
        page = requests.get(ap_articles[i].link)
        bsobj = soup(page.content, 'lxml')
        for news in bsobj.findAll('p'):
            story += news.text.strip()
        ap_articles[i].story = story

    for i in range(len(nbc_articles)):
        if nbc_articles[i].story == "" or nbc_articles[i].link == "" or nbc_articles[i].title == "":
            nbc_articles.pop(i)
            break

    for i in range(len(fox_articles)):
        if fox_articles[i].story == "" or fox_articles[i].link == "" or fox_articles[i].title == "":
            fox_articles.pop(i)
            break

    for i in range(len(ap_articles)):
        if ap_articles[i].story == "" or ap_articles[i].link == "" or ap_articles[i].title == "":
            ap_articles.pop(i)
            break
    
    db = ArticleDB()

    for i in range(len(nbc_articles)):
        try:
            db.insertArticle(nbc_articles[i].source,nbc_articles[i].title,nbc_articles[i].link,nbc_articles[i].story)
        except:
            pass
    for j in range(12,len(fox_articles)):
        try:
            db.insertArticle(fox_articles[j].source,fox_articles[j].title,fox_articles[j].link,fox_articles[j].story)
        except:
            pass

    for i in range(len(ap_articles)):
        try:
            db.insertArticle(ap_articles[i].source,ap_articles[i].title,ap_articles[i].link,ap_articles[i].story)
        except:
            pass

main()