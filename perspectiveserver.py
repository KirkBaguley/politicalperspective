import os
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from http import cookies
from urllib.parse import parse_qs
from passlib.hash import bcrypt
from socketserver import ThreadingMixIn
from articlesdb import ArticleDB
from usersdb import UserDB
from sessionstore import SessionStore

gSessionStore = SessionStore()

class PerspectiveHTTPRequestHandler(BaseHTTPRequestHandler):

    def readCookie(self):
        if "Cookie" in self.headers:
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:
            self.cookie = cookies.SimpleCookie()

    def sendCookie(self):
        for morsel in self.cookie.values():
            self.send_header("Set-Cookie", morsel.OutputString())

    def loadSessionData(self):
        self.readCookie()
        if "sessionId" in self.cookie:
            sessionId = self.cookie["sessionId"].value
            sessionData = gSessionStore.getSessionData(sessionId)
            if sessionData == None:
                sessionId = gSessionStore.createSession()
                sessionData = gSessionStore.getSessionData(sessionId)
                self.cookie["sessionId"] = sessionId
        else:
            sessionId = gSessionStore.createSession()
            sessionData = gSessionStore.getSessionData(sessionId)
            self.cookie["sessionId"] = sessionId
        self.sessionData = sessionData


    def end_headers(self):
        self.sendCookie()
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        BaseHTTPRequestHandler.end_headers(self)

    def handleNotFound(self):
        self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes("Not Found", "utf-8"))

    def handleGetLikeArticles(self):
        self.send_response(200)
        self.send_header("Content-Type","application/json")
        self.end_headers()
        db = ArticleDB()
        likeArticles = db.getAllLikeArticles()
        self.wfile.write(bytes(json.dumps(likeArticles),"utf-8"))

    def handleGetOneArticle(self,member_id):
        db = ArticleDB() 
        oneArticle = db.getOneArticle(member_id)
        if oneArticle != None:
            self.send_response(200)
            self.send_header("Content-Type","application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(oneArticle),"utf-8"))
        else:
            self.handleNotFound()

    def handleCreateUser(self):
        print("The HEADERS are:", self.headers)
        length = self.headers['Content-Length']
        body = self.rfile.read(int(length)).decode("utf-8")
        parsed_body = parse_qs(body)
        fname = parsed_body["sfname"][0]
        lname = parsed_body["slname"][0]
        age = parsed_body["sage"][0]
        email = parsed_body["semail"][0]
        password = parsed_body["cspassword"][0]
        epassword = bcrypt.hash(password)
        password = None
        db = UserDB()
        user = db.getOneUser(email)
        if user == None:
            db.insertUser(fname,lname,age,email,epassword)
            self.send_response(201)
            self.end_headers()
        else:
            self.send_response(422)
            self.end_headers()
            self.wfile.write(bytes("User already exists","utf-8"))

    def handleLoginUser(self):
        print("The HEADERS are:", self.headers)
        length = self.headers['Content-Length']
        body = self.rfile.read(int(length)).decode("utf-8")
        parsed_body = parse_qs(body)
        email = parsed_body["lemail"][0]
        password = parsed_body["lpassword"][0]
        db = UserDB()
        user = db.getOneUser(email)
        if user != None:
            pdict = db.verifyUser(email)
            test = pdict['password']
            if bcrypt.verify(password, test):
                self.send_response(201)
                self.sessionData["userId"] = user["id"]
                self.end_headers()
            else:
                self.send_response(401)
                self.end_headers()
                self.wfile.write(bytes("Password or Email incorrect","utf-8"))
        else:
            self.send_response(401)
            self.end_headers()
            self.wfile.write(bytes("User does not exist.","utf-8"))

    def handleLogoutUser(self):
        if "userId" not in self.sessionData:
            self.send_response(401)
            self.end_headers()
            self.wfile.write(bytes("Error logging out","utf-8"))
            return
        self.send_response(200)
        self.sessionData["userId"] = None
        self.end_headers()

    def do_OPTIONS(self):
        self.loadSessionData()
        self.send_response(200)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        
    def do_DELETE(self):
        self.loadSessionData()
        print("The PATH is:", self.path)
        if self.path == "/sessions":
            self.handleLogoutUser()
            return
        else:
            self.handleNotFound()

    def do_GET(self):
        self.loadSessionData()
        print("The PATH is:", self.path)
        parts = self.path.split('/')
        collection = parts[1]
        article_id = None
        if len(parts) > 2:
            article_id = parts[2]
            
        if collection=="articles":
            if article_id:
                self.handleGetOneArticle(article_id)
            else:
                self.handleGetLikeArticles()
        else:
            self.handleNotFound()
            
    def do_POST(self):
        self.loadSessionData()
        print("The PATH is:", self.path)
        if self.path == "/users":
            self.handleCreateUser()
        elif self.path == "/sessions":
            self.handleLoginUser()
        else:
            self.handleNotFound()
            
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def run():
    port = int(os.environ.get("PORT",5000))
    listen = ("0.0.0.0", port)
    server = ThreadedHTTPServer(listen, PerspectiveHTTPRequestHandler)
    print("Server is ready! Listening...")
    server.serve_forever()
     
run()