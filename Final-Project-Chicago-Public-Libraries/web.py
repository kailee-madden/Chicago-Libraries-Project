import os
import json
import tornado.ioloop
import tornado.web
from Libraries.db import LibrariesDB

PORT = 8888
ROOT = '.'

class MainHandler(tornado.web.RequestHandler):
    '''Requests for the landing page'''
    def get(self):
        
        self.render('search.html')
    

class SearchHandler(tornado.web.RequestHandler):
    '''Requests for Searches'''

    def initialize(self, db):
        self.db = db
        
    def get(self):
        name = self.get_argument('name')
        search = self.db.search(name)
        data = {'data':search}
        self.write(data)
     

class DetailHandler(tornado.web.RequestHandler):
    '''Requests for a single record'''

    def initialize(self, db):
        self.db = db

    def get(self):

        library_id = self.get_argument("library_id")
        row = self.db.detail(library_id) 
        data = {'data': row}
        self.write(data)

class DetailHTMLHandler(tornado.web.RequestHandler):
    '''Requests for a single record'''

    def initialize(self, db):
        self.db = db

    def post(self):

        library_id = self.get_argument("library_id")
        row = self.db.detail(library_id) 
        self.render("test.html", Detail=row)

# main code block
if __name__ == '__main__':
    db = LibrariesDB(os.path.join(ROOT, 'data'))
    
    # create app, register handlers
    app = tornado.web.Application([
            # hookup dynamic content handlers
            (r'/', MainHandler),
            (r'/search', SearchHandler, {'db': db}),
            (r'/detail', DetailHandler, {'db': db}),
            
            (r'/detailhtml', DetailHTMLHandler, {'db': db}),
            # static content handlers
            (r'/css/(.*)', tornado.web.StaticFileHandler, {'path':'web_content/css'}),
            (r'/js/(.*)', tornado.web.StaticFileHandler, {'path':'web_content/js'}),
        ],
        template_path = os.path.join('web_content', 'html'),
        debug = True
    )

    # run the app
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()