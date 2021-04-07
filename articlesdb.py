import psycopg2
import psycopg2.extras
import time

## sudo service postgresql start
## sudo -i -u postgres
## psql -U kirk -d perspective (kirk24)
## \l lists all databases
## \c perspective (change to perspective)
## \du lists all users
## \d table lists schema

class ArticleDB:

    def __init__(self):
        self.connection = psycopg2.connect(database='perspective', user='kirk', password='kirk24', host='127.0.0.1', port='5432')
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def insertArticle(self, source, title, url, story):
        data = [source,title,url,story]
        self.cursor.execute("INSERT INTO articles (source,title,url,story) VALUES (%s, %s, %s, %s);", data)
        self.connection.commit()

    def getAllArticles(self):
        self.cursor.execute("SELECT * FROM articles;")
        articles = self.cursor.fetchall()
        return articles
    
    def getOneArticle(self,article_id):
        data = [article_id]
        self.cursor.execute("SELECT * FROM articles WHERE article_id = %s;", data)
        article = self.cursor.fetchone()
        return article
    
    def getAllLikeArticles(self):
        self.cursor.execute("SET pg_trgm.similarity_threshold = 0.18; SELECT DISTINCT ON (2) a1.source AS source1, a1.title AS title1, a1.url AS url1, a1.story AS story1, a2.source AS source2, a2.title AS title2, a2.url AS url2, a2.story AS story2, a3.source AS source3, a3.title AS title3, a3.url AS url3, a3.story AS story3, AVG( similarity(a1.title, a2.title) + similarity(a2.title, a3.title) + similarity(a1.title, a3.title) ) AS sim, CAST( AVG( a1.id + a2.id + a3.id ) AS VARCHAR ) AS x FROM articles a1 JOIN articles a2 ON a1.title <> a2.title AND a1.title % a2.title AND a1.source <> a2.source JOIN articles a3 ON a1.title <> a3.title AND a1.title % a3.title AND a1.source <> a3.source AND a2.title <> a3.title AND a2.source <> a3.source GROUP BY a1.source, a1.title, a1.url, a1.story, a2.source, a2.title, a2.url, a2.story, a3.source, a3.title, a3.url, a3.story ORDER BY 2 DESC, x DESC;")
        articles = self.cursor.fetchall()
        return articles